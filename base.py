"""Base classes and runtime for CLI-to-Mattermost bridges."""

from __future__ import annotations

import json
import os
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests


def _format_error(code: str, message: str) -> str:
    return f"[{code}] {message}"


def _now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    tmp_path = path.with_suffix(f"{path.suffix}.tmp")
    tmp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp_path.replace(path)


class BridgeConfig:
    """Configuration for a CLI bridge instance."""

    def __init__(
        self,
        backend_name: str,
        bot_name: str,
        channel_id: str,
        bot_token: str,
        monitor_token: str,
        mm_url: str = "",
        poll_interval: int = 30,
        cli_cmd: str = "",
        cli_args: list[str] | None = None,
        state_file: str = "",
        working_dir: str = ".",
        max_response_length: int = 3800,
        mode: str = "execute",
        respond_to_mentions: bool = True,
        task_prefix: str = "",
        task_regex: str = "",
        cli_timeout_seconds: int = 300,
        mm_per_page: int = 100,
        mm_max_pages: int = 5,
        retry_max_attempts: int = 3,
        retry_base_seconds: float = 1.0,
        heartbeat_file: str = "",
    ):
        self.backend_name = backend_name
        self.bot_name = bot_name
        self.channel_id = channel_id
        self.bot_token = bot_token
        self.monitor_token = monitor_token
        self.mm_url = (mm_url or os.getenv("MM_URL", "http://10.40.10.83:8065")).rstrip("/")
        self.poll_interval = poll_interval
        self.cli_cmd = cli_cmd
        self.cli_args = cli_args or []
        self.state_file = state_file or f".{backend_name}_bridge_state.json"
        self.working_dir = working_dir
        self.max_response_length = max_response_length
        self.mode = mode
        self.respond_to_mentions = respond_to_mentions
        self.task_prefix = task_prefix
        self.task_regex = task_regex
        self.cli_timeout_seconds = cli_timeout_seconds
        self.mm_per_page = mm_per_page
        self.mm_max_pages = mm_max_pages
        self.retry_max_attempts = retry_max_attempts
        self.retry_base_seconds = retry_base_seconds
        self.heartbeat_file = heartbeat_file or f".{backend_name}_bridge_heartbeat.json"


class BridgeState:
    """Persistent state for a bridge instance."""

    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.data = self._load()

    def _load(self) -> dict[str, Any]:
        default_state = {
            "last_ts": 0,
            "handled_ids": [],
            "active_tasks": {},
            "pending_posts": {},
        }
        if not self.state_file.exists():
            return default_state

        try:
            data = json.loads(self.state_file.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return default_state
            for key, value in default_state.items():
                data.setdefault(key, value)
            if not isinstance(data.get("handled_ids"), list):
                data["handled_ids"] = []
            if not isinstance(data.get("active_tasks"), dict):
                data["active_tasks"] = {}
            if not isinstance(data.get("pending_posts"), dict):
                data["pending_posts"] = {}
            return data
        except Exception:
            return default_state

    def save(self) -> None:
        handled_ids = self.data.get("handled_ids", [])
        if len(handled_ids) > 500:
            self.data["handled_ids"] = handled_ids[-500:]
        _atomic_write_json(self.state_file, self.data)

    @property
    def last_ts(self) -> int:
        return int(self.data.get("last_ts", 0) or 0)

    @last_ts.setter
    def last_ts(self, value: int) -> None:
        self.data["last_ts"] = int(value)

    def bump_last_ts(self, value: int) -> None:
        if value > self.last_ts:
            self.last_ts = value

    def is_handled(self, post_id: str) -> bool:
        return post_id in self.data.get("handled_ids", [])

    def has_pending(self, post_id: str) -> bool:
        return post_id in self.data.get("pending_posts", {})

    def mark_handled(self, post_id: str, create_at: int = 0) -> None:
        handled = self.data.setdefault("handled_ids", [])
        if post_id not in handled:
            handled.append(post_id)
        self.bump_last_ts(create_at)
        self.data.setdefault("pending_posts", {}).pop(post_id, None)

    def add_pending_post(self, post_id: str, payload: dict[str, Any], create_at: int) -> None:
        pending = self.data.setdefault("pending_posts", {})
        pending[post_id] = {
            "channel_id": payload.get("channel_id", ""),
            "message": payload.get("message", ""),
            "root_id": payload.get("root_id", ""),
            "attempts": int(pending.get(post_id, {}).get("attempts", 0)),
            "created_at": create_at,
            "updated_at": _now_iso(),
        }
        self.bump_last_ts(create_at)


class BaseBridge:
    """Base class for CLI-to-Mattermost bridges."""

    def __init__(self, config: BridgeConfig):
        self.config = config
        self.script_dir = Path(__file__).parent.parent
        self.state = BridgeState(self.script_dir / config.state_file)
        self.heartbeat_file = self.script_dir / config.heartbeat_file

        self._monitor_headers = {
            "Authorization": f"Bearer {config.monitor_token}",
            "Content-Type": "application/json",
        }
        self._bot_headers = {
            "Authorization": f"Bearer {config.bot_token}",
            "Content-Type": "application/json",
        }
        self._username_cache: dict[str, str] = {}
        self._bot_user_id: str = ""  # Resolved at startup to skip own posts

        self._session = requests.Session()
        self._error_count = 0

    # ---- Config / lifecycle ----

    def validate_config(self) -> list[str]:
        errors: list[str] = []
        if not self.config.channel_id:
            errors.append(_format_error("E-CONFIG-CHANNEL", "channel_id is missing"))
        if not self.config.mm_url:
            errors.append(_format_error("E-CONFIG-MMURL", "mm_url is missing"))
        if not self.config.monitor_token:
            errors.append(_format_error("E-CONFIG-MONITOR-TOKEN", "monitor token is missing"))

        if self.config.mode == "execute":
            if not self.config.bot_token:
                errors.append(_format_error("E-CONFIG-BOT-TOKEN", "bot token is missing"))
            if not self.config.cli_cmd:
                errors.append(_format_error("E-CONFIG-CLI", "cli_cmd is missing in execute mode"))

        if self.config.poll_interval <= 0:
            errors.append(_format_error("E-CONFIG-POLL", "poll_interval must be > 0"))
        if self.config.mm_per_page <= 0:
            errors.append(_format_error("E-CONFIG-PERPAGE", "mm_per_page must be > 0"))
        if self.config.mm_max_pages <= 0:
            errors.append(_format_error("E-CONFIG-MAXPAGES", "mm_max_pages must be > 0"))
        if self.config.retry_max_attempts <= 0:
            errors.append(_format_error("E-CONFIG-RETRY", "retry_max_attempts must be > 0"))

        return errors

    def update_heartbeat(self, status: str, *, error: str = "", success: bool = False) -> None:
        now = _now_iso()
        payload: dict[str, Any] = {
            "backend": self.config.backend_name,
            "bot_name": self.config.bot_name,
            "pid": os.getpid(),
            "status": status,
            "last_poll": now,
            "error_count": self._error_count,
        }

        if self.heartbeat_file.exists():
            try:
                existing = json.loads(self.heartbeat_file.read_text(encoding="utf-8"))
                if isinstance(existing, dict):
                    payload = {**existing, **payload}
            except Exception:
                pass

        payload.setdefault("started", now)
        if success:
            payload["last_success"] = now
        if error:
            payload["last_error"] = error

        try:
            _atomic_write_json(self.heartbeat_file, payload)
        except Exception:
            # Heartbeat errors must never crash the bridge loop.
            pass

    # ---- MM API ----

    def _retry_delay(self, response: requests.Response | None, attempt: int) -> float:
        if response is not None:
            retry_after = response.headers.get("Retry-After", "").strip()
            if retry_after.isdigit():
                return max(float(retry_after), 0.0)

        exp = max(attempt - 1, 0)
        return max(self.config.retry_base_seconds * (2**exp), 0.0)

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        json_body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.config.mm_url}/api/v4{endpoint}"
        retries = self.config.retry_max_attempts
        last_error = ""

        for attempt in range(1, retries + 1):
            response: requests.Response | None = None
            try:
                response = self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json_body,
                    timeout=10,
                )

                status = response.status_code
                if status in {429, 500, 502, 503, 504} and attempt < retries:
                    delay = self._retry_delay(response, attempt)
                    time.sleep(delay)
                    continue

                response.raise_for_status()
                if not response.content:
                    return {}
                data = response.json()
                if isinstance(data, dict):
                    return data
                return {"data": data}

            except requests.exceptions.HTTPError as exc:
                status = exc.response.status_code if exc.response is not None else "unknown"
                body = ""
                if exc.response is not None:
                    body = exc.response.text.strip().replace("\n", " ")[:240]
                last_error = _format_error(
                    "E-MM-HTTP",
                    f"{method} {endpoint} failed with status {status}: {body or 'no body'}",
                )

                if status in {429, 500, 502, 503, 504} and attempt < retries:
                    delay = self._retry_delay(exc.response, attempt)
                    time.sleep(delay)
                    continue
                raise RuntimeError(last_error) from exc

            except requests.exceptions.RequestException as exc:
                last_error = _format_error(
                    "E-MM-CONNECTION",
                    f"{method} {endpoint} failed: {type(exc).__name__}: {exc}",
                )
                if attempt < retries:
                    delay = self._retry_delay(response, attempt)
                    time.sleep(delay)
                    continue
                raise RuntimeError(last_error) from exc

        raise RuntimeError(last_error or _format_error("E-MM-UNKNOWN", f"{method} {endpoint} failed"))

    def mm_get(self, endpoint: str) -> dict[str, Any]:
        return self._request("GET", endpoint, headers=self._monitor_headers)

    def mm_post_as_bot(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", endpoint, json_body=data, headers=self._bot_headers)

    def get_channel_posts(self, since: int = 0) -> list[dict[str, Any]]:
        posts_by_id: dict[str, dict[str, Any]] = {}
        page = 0

        while page < self.config.mm_max_pages:
            if since > 0:
                endpoint = (
                    f"/channels/{self.config.channel_id}/posts"
                    f"?since={since}&page={page}&per_page={self.config.mm_per_page}"
                )
            else:
                endpoint = (
                    f"/channels/{self.config.channel_id}/posts"
                    f"?page={page}&per_page={self.config.mm_per_page}"
                )

            data = self.mm_get(endpoint)
            order = data.get("order", [])
            posts_dict = data.get("posts", {})
            if not order:
                break

            for post_id in order:
                post = posts_dict.get(post_id)
                if isinstance(post, dict):
                    posts_by_id[post_id] = post

            if len(order) < self.config.mm_per_page:
                break
            page += 1

        posts = list(posts_by_id.values())
        posts.sort(key=lambda p: p.get("create_at", 0))
        return posts

    def post_message(self, text: str, *, root_id: str = "") -> None:
        payload = {
            "channel_id": self.config.channel_id,
            "message": text,
        }
        if root_id:
            payload["root_id"] = root_id
        self.mm_post_as_bot("/posts", payload)

    def get_username(self, user_id: str) -> str:
        if user_id in self._username_cache:
            return self._username_cache[user_id]

        try:
            user = self.mm_get(f"/users/{user_id}")
            name = str(user.get("username", user_id[:8]))
            self._username_cache[user_id] = name
            return name
        except Exception:
            return user_id[:8]

    # ---- Mention detection / backends ----

    def should_respond(self, post: dict[str, Any]) -> bool:
        if not self.config.respond_to_mentions:
            return False
        message = str(post.get("message", "")).lower()
        return f"@{self.config.bot_name.lower()}" in message

    def detect_task(self, post: dict[str, Any]) -> dict[str, Any] | None:
        return None

    def detect_completion(self, post: dict[str, Any]) -> bool:
        return False

    def execute_task(self, task_info: dict[str, Any]) -> str:
        raise NotImplementedError("Subclass must implement execute_task()")

    # ---- CLI execution ----

    def _truncate_output(self, output: str) -> str:
        if len(output) > self.config.max_response_length:
            return output[: self.config.max_response_length] + "\n\n*(...gekuerzt)*"
        return output

    def execute_subprocess(
        self,
        cmd: list[str],
        *,
        stdin: str | None = None,
        timeout: int | None = None,
        env: dict[str, str] | None = None,
    ) -> str:
        try:
            result = subprocess.run(
                cmd,
                input=stdin,
                capture_output=True,
                text=True,
                timeout=timeout or self.config.cli_timeout_seconds,
                cwd=self.config.working_dir,
                env=env,
            )
        except subprocess.TimeoutExpired:
            return _format_error("E-CLI-TIMEOUT", "CLI command timed out")
        except FileNotFoundError:
            return _format_error("E-CLI-NOTFOUND", f"CLI not found: {cmd[0] if cmd else 'unknown'}")
        except Exception as exc:
            return _format_error("E-CLI-RUNTIME", f"{type(exc).__name__}: {exc}")

        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()

        if result.returncode != 0:
            detail = stderr or stdout or "no output"
            detail_lower = detail.lower()
            detail = detail.replace("\n", " ")[:300]

            # Categorize common CLI errors
            if any(kw in detail_lower for kw in ("429", "rate limit", "quota", "no capacity")):
                code = "E-CLI-QUOTA"
            elif any(kw in detail_lower for kw in ("permission denied", "sandbox", "policy block")):
                code = "E-CLI-PERMISSION"
            elif any(kw in detail_lower for kw in ("unauthorized", "auth", "token expired", "401")):
                code = "E-CLI-AUTH"
            else:
                code = "E-CLI-EXIT"

            return _format_error(
                code,
                f"command exited with code {result.returncode}: {detail}",
            )

        output = stdout or stderr or "(no output)"
        return self._truncate_output(output)

    def run_cli(self, prompt: str, extra_args: list[str] | None = None) -> str:
        cmd = [self.config.cli_cmd] + self.config.cli_args + (extra_args or [])
        return self.execute_subprocess(cmd, stdin=prompt)

    # ---- Posting and idempotency ----

    def _enqueue_response(
        self,
        post_id: str,
        *,
        message: str,
        create_at: int,
        root_id: str = "",
    ) -> None:
        payload = {
            "channel_id": self.config.channel_id,
            "message": message,
            "root_id": root_id,
        }
        self.state.add_pending_post(post_id, payload, create_at)
        self.state.save()

    def _deliver_pending_post(self, post_id: str) -> bool:
        pending = self.state.data.get("pending_posts", {}).get(post_id)
        if not isinstance(pending, dict):
            return True

        payload = {
            "channel_id": pending.get("channel_id", self.config.channel_id),
            "message": pending.get("message", ""),
        }
        root_id = str(pending.get("root_id", "") or "")
        if root_id:
            payload["root_id"] = root_id

        try:
            self.mm_post_as_bot("/posts", payload)
            self.state.data.get("pending_posts", {}).pop(post_id, None)
            return True
        except Exception:
            pending["attempts"] = int(pending.get("attempts", 0)) + 1
            pending["updated_at"] = _now_iso()
            return False

    def process_pending_posts(self) -> None:
        pending_ids = list(self.state.data.get("pending_posts", {}).keys())
        if not pending_ids:
            return

        for post_id in pending_ids:
            pending = self.state.data.get("pending_posts", {}).get(post_id, {})
            create_at = int(pending.get("created_at", 0) or 0)
            delivered = self._deliver_pending_post(post_id)
            if delivered:
                self.state.mark_handled(post_id, create_at)

        self.state.save()

    # ---- Main processing ----

    def _sender_reply(self, sender: str, body: str, task_name: str = "") -> str:
        # Anti-loop: Never @mention echo_log in responses — it triggers a feedback loop
        # where echo_log's MM bot picks up the @mention and processes it as new input
        if sender.lower() == "echo_log":
            sender = "echo-log"  # Use hyphen to prevent @mention matching
        if task_name:
            return f"@{sender} [{task_name}] {body}"
        return f"@{sender} {body}"

    def _mark_task_pending(self, task_name: str, create_at: int, post_id: str) -> None:
        self.state.data.setdefault("active_tasks", {})[task_name] = {
            "status": "pending",
            "created_at": create_at,
            "post_id": post_id,
        }

    def _mark_first_pending_task_complete(self, create_at: int) -> None:
        for _, info in self.state.data.get("active_tasks", {}).items():
            if info.get("status") == "pending":
                info["status"] = "completed"
                info["completed_at"] = create_at
                break

    def process_posts(self, posts: list[dict[str, Any]]) -> None:
        for post in posts:
            post_id = str(post.get("id", ""))
            user_id = str(post.get("user_id", ""))
            message = str(post.get("message", "")).strip()
            create_at = int(post.get("create_at", 0) or 0)
            root_id = str(post.get("root_id", "") or "")

            if not post_id:
                continue
            if self.state.is_handled(post_id):
                continue
            if self.state.has_pending(post_id):
                pending = self.state.data.get("pending_posts", {}).get(post_id, {})
                create_at_pending = int(pending.get("created_at", 0) or 0)
                delivered = self._deliver_pending_post(post_id)
                if delivered:
                    self.state.mark_handled(post_id, create_at_pending)
                self.state.save()
                continue

            self.state.bump_last_ts(create_at)

            # Anti-loop: Skip own posts (bot responding to itself)
            if self._bot_user_id and user_id == self._bot_user_id:
                self.state.mark_handled(post_id, create_at)
                self.state.save()
                continue

            if not message:
                self.state.mark_handled(post_id, create_at)
                self.state.save()
                continue

            sender = self.get_username(user_id)
            ts = datetime.fromtimestamp(create_at / 1000, tz=UTC).strftime("%H:%M:%S")

            try:
                task_info = self.detect_task(post)
                if task_info is not None:
                    task_name = str(task_info.get("name", "TASK"))
                    print(f"[{ts}] TASK DETECTED: {task_name} from @{sender}")
                    self._mark_task_pending(task_name, create_at, post_id)

                    if self.config.mode == "execute":
                        response = self.execute_task(task_info)
                        outbound = self._sender_reply(sender, response, task_name=task_name)
                        self._enqueue_response(post_id, message=outbound, create_at=create_at, root_id=root_id)
                        delivered = self._deliver_pending_post(post_id)
                        if delivered:
                            self.state.mark_handled(post_id, create_at)
                    else:
                        self.state.mark_handled(post_id, create_at)

                    self.state.save()
                    continue

                if self.detect_completion(post):
                    print(f"[{ts}] COMPLETION from @{sender}: {message[:100]}...")
                    self._mark_first_pending_task_complete(create_at)
                    self.state.mark_handled(post_id, create_at)
                    self.state.save()
                    continue

                if self.should_respond(post) and self.config.mode == "execute":
                    print(f"[{ts}] @{self.config.bot_name} mentioned by @{sender}")
                    clean_msg = message.replace(f"@{self.config.bot_name}", "").strip()
                    if clean_msg:
                        response = self.run_cli(clean_msg)
                        outbound = self._sender_reply(sender, response)
                        self._enqueue_response(post_id, message=outbound, create_at=create_at, root_id=root_id)
                        delivered = self._deliver_pending_post(post_id)
                        if delivered:
                            self.state.mark_handled(post_id, create_at)
                    else:
                        self.state.mark_handled(post_id, create_at)
                else:
                    self.state.mark_handled(post_id, create_at)

                self.state.save()

            except Exception as exc:
                self._error_count += 1
                error_text = _format_error("E-STATE-PROCESS", f"{type(exc).__name__}: {exc}")
                self.update_heartbeat("degraded", error=error_text)
                # Do not mark as handled here; keep post for next cycle.

    # ---- Polling loop ----

    def show_status(self) -> None:
        tasks = self.state.data.get("active_tasks", {})
        if tasks:
            print("\nActive Tasks:")
            for name, info in sorted(tasks.items()):
                status = info.get("status", "unknown")
                icon = "+" if status == "completed" else "~" if status == "pending" else "?"
                print(f"  {icon} {name}: {status}")
            print()

    def run(self, *, once: bool = False) -> int:
        name = self.config.bot_name
        print("=" * 60)
        print(f"CLI BRIDGE - {name}")
        print("=" * 60)
        print(f"Backend:    {self.config.backend_name}")
        print(f"MM URL:     {self.config.mm_url}")
        print(f"Channel:    {self.config.channel_id}")
        print(f"Bot:        @{name}")
        print(f"CLI:        {self.config.cli_cmd or '(monitor only)'}")
        print(f"Mode:       {self.config.mode}")
        print(f"Interval:   {self.config.poll_interval}s")
        print("=" * 60)

        config_errors = self.validate_config()
        if config_errors:
            for item in config_errors:
                print(item)
            return 1

        try:
            me = self.mm_get("/users/me")
            print(f"Reading as: @{me.get('username', '?')} ({me.get('id', '?')})")
        except Exception as exc:
            print(_format_error("E-MM-CONNECTION", f"Cannot connect to Mattermost: {exc}"))
            return 1

        # Verify bot token identity (the token used for posting responses)
        if self.config.bot_token:
            try:
                bot_me = self._request("GET", "/users/me", headers=self._bot_headers)
                bot_user = bot_me.get("username", "?")
                bot_id = bot_me.get("id", "?")
                self._bot_user_id = str(bot_id)
                print(f"Posting as: @{bot_user} ({bot_id})")
                if bot_user != name:
                    print(
                        f"WARNING: Bot name is @{name} but posting token belongs to @{bot_user}! "
                        f"Responses will appear as @{bot_user}."
                    )
            except Exception as exc:
                print(_format_error("E-BOT-TOKEN", f"Bot token verification failed: {exc}"))

        self.show_status()

        if self.state.last_ts == 0:
            self.state.last_ts = int(time.time() * 1000) - 60000
            try:
                self.state.save()
            except Exception as exc:
                print(_format_error("E-STATE-SAVE", f"Failed to initialize state: {exc}"))
                return 1

        self.update_heartbeat("running")
        print("Starting poll loop... (Ctrl+C to stop)\n")

        while True:
            cycle_ok = False
            try:
                self.process_pending_posts()
                posts = self.get_channel_posts(since=self.state.last_ts)
                if posts:
                    self.process_posts(posts)
                    self.state.save()
                cycle_ok = True

            except Exception as exc:
                self._error_count += 1
                ts = datetime.now().strftime("%H:%M:%S")
                error_text = _format_error("E-MM-POLL", f"{type(exc).__name__}: {exc}")
                print(f"[{ts}] {error_text}")
                self.update_heartbeat("degraded", error=error_text)

            if cycle_ok:
                self.update_heartbeat("running", success=True)

            if once:
                return 0 if cycle_ok else 1

            time.sleep(self.config.poll_interval)

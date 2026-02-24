"""Echo Log backend - Claude Opus 4.5 CLI bridge with Codex subagent support."""

from __future__ import annotations

import json
import os
import re
from typing import Any

from ..base import BaseBridge

DEFAULT_TASK_PATTERN = re.compile(r"##\s*ECHO[_-]?LOG-TASK[:\s]*(.*)", re.IGNORECASE | re.DOTALL)
CODEX_SUBAGENT_PATTERN = re.compile(r"##\s*CODEX-SUBAGENT[:\s]*(.*)", re.IGNORECASE | re.DOTALL)


class EchoLogBridge(BaseBridge):
    """Echo Log (Claude Opus 4.5) bridge with Codex subagent for large tasks.

    Features:
    - Primary: Responds to ## ECHO_LOG-TASK: commands
    - Subagent: Delegates ## CODEX-SUBAGENT: tasks to Codex CLI
    - Integration: Works with Claude Code CLI (claude command)
    - Persona: Network Admin / AIOps specialist for HomeLab infrastructure
    """

    _compiled_task_regex: re.Pattern[str] | None = None
    _compiled_codex_regex: re.Pattern[str] | None = None

    def _get_task_pattern(self) -> re.Pattern[str]:
        if self._compiled_task_regex is not None:
            return self._compiled_task_regex

        if self.config.task_regex:
            self._compiled_task_regex = re.compile(self.config.task_regex, re.IGNORECASE | re.DOTALL)
        else:
            self._compiled_task_regex = DEFAULT_TASK_PATTERN
        return self._compiled_task_regex

    def _get_codex_pattern(self) -> re.Pattern[str]:
        if self._compiled_codex_regex is not None:
            return self._compiled_codex_regex
        self._compiled_codex_regex = CODEX_SUBAGENT_PATTERN
        return self._compiled_codex_regex

    def _is_mentioned(self, message: str) -> bool:
        """Check if @echo_log is mentioned in the message."""
        lower_msg = message.lower()
        return "@echo_log" in lower_msg or "@echo-log" in lower_msg

    def detect_task(self, post: dict[str, Any]) -> dict[str, Any] | None:
        message = str(post.get("message", ""))

        # Check for Codex subagent task first
        codex_match = self._get_codex_pattern().search(message)
        if codex_match and self._is_mentioned(message):
            prompt = (codex_match.group(1) if codex_match.groups() else "").strip()
            if not prompt:
                prompt = message
            return {
                "name": "CODEX-SUBAGENT",
                "prompt": prompt,
                "post_id": post.get("id", ""),
                "is_codex": True,
            }

        # Check for standard echo_log task
        if not self._is_mentioned(message):
            return None

        match = self._get_task_pattern().search(message)
        if not match:
            return None

        prompt = (match.group(1) if match.groups() else "").strip()
        if not prompt:
            prompt = message

        return {
            "name": "ECHO_LOG-TASK",
            "prompt": prompt,
            "post_id": post.get("id", ""),
            "is_codex": False,
        }

    def _extract_text_from_json(self, payload: str) -> str:
        """Extract text content from Claude JSON output."""
        payload = payload.strip()
        if not payload:
            return ""

        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError:
            return ""

        if isinstance(parsed, dict):
            for key in ("text", "content", "result", "response"):
                value = parsed.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()

            content = parsed.get("content")
            if isinstance(content, list):
                parts: list[str] = []
                for item in content:
                    if isinstance(item, dict):
                        text = item.get("text")
                        if isinstance(text, str) and text.strip():
                            parts.append(text.strip())
                if parts:
                    return "\n".join(parts)

        if isinstance(parsed, list):
            parts = []
            for item in parsed:
                if isinstance(item, dict):
                    text = item.get("text") or item.get("content")
                    if isinstance(text, str) and text.strip():
                        parts.append(text.strip())
            if parts:
                return "\n".join(parts)

        return ""

    def _execute_codex_subagent(self, prompt: str) -> str:
        """Execute a task using Codex CLI as subagent for large/complex tasks.

        Uses 'codex' CLI with full auto mode for autonomous task execution.
        Ideal for: Multi-file refactoring, large codebase analysis, complex automation.
        """
        codex_cmd = os.getenv("CODEX_CLI_CMD", "codex")
        codex_args = [
            "--full-auto",  # Autonomous execution
            "--quiet",      # Reduced output
        ]

        # Add approval mode if configured
        approval_mode = os.getenv("CODEX_APPROVAL_MODE", "auto-edit")
        if approval_mode:
            codex_args.extend(["--approval-mode", approval_mode])

        cmd = [codex_cmd] + codex_args + [prompt]

        # Codex tasks get longer timeout (10 minutes default)
        codex_timeout = int(os.getenv("CODEX_TIMEOUT_SECONDS", "600"))

        result = self.execute_subprocess(
            cmd,
            timeout=codex_timeout,
        )

        # Prefix response to indicate Codex handled it
        if not result.startswith("[E-"):
            result = f"**[Codex Subagent]**\n\n{result}"

        return result

    def execute_task(self, task_info: dict[str, Any]) -> str:
        prompt = str(task_info.get("prompt", "")).strip()
        if not prompt:
            return "[E-CLI-INPUT] Empty task prompt"

        # Route to Codex subagent if flagged
        if task_info.get("is_codex"):
            return self._execute_codex_subagent(prompt)

        # Standard Claude execution
        cmd_base = [self.config.cli_cmd] + self.config.cli_args
        preferred_output = os.getenv("CLAUDE_OUTPUT_FORMAT", "json").strip().lower()

        if preferred_output == "json":
            cmd_json = cmd_base + ["--output-format", "json", "-p", prompt]
            raw = self.execute_subprocess(cmd_json)
            if raw.startswith("[E-"):
                return raw

            parsed = self._extract_text_from_json(raw)
            if parsed:
                return self._truncate_output(parsed)

        cmd_text = cmd_base + ["-p", prompt]
        return self.execute_subprocess(cmd_text)

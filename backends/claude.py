"""Claude backend - Claude Code CLI bridge."""

from __future__ import annotations

import json
import os
import re
from typing import Any

from ..base import BaseBridge

DEFAULT_TASK_PATTERN = re.compile(r"##\s*CLAUDE-TASK[:\s]*(.*)", re.IGNORECASE | re.DOTALL)


class ClaudeBridge(BaseBridge):
    """Claude CLI bridge for CLAUDE-TASK execution."""

    _compiled_task_regex: re.Pattern[str] | None = None

    def _get_task_pattern(self) -> re.Pattern[str]:
        if self._compiled_task_regex is not None:
            return self._compiled_task_regex

        if self.config.task_regex:
            self._compiled_task_regex = re.compile(self.config.task_regex, re.IGNORECASE | re.DOTALL)
        else:
            self._compiled_task_regex = DEFAULT_TASK_PATTERN
        return self._compiled_task_regex

    def _is_mentioned(self, message: str) -> bool:
        return f"@{self.config.bot_name.lower()}" in message.lower()

    def detect_task(self, post: dict[str, Any]) -> dict[str, Any] | None:
        message = str(post.get("message", ""))
        if not self._is_mentioned(message):
            return None

        match = self._get_task_pattern().search(message)
        if not match:
            return None

        prompt = (match.group(1) if match.groups() else "").strip()
        if not prompt:
            prompt = message

        return {
            "name": "CLAUDE-TASK",
            "prompt": prompt,
            "post_id": post.get("id", ""),
        }

    def _extract_text_from_json(self, payload: str) -> str:
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

    def execute_task(self, task_info: dict[str, Any]) -> str:
        prompt = str(task_info.get("prompt", "")).strip()
        if not prompt:
            return "[E-CLI-INPUT] Empty task prompt"

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

"""OpenAI Codex CLI backend - execute mode for CODEX tasks."""

from __future__ import annotations

import re
from typing import Any

from ..base import BaseBridge

DEFAULT_TASK_PATTERN = re.compile(
    r"##\s*CODEX-TASK(?:-R\d+)?[:\s]*(.*)", re.IGNORECASE | re.DOTALL
)


class OpenAICodexBridge(BaseBridge):
    """OpenAI Codex CLI bridge for CODEX-TASK execution."""

    _compiled_task_regex: re.Pattern[str] | None = None

    def _get_task_pattern(self) -> re.Pattern[str]:
        if self._compiled_task_regex is not None:
            return self._compiled_task_regex

        if self.config.task_regex:
            self._compiled_task_regex = re.compile(self.config.task_regex, re.IGNORECASE | re.DOTALL)
        else:
            self._compiled_task_regex = DEFAULT_TASK_PATTERN
        return self._compiled_task_regex

    def _is_task_post(self, message: str) -> bool:
        """Check if message contains a CODEX-TASK pattern."""
        return bool(self._get_task_pattern().search(message))

    def _is_mentioned(self, message: str) -> bool:
        return f"@{self.config.bot_name.lower()}" in message.lower()

    def detect_task(self, post: dict[str, Any]) -> dict[str, Any] | None:
        message = str(post.get("message", ""))

        # Accept task if it has the CODEX-TASK pattern (with or without @mention)
        match = self._get_task_pattern().search(message)
        if not match:
            # Also accept plain @mentions (without task prefix)
            if self.config.respond_to_mentions and self._is_mentioned(message):
                return None  # Let base class handle via should_respond + run_cli
            return None

        prompt = (match.group(1) if match.groups() else "").strip()
        if not prompt:
            prompt = message

        return {
            "name": "CODEX-TASK",
            "prompt": prompt,
            "post_id": post.get("id", ""),
        }

    def execute_task(self, task_info: dict[str, Any]) -> str:
        prompt = str(task_info.get("prompt", "")).strip()
        if not prompt:
            return "[E-CLI-INPUT] Empty task prompt"

        cmd = [self.config.cli_cmd] + self.config.cli_args + ["--ephemeral", prompt]
        return self.execute_subprocess(cmd)

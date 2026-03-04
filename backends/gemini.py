"""Gemini backend - Google Gemini CLI bridge."""

from __future__ import annotations

import re
from typing import Any

from ..base import BaseBridge

DEFAULT_TASK_PATTERN = re.compile(
    r"##\s*GEMINI-TASK(?:-R\d+)?[:\s]*(.*)", re.IGNORECASE | re.DOTALL
)


class GeminiBridge(BaseBridge):
    """Google Gemini CLI bridge for research and analysis tasks."""

    _compiled_task_regex: re.Pattern[str] | None = None

    def _get_task_pattern(self) -> re.Pattern[str]:
        if self._compiled_task_regex is not None:
            return self._compiled_task_regex

        if self.config.task_regex:
            self._compiled_task_regex = re.compile(self.config.task_regex, re.IGNORECASE | re.DOTALL)
        else:
            self._compiled_task_regex = DEFAULT_TASK_PATTERN
        return self._compiled_task_regex

    def detect_task(self, post: dict[str, Any]) -> dict[str, Any] | None:
        message = str(post.get("message", ""))

        # Accept task if it has the GEMINI-TASK pattern (with or without @mention)
        match = self._get_task_pattern().search(message)
        if not match:
            return None

        prompt = (match.group(1) if match.groups() else "").strip()
        if not prompt:
            prompt = message

        return {
            "name": "GEMINI-TASK",
            "prompt": prompt,
            "post_id": post.get("id", ""),
        }

    def execute_task(self, task_info: dict[str, Any]) -> str:
        prompt = str(task_info.get("prompt", "")).strip()
        if not prompt:
            return "[E-CLI-INPUT] Empty task prompt"

        # Gemini CLI requires prompt as argument, not via stdin
        cmd = [self.config.cli_cmd] + self.config.cli_args + [prompt]
        return self.execute_subprocess(cmd)

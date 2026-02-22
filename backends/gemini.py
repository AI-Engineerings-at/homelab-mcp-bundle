"""Gemini backend - Google Gemini CLI bridge."""

from __future__ import annotations

import re
from typing import Any

from ..base import BaseBridge

TASK_PATTERN = re.compile(r"##\s*GEMINI-TASK[:\s]*(.*)", re.IGNORECASE | re.DOTALL)


class GeminiBridge(BaseBridge):
    """Google Gemini CLI bridge for research and analysis tasks."""

    def detect_task(self, post: dict[str, Any]) -> dict[str, Any] | None:
        if not self.should_respond(post):
            return None

        message = str(post.get("message", ""))
        match = TASK_PATTERN.search(message)
        if not match:
            return None

        prompt = match.group(1).strip()
        return {
            "name": "GEMINI-TASK",
            "prompt": prompt,
            "post_id": post.get("id", ""),
        }

    def execute_task(self, task_info: dict[str, Any]) -> str:
        prompt = str(task_info.get("prompt", ""))
        # Gemini CLI requires prompt as argument to -p, not via stdin
        cmd = [self.config.cli_cmd, "-p", prompt]
        return self.execute_subprocess(cmd)

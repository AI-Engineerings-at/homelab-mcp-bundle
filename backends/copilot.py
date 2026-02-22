"""Copilot backend - GitHub Copilot CLI bridge."""

from __future__ import annotations

import os
import re
from typing import Any

from ..base import BaseBridge

TASK_PATTERN = re.compile(r"##\s*COPILOT-TASK[:\s]*(.*)", re.IGNORECASE | re.DOTALL)


class CopilotBridge(BaseBridge):
    """GitHub Copilot CLI bridge for coding tasks."""

    def detect_task(self, post: dict[str, Any]) -> dict[str, Any] | None:
        if not self.should_respond(post):
            return None

        message = str(post.get("message", ""))
        match = TASK_PATTERN.search(message)
        if not match:
            return None

        prompt = match.group(1).strip()
        return {
            "name": "COPILOT-TASK",
            "prompt": prompt,
            "post_id": post.get("id", ""),
            "mode": self._detect_mode(prompt),
        }

    @staticmethod
    def _detect_mode(prompt: str) -> str:
        explain_keywords = ["explain", "erklaer", "was macht", "what does", "how does"]
        prompt_lower = prompt.lower()
        if any(keyword in prompt_lower for keyword in explain_keywords):
            return "explain"
        return "suggest"

    def execute_task(self, task_info: dict[str, Any]) -> str:
        prompt = str(task_info.get("prompt", ""))
        mode = str(task_info.get("mode", "suggest")).lower()

        if mode == "explain":
            cmd = ["gh", "copilot", "explain", prompt]
        else:
            cmd = ["gh", "copilot", "suggest", "-t", "shell", prompt]

        return self.execute_subprocess(
            cmd,
            timeout=min(self.config.cli_timeout_seconds, 120),
            env={**os.environ, "GH_PROMPT": "disable"},
        )

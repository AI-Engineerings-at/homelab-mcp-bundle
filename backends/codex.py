"""Codex backend - monitor mode for CODEX task lifecycle."""

from __future__ import annotations

import re
from typing import Any

from ..base import BaseBridge

ECHO_LOG_BOT_ID = "rbuq48qpr7b6ff88cuiugaz7jh"
CODEX_ASSISTANT_ID = "eu93je3tujdqpewy8pqri9fqjo"
JIM_USER_ID = "69uf4ng7n7rf3x578phspc1jyo"

TASK_PATTERN = re.compile(r"##\s*CODEX-TASK-R(\d+)", re.IGNORECASE)
COMPLETION_KEYWORDS = [
    "erledigt",
    "abgeschlossen",
    "completed",
    "done",
    "alle tests",
    "passed",
    "fertig",
]


class CodexBridge(BaseBridge):
    """Codex monitor bridge (no local CLI execution)."""

    def detect_task(self, post: dict[str, Any]) -> dict[str, Any] | None:
        user_id = str(post.get("user_id", ""))
        message = str(post.get("message", ""))

        if user_id not in {JIM_USER_ID, ECHO_LOG_BOT_ID}:
            return None

        match = TASK_PATTERN.search(message)
        if not match:
            return None

        round_num = int(match.group(1))
        return {
            "name": f"CODEX-TASK-R{round_num}",
            "round": round_num,
            "post_id": post.get("id", ""),
        }

    def detect_completion(self, post: dict[str, Any]) -> bool:
        user_id = str(post.get("user_id", ""))
        message = str(post.get("message", "")).lower()

        if user_id != CODEX_ASSISTANT_ID:
            return False
        return any(keyword in message for keyword in COMPLETION_KEYWORDS)

    def execute_task(self, task_info: dict[str, Any]) -> str:
        return f"CODEX-TASK-R{task_info.get('round', '?')} erkannt. Warte auf Codex-Output."

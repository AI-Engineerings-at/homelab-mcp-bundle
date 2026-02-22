"""CLI Bridge Framework - Modular CLI-to-Mattermost bridges.

Provides a pluggable system for connecting CLI tools (Codex, Copilot, Gemini,
Claude) to Mattermost channels. Each backend monitors a channel for mentions
and task patterns, then executes the appropriate CLI tool and posts results.

Usage:
    python -m cli_bridge --backend copilot
    python -m cli_bridge --backend gemini
    python -m cli_bridge --backend codex
    python -m cli_bridge --backend claude
"""

__version__ = "1.1.0"

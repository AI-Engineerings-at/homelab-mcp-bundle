"""Config loader for CLI Bridge."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml

from .base import BridgeConfig

DEFAULT_CONFIG = Path(__file__).parent.parent / "cli_bridge_config.yaml"
ENV_PATTERN = re.compile(r"\$\{(\w+)\}")


def _resolve_env(value: Any) -> Any:
    if isinstance(value, str):
        return ENV_PATTERN.sub(lambda m: os.getenv(m.group(1), ""), value)
    if isinstance(value, list):
        return [_resolve_env(item) for item in value]
    if isinstance(value, dict):
        return {key: _resolve_env(item) for key, item in value.items()}
    return value


def _as_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
    return default


def _as_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _parse_cli_args(value: Any) -> list[str]:
    """Parse cli_args safely - prevents string-to-character split bug."""
    if isinstance(value, list):
        return [str(x) for x in value]
    if isinstance(value, str):
        # Single string argument - wrap in list, don't split characters
        stripped = value.strip()
        return [stripped] if stripped else []
    return []


def _load_yaml(config_file: Path) -> dict[str, Any]:
    try:
        parsed = yaml.safe_load(config_file.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise RuntimeError(f"[E-CONFIG-PARSE] Could not parse {config_file}: {exc}") from exc

    if not isinstance(parsed, dict):
        raise RuntimeError(f"[E-CONFIG-TYPE] Expected object at root of {config_file}")
    return parsed


def load_config(backend: str, config_path: str | None = None) -> BridgeConfig:
    """Load bridge config from YAML file for a specific backend."""
    config_file = Path(config_path) if config_path else DEFAULT_CONFIG

    defaults: dict[str, Any] = {}
    bridge_cfg: dict[str, Any] = {}

    if config_file.exists():
        parsed = _load_yaml(config_file)
        defaults = parsed.get("defaults", {}) if isinstance(parsed.get("defaults"), dict) else {}
        bridges = parsed.get("bridges", {}) if isinstance(parsed.get("bridges"), dict) else {}
        bridge_cfg = bridges.get(backend, {}) if isinstance(bridges.get(backend), dict) else {}

    cfg = {**defaults, **bridge_cfg}
    cfg = _resolve_env(cfg)

    bot_token_env = str(cfg.get("bot_token_env", f"MM_{backend.upper()}_TOKEN"))
    bot_token_fallback_env = str(cfg.get("bot_token_fallback_env", "")).strip()
    monitor_token_env = str(cfg.get("monitor_token_env", "MM_JIM_TOKEN"))

    bot_token = os.getenv(bot_token_env, "")
    if not bot_token and bot_token_fallback_env:
        bot_token = os.getenv(bot_token_fallback_env, "")

    return BridgeConfig(
        backend_name=backend,
        bot_name=str(cfg.get("bot_name", backend)),
        channel_id=str(cfg.get("channel_id", "")).strip(),
        bot_token=bot_token,
        monitor_token=os.getenv(monitor_token_env, ""),
        mm_url=str(cfg.get("mm_url", "")).strip(),
        poll_interval=_as_int(cfg.get("poll_interval"), 30),
        cli_cmd=str(cfg.get("cli_cmd", "")).strip(),
        cli_args=_parse_cli_args(cfg.get("cli_args", [])),
        state_file=str(cfg.get("state_file", f".{backend}_bridge_state.json")),
        working_dir=str(cfg.get("working_dir", ".")),
        max_response_length=_as_int(cfg.get("max_response_length"), 3800),
        mode=str(cfg.get("mode", "execute")).strip().lower(),
        respond_to_mentions=_as_bool(cfg.get("respond_to_mentions"), default=True),
        task_prefix=str(cfg.get("task_prefix", "")),
        task_regex=str(cfg.get("task_regex", "")),
        cli_timeout_seconds=_as_int(cfg.get("cli_timeout_seconds"), 300),
        mm_per_page=_as_int(cfg.get("mm_per_page"), 100),
        mm_max_pages=_as_int(cfg.get("mm_max_pages"), 5),
        retry_max_attempts=_as_int(cfg.get("retry_max_attempts"), 3),
        retry_base_seconds=_as_float(cfg.get("retry_base_seconds"), 1.0),
        heartbeat_file=str(cfg.get("heartbeat_file", f".{backend}_bridge_heartbeat.json")),
    )

"""CLI Bridge launcher."""

from __future__ import annotations

import argparse
import sys

from .config import load_config

BACKENDS = {
    "codex": "cli_bridge.backends.codex:CodexBridge",
    "copilot": "cli_bridge.backends.copilot:CopilotBridge",
    "gemini": "cli_bridge.backends.gemini:GeminiBridge",
    "claude": "cli_bridge.backends.claude:ClaudeBridge",
    "lisa01": "cli_bridge.backends.claude:ClaudeBridge",
}


def get_bridge_class(backend: str):
    """Import and return the bridge class for a backend."""
    if backend == "codex":
        from .backends.codex import CodexBridge

        return CodexBridge
    if backend == "copilot":
        from .backends.copilot import CopilotBridge

        return CopilotBridge
    if backend == "gemini":
        from .backends.gemini import GeminiBridge

        return GeminiBridge
    if backend == "claude":
        from .backends.claude import ClaudeBridge

        return ClaudeBridge

    if backend == "lisa01":
        from .backends.claude import ClaudeBridge

        return ClaudeBridge

    raise ValueError(f"Unknown backend: {backend}. Available: {list(BACKENDS.keys())}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CLI Bridge - Modular CLI-to-Mattermost bridges",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m cli_bridge --backend copilot
  python -m cli_bridge --backend gemini
  python -m cli_bridge --backend codex
  python -m cli_bridge --backend claude
  python -m cli_bridge --backend claude --dry-run
  python -m cli_bridge --backend claude --once
        """,
    )
    parser.add_argument(
        "--backend",
        "-b",
        required=True,
        choices=list(BACKENDS.keys()),
        help="Which CLI backend to run",
    )
    parser.add_argument(
        "--config",
        "-c",
        default=None,
        help="Path to config YAML (default: scripts/cli_bridge_config.yaml)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Test config and connection, then exit",
    )
    parser.add_argument(
        "--interval",
        "-i",
        type=int,
        default=None,
        help="Override poll interval (seconds)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one poll cycle and exit (smoke mode)",
    )

    args = parser.parse_args()

    try:
        config = load_config(args.backend, args.config)
    except Exception as exc:
        print(f"[E-CONFIG-LOAD] Failed to load config: {exc}")
        return 1

    if args.interval:
        config.poll_interval = args.interval

    BridgeClass = get_bridge_class(args.backend)
    bridge = BridgeClass(config)

    config_errors = bridge.validate_config()

    if args.dry_run:
        print(f"DRY RUN - Testing @{config.bot_name} bridge config...")
        print(f"  Backend:    {config.backend_name}")
        print(f"  MM URL:     {config.mm_url}")
        print(f"  Channel:    {config.channel_id or '(missing)'}")
        print(f"  CLI:        {config.cli_cmd or '(monitor)'}")
        print(f"  Mode:       {config.mode}")
        print(f"  Bot token:  {'set' if config.bot_token else 'MISSING'}")
        print(f"  Monitor:    {'set' if config.monitor_token else 'MISSING'}")
        print(f"  Mentions:   {config.respond_to_mentions}")

        if config_errors:
            print("  Config errors:")
            for item in config_errors:
                print(f"    - {item}")

        if config.monitor_token:
            try:
                me = bridge.mm_get("/users/me")
                print(f"  MM conn:    OK (@{me.get('username', '?')})")
            except Exception as exc:
                print(f"  MM conn:    FAILED ({exc})")

        bridge.show_status()
        print("Dry run complete.")
        return 1 if config_errors else 0

    if config_errors:
        print("Config validation failed:")
        for item in config_errors:
            print(f"  - {item}")
        return 1

    try:
        return bridge.run(once=args.once)
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

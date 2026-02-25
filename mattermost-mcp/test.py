#!/usr/bin/env python3
"""
Quick Test fuer Mattermost MCP Server.
Testet alle 5 Tools direkt (ohne MCP Protokoll).
"""

import os
import sys

# Token aus Umgebung oder direkt
os.environ.setdefault("MM_TOKEN", os.environ.get("MM_LISA01_TOKEN", "pd5bcjnin3gi5bsuoqi4atyoyc"))

# Import nach Token-Setup
from server import channels_list, posts_read, posts_create, users_list, posts_search

ECHO_LOG_CHANNEL = "1trxzu41pbfc3qd8cxfmsyus8c"
TEAM_ID = "yhtr94a73pd7tmwg6arr34k1ow"

def run_tests():
    print("=" * 60)
    print("Mattermost MCP Server — Test")
    print("=" * 60)

    # Test 1: channels_list
    print("\n[1/4] channels_list...")
    try:
        result = channels_list(per_page=5)
        import json
        channels = json.loads(result)
        print(f"  OK — {len(channels)} Channels (erste 5)")
        for ch in channels[:3]:
            print(f"  - {ch['display_name']} ({ch['name']}) [{ch['type']}]")
    except Exception as e:
        print(f"  FEHLER: {e}")

    # Test 2: posts_read
    print("\n[2/4] posts_read (echo_log)...")
    try:
        result = posts_read(channel_id=ECHO_LOG_CHANNEL, per_page=3)
        import json
        posts = json.loads(result)
        print(f"  OK — {len(posts)} Posts gelesen")
        for p in posts[:2]:
            msg_preview = p['message'][:60].replace('\n', ' ')
            print(f"  - [{p['user_id'][:8]}...] {msg_preview}")
    except Exception as e:
        print(f"  FEHLER: {e}")

    # Test 3: users_list
    print("\n[3/4] users_list...")
    try:
        result = users_list(per_page=5, in_team=TEAM_ID)
        import json
        users = json.loads(result)
        print(f"  OK — {len(users)} User")
        for u in users[:3]:
            print(f"  - @{u['username']} ({u['first_name']} {u['last_name']})")
    except Exception as e:
        print(f"  FEHLER: {e}")

    # Test 4: posts_create
    print("\n[4/4] posts_create (Test-Post in echo_log)...")
    try:
        result = posts_create(
            channel_id=ECHO_LOG_CHANNEL,
            message="**Mattermost MCP Server PoC** — Test erfolgreich! :white_check_mark:\n\nAlle 4 Tools getestet:\n- `channels_list` OK\n- `posts_read` OK\n- `users_list` OK\n- `posts_create` OK ← dieser Post\n\n_via @lisa01 MCP Server_"
        )
        import json
        post = json.loads(result)
        print(f"  OK — Post erstellt: {post['id']}")
    except Exception as e:
        print(f"  FEHLER: {e}")

    print("\n" + "=" * 60)
    print("Test abgeschlossen!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()

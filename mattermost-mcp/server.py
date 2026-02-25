#!/usr/bin/env python3
"""
Mattermost MCP Server — PoC
Ermoeglicht AI-Agents Zugriff auf Mattermost via Model Context Protocol.

Features:
- channels/list   — Alle Channels auflisten
- posts/read      — Posts lesen (mit Pagination)
- posts/create    — Neue Posts schreiben
- users/list      — User auflisten
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Any
from mcp.server.fastmcp import FastMCP

# Konfiguration
MM_BASE_URL = os.environ.get("MM_BASE_URL", "http://your-mattermost-host:8065/api/v4")
MM_TOKEN = os.environ.get("MM_TOKEN", "")
MM_TEAM_ID = os.environ.get("MM_TEAM_ID", "yhtr94a73pd7tmwg6arr34k1ow")

mcp = FastMCP("mattermost-mcp")


def mm_request(method: str, path: str, data: dict = None) -> Any:
    """HTTP Request an Mattermost API."""
    if not MM_TOKEN:
        raise ValueError("MM_TOKEN nicht gesetzt. Bitte MM_TOKEN Umgebungsvariable setzen.")

    url = f"{MM_BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {MM_TOKEN}",
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise RuntimeError(f"MM API Fehler {e.code}: {error_body}")


@mcp.tool()
def channels_list(team_id: str = None, per_page: int = 50, page: int = 0) -> str:
    """
    Listet alle Channels im Team auf.

    Args:
        team_id: Team-ID (Standard: konfiguriertes Team)
        per_page: Anzahl Channels pro Seite (max 200)
        page: Seite (ab 0)

    Returns:
        JSON-Liste der Channels mit id, name, display_name, type, purpose
    """
    tid = team_id or MM_TEAM_ID
    path = f"/teams/{tid}/channels?per_page={per_page}&page={page}"
    channels = mm_request("GET", path)

    result = []
    for ch in channels:
        result.append({
            "id": ch.get("id"),
            "name": ch.get("name"),
            "display_name": ch.get("display_name"),
            "type": ch.get("type"),  # O=public, P=private, D=direct, G=group
            "purpose": ch.get("purpose", ""),
            "header": ch.get("header", ""),
        })

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def posts_read(channel_id: str, per_page: int = 20, page: int = 0) -> str:
    """
    Liest Posts aus einem Channel.

    Args:
        channel_id: Channel-ID
        per_page: Anzahl Posts pro Seite (max 200)
        page: Seite (ab 0)

    Returns:
        JSON-Liste der Posts (sortiert nach Zeit, neueste zuerst)
    """
    path = f"/channels/{channel_id}/posts?per_page={per_page}&page={page}"
    resp = mm_request("GET", path)

    order = resp.get("order", [])
    posts_map = resp.get("posts", {})

    result = []
    for post_id in order:
        post = posts_map.get(post_id, {})
        result.append({
            "id": post.get("id"),
            "create_at": post.get("create_at"),
            "user_id": post.get("user_id"),
            "channel_id": post.get("channel_id"),
            "message": post.get("message"),
            "type": post.get("type", ""),
            "props": post.get("props", {}),
        })

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def posts_create(channel_id: str, message: str, reply_to_post_id: str = None) -> str:
    """
    Erstellt einen neuen Post in einem Channel.

    Args:
        channel_id: Ziel-Channel-ID
        message: Nachrichtentext (Markdown wird unterstuetzt)
        reply_to_post_id: Optional — Post-ID auf die geantwortet wird (Thread)

    Returns:
        JSON des erstellten Posts
    """
    data = {
        "channel_id": channel_id,
        "message": message,
    }
    if reply_to_post_id:
        data["root_id"] = reply_to_post_id

    post = mm_request("POST", "/posts", data)

    return json.dumps({
        "id": post.get("id"),
        "create_at": post.get("create_at"),
        "channel_id": post.get("channel_id"),
        "message": post.get("message"),
        "status": "created",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def users_list(per_page: int = 50, page: int = 0, in_team: str = None) -> str:
    """
    Listet User auf.

    Args:
        per_page: Anzahl User pro Seite (max 200)
        page: Seite (ab 0)
        in_team: Optional — nur User dieses Teams (Team-ID)

    Returns:
        JSON-Liste der User mit id, username, email, roles, status
    """
    if in_team:
        path = f"/users?per_page={per_page}&page={page}&in_team={in_team}"
    else:
        path = f"/users?per_page={per_page}&page={page}"

    users = mm_request("GET", path)

    result = []
    for u in users:
        result.append({
            "id": u.get("id"),
            "username": u.get("username"),
            "email": u.get("email"),
            "first_name": u.get("first_name", ""),
            "last_name": u.get("last_name", ""),
            "nickname": u.get("nickname", ""),
            "roles": u.get("roles", ""),
        })

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def posts_search(team_id: str, terms: str, is_or_search: bool = False) -> str:
    """
    Sucht Posts im Team nach Stichworten.

    Args:
        team_id: Team-ID
        terms: Suchbegriffe (Leerzeichen = AND, OR-Operator moeglich)
        is_or_search: True = OR-Suche, False = AND-Suche

    Returns:
        JSON-Liste der gefundenen Posts
    """
    tid = team_id or MM_TEAM_ID
    data = {
        "terms": terms,
        "is_or_search": is_or_search,
    }
    resp = mm_request("POST", f"/teams/{tid}/posts/search", data)

    order = resp.get("order", [])
    posts_map = resp.get("posts", {})

    result = []
    for post_id in order:
        post = posts_map.get(post_id, {})
        result.append({
            "id": post.get("id"),
            "create_at": post.get("create_at"),
            "user_id": post.get("user_id"),
            "channel_id": post.get("channel_id"),
            "message": post.get("message"),
        })

    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys

    if not MM_TOKEN:
        print("FEHLER: MM_TOKEN Umgebungsvariable nicht gesetzt!", file=sys.stderr)
        print("Beispiel: export MM_TOKEN=pd5bcjnin3gi5bsuoqi4atyoyc", file=sys.stderr)
        sys.exit(1)

    print(f"Mattermost MCP Server startet...", file=sys.stderr)
    print(f"Base URL: {MM_BASE_URL}", file=sys.stderr)
    print(f"Team ID: {MM_TEAM_ID}", file=sys.stderr)
    mcp.run()

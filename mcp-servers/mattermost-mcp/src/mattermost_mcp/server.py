"""
Mattermost MCP Server
Mattermost REST API v4 via Model Context Protocol

Tools:
  - list_channels      List all channels in a team
  - read_channel       Read recent posts from a channel
  - post_message       Post a message to a channel
  - list_users         List all users in the team
  - get_mentions       Get posts that mention a specific user
  - search_posts       Search for posts by keyword
  - get_channel_info   Get metadata for a channel (by name or ID)
"""

import asyncio
import json
import os
import sys
from typing import Any

import httpx

# MCP SDK imports
sys.path.insert(0, "/home/joe/.local/lib/python3.14/site-packages")
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types


# ── Config from environment ────────────────────────────────────────────────────
MM_BASE_URL = os.environ.get("MM_BASE_URL", "http://10.40.10.83:8065")
MM_TOKEN    = os.environ.get("MM_TOKEN", "")
MM_TEAM_ID  = os.environ.get("MM_TEAM_ID", "yhtr94a73pd7tmwg6arr34k1ow")


# ── Mattermost API helper ──────────────────────────────────────────────────────
class MattermostClient:
    def __init__(self, base_url: str, token: str, team_id: str):
        self.base = base_url.rstrip("/") + "/api/v4"
        self.team_id = team_id
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    async def _get(self, path: str, params: dict | None = None) -> Any:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base}{path}", headers=self.headers, params=params or {})
            r.raise_for_status()
            return r.json()

    async def _post(self, path: str, body: dict) -> Any:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f"{self.base}{path}", headers=self.headers, json=body)
            r.raise_for_status()
            return r.json()

    # ── Public methods ─────────────────────────────────────────────────────────
    async def list_channels(self, per_page: int = 50) -> list[dict]:
        """List all public channels in the configured team."""
        return await self._get(
            f"/teams/{self.team_id}/channels",
            {"per_page": per_page, "page": 0},
        )

    async def get_channel_by_name(self, name: str) -> dict:
        """Get channel metadata by name (slug)."""
        return await self._get(f"/teams/{self.team_id}/channels/name/{name}")

    async def read_channel(self, channel_id: str, per_page: int = 20) -> dict:
        """Fetch the most recent posts from a channel."""
        return await self._get(
            f"/channels/{channel_id}/posts",
            {"per_page": per_page},
        )

    async def post_message(self, channel_id: str, message: str, root_id: str = "") -> dict:
        """Post a message (optionally as a thread reply)."""
        body: dict = {"channel_id": channel_id, "message": message}
        if root_id:
            body["root_id"] = root_id
        return await self._post("/posts", body)

    async def list_users(self, per_page: int = 50) -> list[dict]:
        """List users in the team."""
        return await self._get(
            f"/users",
            {"per_page": per_page, "in_team": self.team_id},
        )

    async def search_posts(self, terms: str, is_or: bool = False) -> dict:
        """Full-text search across the team."""
        return await self._post(
            f"/teams/{self.team_id}/posts/search",
            {"terms": terms, "is_or_search": is_or},
        )

    async def get_mentions(self, username: str, per_page: int = 20) -> dict:
        """Search for posts that mention @username."""
        return await self.search_posts(f"@{username}")


# ── MCP Server ─────────────────────────────────────────────────────────────────
server = Server("mattermost-mcp")
mm = MattermostClient(MM_BASE_URL, MM_TOKEN, MM_TEAM_ID)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_channels",
            description="List all public channels in the Mattermost team.",
            inputSchema={
                "type": "object",
                "properties": {
                    "per_page": {"type": "integer", "description": "Max channels to return (default 50)", "default": 50}
                },
            },
        ),
        types.Tool(
            name="get_channel_info",
            description="Get metadata for a channel by its name (slug) or ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel_name": {"type": "string", "description": "Channel slug, e.g. 'echo_log' (use this OR channel_id)"},
                    "channel_id":   {"type": "string", "description": "Channel ID (use this OR channel_name)"},
                },
            },
        ),
        types.Tool(
            name="read_channel",
            description="Read the most recent posts from a channel.",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel_id":   {"type": "string", "description": "Channel ID"},
                    "channel_name": {"type": "string", "description": "Channel name/slug (alternative to channel_id)"},
                    "per_page":     {"type": "integer", "description": "Number of posts to fetch (default 20)", "default": 20},
                },
            },
        ),
        types.Tool(
            name="post_message",
            description="Post a message to a Mattermost channel.",
            inputSchema={
                "type": "object",
                "required": ["channel_id", "message"],
                "properties": {
                    "channel_id": {"type": "string", "description": "Channel ID to post into"},
                    "message":    {"type": "string", "description": "Message text (Markdown supported)"},
                    "root_id":    {"type": "string", "description": "Post ID to reply to (optional, for threads)"},
                },
            },
        ),
        types.Tool(
            name="list_users",
            description="List users in the Mattermost team.",
            inputSchema={
                "type": "object",
                "properties": {
                    "per_page": {"type": "integer", "description": "Max users to return (default 50)", "default": 50}
                },
            },
        ),
        types.Tool(
            name="get_mentions",
            description="Get recent posts that mention a specific user (@username).",
            inputSchema={
                "type": "object",
                "required": ["username"],
                "properties": {
                    "username": {"type": "string", "description": "Username WITHOUT the @ sign"},
                },
            },
        ),
        types.Tool(
            name="search_posts",
            description="Full-text search across all posts in the team.",
            inputSchema={
                "type": "object",
                "required": ["terms"],
                "properties": {
                    "terms":  {"type": "string", "description": "Search keywords or phrases"},
                    "is_or":  {"type": "boolean", "description": "If true, match any term (OR); default is AND", "default": False},
                },
            },
        ),
    ]


# ── Tool call dispatcher ────────────────────────────────────────────────────────
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    args = arguments or {}

    try:
        if name == "list_channels":
            data = await mm.list_channels(per_page=args.get("per_page", 50))
            summary = [{"id": c["id"], "name": c["name"], "display_name": c["display_name"],
                        "type": c["type"], "purpose": c.get("purpose", "")} for c in data]
            text = json.dumps(summary, indent=2, ensure_ascii=False)

        elif name == "get_channel_info":
            if args.get("channel_id"):
                data = await mm._get(f"/channels/{args['channel_id']}")
            elif args.get("channel_name"):
                data = await mm.get_channel_by_name(args["channel_name"])
            else:
                raise ValueError("Provide either channel_id or channel_name")
            text = json.dumps({
                "id": data["id"], "name": data["name"],
                "display_name": data["display_name"],
                "type": data["type"], "purpose": data.get("purpose", ""),
                "header": data.get("header", ""),
            }, indent=2, ensure_ascii=False)

        elif name == "read_channel":
            # Resolve channel name → ID if needed
            channel_id = args.get("channel_id")
            if not channel_id and args.get("channel_name"):
                ch = await mm.get_channel_by_name(args["channel_name"])
                channel_id = ch["id"]
            if not channel_id:
                raise ValueError("Provide either channel_id or channel_name")

            data = await mm.read_channel(channel_id, per_page=args.get("per_page", 20))
            order = data.get("order", [])
            posts = data.get("posts", {})
            messages = []
            for pid in order:
                p = posts.get(pid, {})
                messages.append({
                    "id": p.get("id"),
                    "user_id": p.get("user_id"),
                    "create_at": p.get("create_at"),
                    "message": p.get("message", ""),
                })
            text = json.dumps(messages, indent=2, ensure_ascii=False)

        elif name == "post_message":
            data = await mm.post_message(
                args["channel_id"],
                args["message"],
                root_id=args.get("root_id", ""),
            )
            text = json.dumps({"post_id": data["id"], "status": "sent"}, indent=2)

        elif name == "list_users":
            data = await mm.list_users(per_page=args.get("per_page", 50))
            summary = [{"id": u["id"], "username": u["username"],
                        "first_name": u.get("first_name", ""),
                        "last_name": u.get("last_name", ""),
                        "email": u.get("email", "")} for u in data]
            text = json.dumps(summary, indent=2, ensure_ascii=False)

        elif name == "get_mentions":
            data = await mm.get_mentions(args["username"])
            order = data.get("order", [])
            posts = data.get("posts", {})
            results = [{"id": posts[p]["id"], "user_id": posts[p]["user_id"],
                        "message": posts[p]["message"]} for p in order if p in posts]
            text = json.dumps(results, indent=2, ensure_ascii=False)

        elif name == "search_posts":
            data = await mm.search_posts(args["terms"], is_or=args.get("is_or", False))
            order = data.get("order", [])
            posts = data.get("posts", {})
            results = [{"id": posts[p]["id"], "user_id": posts[p]["user_id"],
                        "channel_id": posts[p]["channel_id"],
                        "message": posts[p]["message"]} for p in order if p in posts]
            text = json.dumps(results, indent=2, ensure_ascii=False)

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as exc:
        text = json.dumps({"error": str(exc)}, indent=2)

    return [types.TextContent(type="text", text=text)]


# ── Entry point ─────────────────────────────────────────────────────────────────
async def main():
    if not MM_TOKEN:
        print("ERROR: MM_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mattermost-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

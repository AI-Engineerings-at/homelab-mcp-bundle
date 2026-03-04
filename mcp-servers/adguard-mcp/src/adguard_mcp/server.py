"""
AdGuard Home MCP Server
DNS filtering and ad-blocking management via AdGuard Home REST API and Model Context Protocol

Tools:
  - status            Server status, version, protection state, DNS port
  - stats             DNS query statistics (24h: total, blocked, upstream latency)
  - querylog          Recent DNS queries with client, domain, reason, answer
  - filtering_status  Filter lists with rule counts and enabled/disabled state
  - toggle_protection Enable or disable DNS protection globally
  - add_custom_rule   Add a custom filtering rule (e.g. block or allowlist a domain)
  - remove_custom_rule Remove a custom filtering rule
  - filtering_refresh Trigger a refresh of all enabled filter lists
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
ADGUARD_URL      = os.environ.get("ADGUARD_URL", "http://10.40.10.80:3053")
ADGUARD_USER     = os.environ.get("ADGUARD_USER", "admin")
ADGUARD_PASSWORD = os.environ.get("ADGUARD_PASSWORD", "")


# ── AdGuard Home API client ────────────────────────────────────────────────────
class AdGuardClient:
    def __init__(self):
        self.base = ADGUARD_URL.rstrip("/") + "/control"
        self._auth = (ADGUARD_USER, ADGUARD_PASSWORD)

    async def _get(self, path: str, params: dict | None = None) -> Any:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"{self.base}{path}",
                auth=self._auth,
                params=params or {},
            )
            r.raise_for_status()
            return r.json() if r.content else {}

    async def _post(self, path: str, body: Any = None, json_body: bool = True) -> Any:
        async with httpx.AsyncClient(timeout=15) as client:
            kwargs: dict = {"auth": self._auth}
            if json_body:
                kwargs["json"] = body if body is not None else {}
            else:
                kwargs["data"] = body or {}
            r = await client.post(f"{self.base}{path}", **kwargs)
            r.raise_for_status()
            return r.json() if r.content else {}

    async def status(self) -> dict:
        return await self._get("/status")

    async def stats(self) -> dict:
        return await self._get("/stats")

    async def querylog(self, limit: int = 50, offset: int = 0, search: str = "") -> dict:
        params: dict = {"limit": limit, "offset": offset}
        if search:
            params["search"] = search
        return await self._get("/querylog", params)

    async def filtering_status(self) -> dict:
        return await self._get("/filtering/status")

    async def toggle_protection(self, enabled: bool) -> dict:
        return await self._post("/dns_config", {"protection_enabled": enabled})

    async def get_custom_rules(self) -> list[str]:
        data = await self._get("/filtering/status")
        return data.get("user_rules", [])

    async def set_custom_rules(self, rules: list[str]) -> dict:
        return await self._post("/filtering/set_rules", {"rules": rules})

    async def filtering_refresh(self, whitelist: bool = False) -> dict:
        return await self._post("/filtering/refresh", {"whitelist": whitelist})


# ── MCP Server ─────────────────────────────────────────────────────────────────
server = Server("adguard-mcp")
adguard = AdGuardClient()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="status",
            description=(
                "Get AdGuard Home server status. "
                "Returns version, DNS port, HTTP port, protection state (enabled/disabled), "
                "and whether DHCP is available. "
                "Use this to quickly check if AdGuard is running and protecting."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="stats",
            description=(
                "Get AdGuard Home DNS statistics for the last 24 hours. "
                "Returns total DNS queries, blocked queries, blocked percentage, "
                "average response time, and top queried/blocked domains. "
                "Use this to understand traffic patterns and blocking effectiveness."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="querylog",
            description=(
                "Fetch recent DNS query log entries from AdGuard Home. "
                "Shows client IP, queried domain, query type, result (blocked/allowed/cached), "
                "upstream DNS used, and response time. "
                "Optionally filter by domain or client search term."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of entries to return (default: 50, max: 1000)",
                        "default": 50,
                    },
                    "search": {
                        "type": "string",
                        "description": "Filter by domain name or client IP (optional)",
                    },
                },
            },
        ),
        types.Tool(
            name="filtering_status",
            description=(
                "List all AdGuard Home filter lists with their status. "
                "Returns filter name, URL, rule count, enabled state, and last update time. "
                "Also shows current custom user rules."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="toggle_protection",
            description=(
                "Enable or disable AdGuard Home DNS protection globally. "
                "When disabled, all DNS queries pass through unfiltered. "
                "WARNING: Disabling protection affects all clients on the network immediately."
            ),
            inputSchema={
                "type": "object",
                "required": ["enabled"],
                "properties": {
                    "enabled": {
                        "type": "boolean",
                        "description": "true to enable protection, false to disable",
                    },
                },
            },
        ),
        types.Tool(
            name="add_custom_rule",
            description=(
                "Add a custom DNS filtering rule to AdGuard Home. "
                "Supports AdGuard/hosts format rules:\n"
                "  Block domain:    ||example.com^\n"
                "  Allowlist:       @@||example.com^\n"
                "  Hosts redirect:  127.0.0.1 example.com\n"
                "Use this to quickly block or whitelist specific domains."
            ),
            inputSchema={
                "type": "object",
                "required": ["rule"],
                "properties": {
                    "rule": {
                        "type": "string",
                        "description": "The filtering rule to add (e.g. '||ads.example.com^' or '@@||safe.example.com^')",
                    },
                },
            },
        ),
        types.Tool(
            name="remove_custom_rule",
            description=(
                "Remove a custom DNS filtering rule from AdGuard Home. "
                "The rule must match exactly as it was added. "
                "Use filtering_status to see current custom rules."
            ),
            inputSchema={
                "type": "object",
                "required": ["rule"],
                "properties": {
                    "rule": {
                        "type": "string",
                        "description": "The exact filtering rule to remove",
                    },
                },
            },
        ),
        types.Tool(
            name="filtering_refresh",
            description=(
                "Trigger an immediate refresh of all enabled AdGuard Home filter lists. "
                "Forces AdGuard to re-download and apply all filter list updates. "
                "Use this after adding new filter lists or to get the latest block rules."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


# ── Tool dispatcher ─────────────────────────────────────────────────────────────
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    args = arguments or {}

    try:
        if name == "status":
            data = await adguard.status()
            result = {
                "version": data.get("version"),
                "dns_port": data.get("dns_port"),
                "http_port": data.get("http_port"),
                "protection_enabled": data.get("protection_enabled"),
                "dhcp_available": data.get("dhcp_available"),
                "running": data.get("running"),
            }
            text = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "stats":
            data = await adguard.stats()
            total = data.get("num_dns_queries", 0)
            blocked = data.get("num_blocked_filtering", 0)
            blocked_pct = round((blocked / total * 100), 1) if total > 0 else 0
            result = {
                "total_queries_24h": total,
                "blocked_queries": blocked,
                "blocked_percentage": f"{blocked_pct}%",
                "blocked_safebrowsing": data.get("num_replaced_safebrowsing", 0),
                "blocked_parental": data.get("num_replaced_parental", 0),
                "avg_processing_ms": round(data.get("avg_processing_time", 0) * 1000, 2),
                "top_queried_domains": data.get("top_queried_domains", [])[:10],
                "top_blocked_domains": data.get("top_blocked_domains", [])[:10],
                "top_clients": data.get("top_clients", [])[:10],
            }
            text = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "querylog":
            data = await adguard.querylog(
                limit=args.get("limit", 50),
                search=args.get("search", ""),
            )
            entries = []
            for entry in data.get("data", []):
                q = entry.get("question", {})
                ans = entry.get("answer", [])
                entries.append({
                    "time": entry.get("time", "")[:19].replace("T", " "),
                    "client": entry.get("client", ""),
                    "domain": q.get("name", ""),
                    "type": q.get("type", ""),
                    "reason": entry.get("reason", ""),
                    "cached": entry.get("cached", False),
                    "elapsed_ms": round(float(entry.get("elapsedMs", 0)), 2),
                    "upstream": entry.get("upstream", ""),
                    "answer": [
                        f"{a.get('type', '')} {a.get('value', '')}"
                        for a in ans[:3]
                    ],
                })
            text = json.dumps({
                "count": len(entries),
                "entries": entries,
            }, indent=2, ensure_ascii=False)

        elif name == "filtering_status":
            data = await adguard.filtering_status()
            filters = [
                {
                    "id": f.get("id"),
                    "name": f.get("name"),
                    "enabled": f.get("enabled"),
                    "rules_count": f.get("rules_count", 0),
                    "last_updated": f.get("last_updated", "")[:19].replace("T", " ") if f.get("last_updated") else "",
                    "url": f.get("url"),
                }
                for f in data.get("filters", [])
            ]
            result = {
                "filtering_enabled": data.get("enabled", False),
                "filter_count": len(filters),
                "filters": filters,
                "custom_rules": data.get("user_rules", []),
                "custom_rules_count": len(data.get("user_rules", [])),
            }
            text = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "toggle_protection":
            enabled = args["enabled"]
            await adguard.toggle_protection(enabled)
            text = json.dumps({
                "status": "ok",
                "protection_enabled": enabled,
                "message": f"DNS protection {'enabled' if enabled else 'disabled'}",
            }, indent=2)

        elif name == "add_custom_rule":
            rule = args["rule"].strip()
            current_rules = await adguard.get_custom_rules()
            if rule in current_rules:
                text = json.dumps({
                    "status": "already_exists",
                    "rule": rule,
                    "message": "Rule already present in custom rules",
                }, indent=2)
            else:
                new_rules = current_rules + [rule]
                await adguard.set_custom_rules(new_rules)
                text = json.dumps({
                    "status": "added",
                    "rule": rule,
                    "total_custom_rules": len(new_rules),
                }, indent=2)

        elif name == "remove_custom_rule":
            rule = args["rule"].strip()
            current_rules = await adguard.get_custom_rules()
            if rule not in current_rules:
                text = json.dumps({
                    "status": "not_found",
                    "rule": rule,
                    "message": "Rule not found in custom rules",
                }, indent=2)
            else:
                new_rules = [r for r in current_rules if r != rule]
                await adguard.set_custom_rules(new_rules)
                text = json.dumps({
                    "status": "removed",
                    "rule": rule,
                    "total_custom_rules": len(new_rules),
                }, indent=2)

        elif name == "filtering_refresh":
            await adguard.filtering_refresh()
            text = json.dumps({
                "status": "ok",
                "message": "Filter lists refresh triggered",
            }, indent=2)

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as exc:
        text = json.dumps({"error": str(exc)}, indent=2)

    return [types.TextContent(type="text", text=text)]


# ── Entry point ─────────────────────────────────────────────────────────────────
async def main():
    if not ADGUARD_PASSWORD:
        print(
            "ERROR: Set ADGUARD_PASSWORD environment variable",
            file=sys.stderr,
        )
        sys.exit(1)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="adguard-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

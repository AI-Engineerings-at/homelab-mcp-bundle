"""
Uptime Kuma MCP Server
Uptime Kuma monitoring data via Model Context Protocol

Tools:
  - list_monitors      List all monitors with current status, response time, type
  - get_monitors_down  Show only monitors that are currently DOWN or in error
  - get_monitor        Get details for a specific monitor by name
  - get_summary        Get overall health summary (UP/DOWN counts, incidents)
  - list_status_pages  List public status pages
"""

import asyncio
import json
import os
import re
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
KUMA_BASE_URL = os.environ.get("KUMA_BASE_URL", "http://10.40.10.80:3001")
KUMA_USERNAME = os.environ.get("KUMA_USERNAME", "joe")
KUMA_PASSWORD = os.environ.get("KUMA_PASSWORD", "")


# ── Status codes ───────────────────────────────────────────────────────────────
STATUS_LABELS = {1: "UP", 0: "DOWN", 2: "PENDING", 3: "MAINTENANCE"}


# ── Uptime Kuma client ─────────────────────────────────────────────────────────
class UptimeKumaClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password

    def _auth(self) -> tuple[str, str]:
        return (self.username, self.password)

    async def get_metrics_raw(self) -> str:
        """Fetch raw Prometheus metrics from /metrics endpoint."""
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"{self.base_url}/metrics",
                auth=self._auth(),
            )
            r.raise_for_status()
            return r.text

    async def get_monitors(self) -> list[dict]:
        """Parse Prometheus metrics into structured monitor list."""
        raw = await self.get_metrics_raw()
        monitors: dict[str, dict] = {}

        # Parse monitor_status
        for line in raw.splitlines():
            if line.startswith("#") or not line.strip():
                continue

            # Extract metric name and labels
            m = re.match(
                r'^(\w+)\{([^}]*)\}\s+([-\d.]+)$', line
            )
            if not m:
                continue

            metric_name = m.group(1)
            labels_str = m.group(2)
            value = float(m.group(3))

            # Parse labels
            labels: dict[str, str] = {}
            for label_m in re.finditer(r'(\w+)="([^"]*)"', labels_str):
                labels[label_m.group(1)] = label_m.group(2)

            name = labels.get("monitor_name", "")
            if not name:
                continue

            if name not in monitors:
                monitors[name] = {
                    "name": name,
                    "type": labels.get("monitor_type", "unknown"),
                    "url": labels.get("monitor_url") if labels.get("monitor_url") != "null" else None,
                    "hostname": labels.get("monitor_hostname") if labels.get("monitor_hostname") != "null" else None,
                    "port": labels.get("monitor_port") if labels.get("monitor_port") != "null" else None,
                    "status": None,
                    "status_label": None,
                    "response_time_ms": None,
                    "cert_days_remaining": None,
                    "cert_valid": None,
                }

            if metric_name == "monitor_status":
                monitors[name]["status"] = int(value)
                monitors[name]["status_label"] = STATUS_LABELS.get(int(value), "UNKNOWN")

            elif metric_name == "monitor_response_time" and value >= 0:
                monitors[name]["response_time_ms"] = value

            elif metric_name == "monitor_cert_days_remaining" and value > 0:
                monitors[name]["cert_days_remaining"] = int(value)

            elif metric_name == "monitor_cert_is_valid":
                monitors[name]["cert_valid"] = bool(int(value))

        return list(monitors.values())

    async def list_status_pages(self) -> list[dict]:
        """Fetch public status page list."""
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                f"{self.base_url}/api/status-page/list",
                auth=self._auth(),
            )
            r.raise_for_status()
            data = r.json()
            return data.get("statusPageList", data) if isinstance(data, dict) else data


# ── MCP Server ─────────────────────────────────────────────────────────────────
server = Server("uptime-kuma-mcp")
kuma = UptimeKumaClient(KUMA_BASE_URL, KUMA_USERNAME, KUMA_PASSWORD)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_summary",
            description=(
                "Get a quick health summary of all monitored services: "
                "total monitors, how many are UP/DOWN/PENDING, and which ones are down."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="list_monitors",
            description=(
                "List all Uptime Kuma monitors with their current status, type, "
                "response time and target URL/hostname. Excludes group monitors."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "type_filter": {
                        "type": "string",
                        "description": "Filter by monitor type: 'http', 'ping', 'port', 'tcp'. Omit for all.",
                        "enum": ["http", "ping", "port", "tcp"],
                    },
                },
            },
        ),
        types.Tool(
            name="get_monitors_down",
            description=(
                "Show ONLY monitors that are currently DOWN (status=0) or PENDING (status=2). "
                "Use this for quick incident detection."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="get_monitor",
            description=(
                "Get details for a specific monitor by name. "
                "Returns status, response time, cert info, and target."
            ),
            inputSchema={
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Exact monitor name (e.g. 'Grafana', 'pve', 'PostgreSQL')",
                    },
                },
            },
        ),
        types.Tool(
            name="list_status_pages",
            description=(
                "List all public status pages in Uptime Kuma with their slug and title. "
                "Use to find the public-facing status page URLs."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


# ── Tool dispatcher ─────────────────────────────────────────────────────────────
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    args = arguments or {}

    try:
        if name == "get_summary":
            monitors = await kuma.get_monitors()
            # Exclude groups
            real_monitors = [m for m in monitors if m["type"] != "group"]
            up = [m for m in real_monitors if m["status"] == 1]
            down = [m for m in real_monitors if m["status"] == 0]
            pending = [m for m in real_monitors if m["status"] == 2]
            maintenance = [m for m in real_monitors if m["status"] == 3]
            result = {
                "total": len(real_monitors),
                "up": len(up),
                "down": len(down),
                "pending": len(pending),
                "maintenance": len(maintenance),
                "health_percent": round(len(up) / max(len(real_monitors), 1) * 100, 1),
                "incidents": [
                    {"name": m["name"], "type": m["type"], "status": m["status_label"]}
                    for m in down + pending
                ],
            }
            text = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "list_monitors":
            monitors = await kuma.get_monitors()
            type_filter = args.get("type_filter")
            # Exclude groups, optionally filter by type
            result = [
                m for m in monitors
                if m["type"] != "group"
                and (type_filter is None or m["type"] == type_filter)
            ]
            # Sort: DOWN first, then by name
            result.sort(key=lambda m: (m.get("status", 1) != 0, m["name"]))
            text = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "get_monitors_down":
            monitors = await kuma.get_monitors()
            down = [
                m for m in monitors
                if m["type"] != "group" and m.get("status") in (0, 2)
            ]
            if not down:
                text = json.dumps({"status": "ALL_UP", "message": "All monitors are UP"}, indent=2)
            else:
                text = json.dumps(down, indent=2, ensure_ascii=False)

        elif name == "get_monitor":
            monitors = await kuma.get_monitors()
            search = args["name"].lower()
            # Exact match first, then fuzzy
            match = next(
                (m for m in monitors if m["name"].lower() == search),
                next((m for m in monitors if search in m["name"].lower()), None),
            )
            if match:
                text = json.dumps(match, indent=2, ensure_ascii=False)
            else:
                available = [m["name"] for m in monitors if m["type"] != "group"]
                text = json.dumps(
                    {"error": f"Monitor '{args['name']}' not found", "available": available},
                    indent=2, ensure_ascii=False,
                )

        elif name == "list_status_pages":
            pages = await kuma.list_status_pages()
            result = [
                {
                    "id": p.get("id"),
                    "title": p.get("title"),
                    "slug": p.get("slug"),
                    "url": f"{KUMA_BASE_URL}/status/{p.get('slug')}",
                    "published": p.get("published"),
                }
                for p in (pages if isinstance(pages, list) else [])
            ]
            text = json.dumps(result, indent=2, ensure_ascii=False)

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as exc:
        text = json.dumps({"error": str(exc)}, indent=2)

    return [types.TextContent(type="text", text=text)]


# ── Entry point ─────────────────────────────────────────────────────────────────
async def main():
    if not KUMA_PASSWORD:
        print("ERROR: KUMA_PASSWORD environment variable not set", file=sys.stderr)
        sys.exit(1)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="uptime-kuma-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Uptime Kuma MCP Server
Enables AI agents to monitor service status via Uptime Kuma's API.

Features:
- monitors/list    — List all monitors from a status page
- monitors/status  — Get current UP/DOWN status with latency
- status/overview  — Full dashboard overview (all monitors + stats)
"""

import os
import json
import urllib.request
from typing import Any
from mcp.server.fastmcp import FastMCP

# Configuration
KUMA_BASE_URL = os.environ.get("KUMA_BASE_URL", "http://your-uptime-kuma:3001")
KUMA_STATUS_PAGE = os.environ.get("KUMA_STATUS_PAGE", "homelab")

mcp = FastMCP("uptime-kuma-mcp")


def kuma_request(path: str) -> Any:
    """HTTP GET request to Uptime Kuma API."""
    url = f"{KUMA_BASE_URL}{path}"
    req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise RuntimeError(f"Uptime Kuma API error {e.code}: {error_body}")


def _get_monitor_map(slug: str) -> dict:
    """Returns {monitor_id: monitor_info} from the status page."""
    page_data = kuma_request(f"/api/status-page/{slug}")
    monitor_map = {}
    for group in page_data.get("publicGroupList", []):
        for m in group.get("monitorList", []):
            monitor_map[str(m["id"])] = {
                "id": m["id"],
                "name": m["name"],
                "type": m.get("type"),
                "group": group.get("name"),
            }
    return monitor_map


def _get_heartbeats(slug: str) -> dict:
    """Returns {monitor_id: [heartbeats]} from the heartbeat endpoint."""
    data = kuma_request(f"/api/status-page/heartbeat/{slug}")
    return data.get("heartbeatList", {})


@mcp.tool()
def monitors_list(status_page: str = None) -> str:
    """
    Lists all monitors from a status page.

    Args:
        status_page: Status page slug (default: configured page, 'homelab')

    Returns:
        JSON list of monitors with id, name, type, group
    """
    slug = status_page or KUMA_STATUS_PAGE
    monitor_map = _get_monitor_map(slug)

    result = list(monitor_map.values())
    return json.dumps({
        "monitors": result,
        "total": len(result),
        "status_page": slug,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def monitors_status(status_page: str = None) -> str:
    """
    Gets current UP/DOWN status for all monitors with latest heartbeat data.

    Args:
        status_page: Status page slug (default: 'homelab')

    Returns:
        JSON list of monitors with current status (1=UP, 0=DOWN), latency, last check time
    """
    slug = status_page or KUMA_STATUS_PAGE
    monitor_map = _get_monitor_map(slug)
    heartbeats = _get_heartbeats(slug)

    result = []
    for mid, info in monitor_map.items():
        beats = heartbeats.get(mid, [])
        latest = beats[-1] if beats else None

        result.append({
            "id": info["id"],
            "name": info["name"],
            "type": info["type"],
            "group": info["group"],
            "status": latest.get("status") if latest else None,
            "status_text": "UP" if (latest and latest.get("status") == 1) else "DOWN" if latest else "UNKNOWN",
            "latency_ms": latest.get("ping") if latest else None,
            "last_check": latest.get("time") if latest else None,
            "message": latest.get("msg", "") if latest else None,
        })

    # Sort: DOWN first, then UP
    result.sort(key=lambda x: (x["status"] if x["status"] is not None else -1), reverse=False)

    up_count = sum(1 for m in result if m["status"] == 1)
    down_count = sum(1 for m in result if m["status"] == 0)
    unknown_count = sum(1 for m in result if m["status"] is None)

    return json.dumps({
        "monitors": result,
        "summary": {
            "total": len(result),
            "up": up_count,
            "down": down_count,
            "unknown": unknown_count,
            "health_pct": round(up_count / len(result) * 100, 1) if result else 0,
        },
        "status_page": slug,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def status_overview(status_page: str = None) -> str:
    """
    Full dashboard overview: all monitor statuses with 24h uptime from heartbeat history.

    Args:
        status_page: Status page slug (default: 'homelab')

    Returns:
        JSON with all monitors, current status, avg latency, and uptime percentage
    """
    slug = status_page or KUMA_STATUS_PAGE
    monitor_map = _get_monitor_map(slug)
    heartbeats = _get_heartbeats(slug)

    result = []
    for mid, info in monitor_map.items():
        beats = heartbeats.get(mid, [])
        latest = beats[-1] if beats else None

        # Calculate uptime % from heartbeat history
        total_beats = len(beats)
        up_beats = sum(1 for b in beats if b.get("status") == 1)
        uptime_pct = round(up_beats / total_beats * 100, 2) if total_beats > 0 else None

        # Average latency (only from UP beats with ping)
        pings = [b.get("ping") for b in beats if b.get("status") == 1 and b.get("ping")]
        avg_latency = round(sum(pings) / len(pings), 1) if pings else None

        result.append({
            "id": info["id"],
            "name": info["name"],
            "type": info["type"],
            "group": info["group"],
            "current_status": "UP" if (latest and latest.get("status") == 1) else "DOWN" if latest else "UNKNOWN",
            "latency_ms": latest.get("ping") if latest else None,
            "avg_latency_ms": avg_latency,
            "uptime_pct": uptime_pct,
            "checks_in_history": total_beats,
            "last_check": latest.get("time") if latest else None,
        })

    result.sort(key=lambda x: (0 if x["current_status"] == "DOWN" else 1, x["name"]))

    up_count = sum(1 for m in result if m["current_status"] == "UP")
    down_count = sum(1 for m in result if m["current_status"] == "DOWN")

    return json.dumps({
        "overview": result,
        "summary": {
            "total": len(result),
            "up": up_count,
            "down": down_count,
            "health_pct": round(up_count / len(result) * 100, 1) if result else 0,
        },
        "status_page_url": f"{KUMA_BASE_URL}/status/{slug}",
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print(f"Uptime Kuma MCP Server starting...", flush=True)
    print(f"Kuma URL: {KUMA_BASE_URL} | Page: {KUMA_STATUS_PAGE}", flush=True)
    mcp.run()

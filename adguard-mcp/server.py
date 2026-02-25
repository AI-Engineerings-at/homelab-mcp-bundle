#!/usr/bin/env python3
"""
AdGuard Home MCP Server
Enables AI agents to monitor and manage AdGuard Home DNS filtering via its REST API.

Features:
- status        — AdGuard version, protection state, DNS port
- stats         — Query statistics: blocked %, top domains, top clients
- querylog      — Recent DNS query log with block reason
- filtering     — Filter lists status and rule counts
- block_domain  — Add a domain to the custom blocklist
- toggle_protection — Enable/disable DNS protection
"""

import os
import json
import urllib.request
import urllib.parse
import base64
from typing import Any
from mcp.server.fastmcp import FastMCP

# Configuration
ADGUARD_URL = os.environ.get("ADGUARD_URL", "http://your-adguard-host:3053")
ADGUARD_USER = os.environ.get("ADGUARD_USER", "admin")
ADGUARD_PASSWORD = os.environ.get("ADGUARD_PASSWORD", "")

mcp = FastMCP("adguard-mcp")


def _auth_header() -> str:
    """Basic auth header for AdGuard Home."""
    if not ADGUARD_PASSWORD:
        raise ValueError("ADGUARD_PASSWORD not set.")
    creds = base64.b64encode(f"{ADGUARD_USER}:{ADGUARD_PASSWORD}".encode()).decode()
    return f"Basic {creds}"


def adguard_get(path: str) -> Any:
    """GET request to AdGuard Home API."""
    url = f"{ADGUARD_URL}{path}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": _auth_header(), "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"AdGuard API error {e.code}: {e.read().decode()}")


def adguard_post(path: str, data: dict) -> Any:
    """POST request to AdGuard Home API."""
    url = f"{ADGUARD_URL}{path}"
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": _auth_header(),
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {"ok": True}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"AdGuard API error {e.code}: {e.read().decode()}")


@mcp.tool()
def status() -> str:
    """
    Gets AdGuard Home status: version, protection state, DNS addresses.

    Returns:
        JSON with version, protection_enabled, dns_port, dns_addresses, running state
    """
    data = adguard_get("/control/status")
    return json.dumps({
        "version": data.get("version"),
        "running": data.get("running"),
        "protection_enabled": data.get("protection_enabled"),
        "dns_port": data.get("dns_port"),
        "http_port": data.get("http_port"),
        "dns_addresses": data.get("dns_addresses", []),
        "dhcp_available": data.get("dhcp_available"),
    }, ensure_ascii=False, indent=2)


def _sum_stat(val) -> int:
    """AdGuard stats API may return hourly arrays or a plain int — normalize to int."""
    if isinstance(val, list):
        return sum(val)
    return val or 0


@mcp.tool()
def stats() -> str:
    """
    Gets AdGuard Home query statistics for the last 24 hours.

    Returns:
        JSON with total queries, blocked count/%, top blocked domains, top clients
    """
    data = adguard_get("/control/stats")

    # dns_queries and blocked_filtering may be hourly arrays or plain ints
    total = _sum_stat(data.get("dns_queries", 0))
    blocked = _sum_stat(data.get("blocked_filtering", 0))
    block_pct = round(blocked / total * 100, 1) if total > 0 else 0

    top_blocked = [
        {"domain": list(item.keys())[0], "count": list(item.values())[0]}
        for item in (data.get("top_blocked_domains") or [])[:10]
    ]
    top_clients = [
        {"client": list(item.keys())[0], "count": list(item.values())[0]}
        for item in (data.get("top_clients") or [])[:10]
    ]
    top_queried = [
        {"domain": list(item.keys())[0], "count": list(item.values())[0]}
        for item in (data.get("top_queried_domains") or [])[:10]
    ]

    return json.dumps({
        "period": "24h",
        "dns_queries_total": total,
        "blocked_total": blocked,
        "blocked_percent": block_pct,
        "safebrowsing_blocked": _sum_stat(data.get("replaced_safebrowsing", 0)),
        "parental_blocked": _sum_stat(data.get("replaced_parental", 0)),
        "top_blocked_domains": top_blocked,
        "top_clients": top_clients,
        "top_queried_domains": top_queried,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def querylog(limit: int = 20, search: str = "") -> str:
    """
    Gets recent DNS query log entries.

    Args:
        limit: Number of recent log entries to return (default: 20, max: 100)
        search: Optional domain search filter (e.g. 'ads.example.com')

    Returns:
        JSON list of DNS queries with domain, client IP, result, and block reason
    """
    limit = min(limit, 100)
    path = f"/control/querylog?limit={limit}"
    if search:
        path += f"&search={urllib.parse.quote(search)}"

    data = adguard_get(path)
    entries = data.get("data", [])

    result = []
    for entry in entries:
        result.append({
            "time": entry.get("time", ""),
            "domain": entry.get("question", {}).get("name", "").rstrip("."),
            "type": entry.get("question", {}).get("type", ""),
            "client": entry.get("client", ""),
            "status": entry.get("reason", ""),
            "blocked": entry.get("reason", "") not in ("", "NotFiltered"),
            "upstream": entry.get("upstream", ""),
            "elapsed_ms": entry.get("elapsed_ms", 0),
        })

    blocked_count = sum(1 for r in result if r["blocked"])
    return json.dumps({
        "entries": result,
        "total_returned": len(result),
        "blocked_in_result": blocked_count,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def filtering_status() -> str:
    """
    Gets filter list status: enabled lists, rule counts, last update.

    Returns:
        JSON with filter lists (name, URL, rule count, enabled state) and custom rules count
    """
    data = adguard_get("/control/filtering/status")

    filters = []
    for f in data.get("filters", []):
        filters.append({
            "id": f.get("id"),
            "name": f.get("name"),
            "url": f.get("url", "")[:80],
            "enabled": f.get("enabled"),
            "rules_count": f.get("rules_count", 0),
            "last_updated": f.get("last_updated", ""),
        })

    custom_rules = data.get("user_rules", [])

    return json.dumps({
        "filtering_enabled": data.get("enabled"),
        "filters": filters,
        "filters_count": len(filters),
        "total_rules": sum(f["rules_count"] for f in filters),
        "custom_rules_count": len(custom_rules),
        "custom_rules_preview": custom_rules[:5],
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def block_domain(domain: str) -> str:
    """
    Adds a domain to AdGuard Home's custom blocking rules.

    Args:
        domain: Domain to block (e.g. 'ads.example.com' or '||tracker.com^')

    Returns:
        JSON confirming the rule was added
    """
    # Normalize: if not already in adblock format, convert it
    if not domain.startswith("||") and not domain.startswith("!"):
        rule = f"||{domain}^"
    else:
        rule = domain

    # Get existing custom rules first
    filter_data = adguard_get("/control/filtering/status")
    existing_rules = filter_data.get("user_rules", [])

    if rule in existing_rules:
        return json.dumps({
            "status": "already_exists",
            "rule": rule,
            "message": f"Rule '{rule}' is already in the custom blocklist.",
        }, ensure_ascii=False, indent=2)

    # Add the new rule
    new_rules = existing_rules + [rule]
    adguard_post("/control/filtering/set_rules", {"rules": new_rules})

    return json.dumps({
        "status": "blocked",
        "rule": rule,
        "domain": domain,
        "total_custom_rules": len(new_rules),
        "message": f"Domain '{domain}' successfully added to blocklist.",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def toggle_protection(enabled: bool) -> str:
    """
    Enables or disables AdGuard Home DNS protection.

    Args:
        enabled: True to enable protection, False to disable

    Returns:
        JSON confirming the new protection state
    """
    adguard_post("/control/protection", {"enabled": enabled})

    # Verify new state
    new_status = adguard_get("/control/status")
    actual_state = new_status.get("protection_enabled")

    return json.dumps({
        "requested": enabled,
        "protection_enabled": actual_state,
        "status": "ok" if actual_state == enabled else "mismatch",
        "message": f"DNS protection {'enabled' if actual_state else 'disabled'}.",
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys

    if not ADGUARD_PASSWORD:
        print("ERROR: ADGUARD_PASSWORD environment variable not set!", file=sys.stderr)
        print("Example: export ADGUARD_PASSWORD=yourpassword", file=sys.stderr)
        sys.exit(1)

    print(f"AdGuard Home MCP Server starting...", file=sys.stderr)
    print(f"AdGuard: {ADGUARD_URL} | User: {ADGUARD_USER}", file=sys.stderr)
    mcp.run()

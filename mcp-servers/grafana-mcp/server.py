#!/usr/bin/env python3
"""
Grafana MCP Server
Enables AI agents to query dashboards, datasources, and alerts via Grafana REST API.

Features:
- dashboards_list  — List all dashboards with folder and UID
- dashboard_get    — Get full dashboard JSON by UID
- datasources_list — List all configured datasources
- alerts_list      — List alert rules (Grafana unified alerting)
- query_prometheus — Run an instant PromQL query against Prometheus datasource
- annotations_list — Get recent annotations/events
"""

import os
import json
import urllib.request
import urllib.parse
import base64
from typing import Any
from mcp.server.fastmcp import FastMCP

# Configuration
GRAFANA_URL = os.environ.get("GRAFANA_URL", "http://10.40.10.80:3000")
GRAFANA_USER = os.environ.get("GRAFANA_USER", "admin")
GRAFANA_PASSWORD = os.environ.get("GRAFANA_PASSWORD", "")
GRAFANA_TOKEN = os.environ.get("GRAFANA_TOKEN", "")  # API key alternative

mcp = FastMCP("grafana-mcp")


def _auth_header() -> str:
    """Auth header — prefer API token, fallback to Basic auth."""
    if GRAFANA_TOKEN:
        return f"Bearer {GRAFANA_TOKEN}"
    if not GRAFANA_PASSWORD:
        raise ValueError("GRAFANA_PASSWORD or GRAFANA_TOKEN not set.")
    creds = base64.b64encode(f"{GRAFANA_USER}:{GRAFANA_PASSWORD}".encode()).decode()
    return f"Basic {creds}"


def grafana_get(path: str, params: dict = None) -> Any:
    """GET request to Grafana API."""
    url = f"{GRAFANA_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"Authorization": _auth_header(), "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Grafana API error {e.code}: {e.read().decode()}")


@mcp.tool()
def dashboards_list(query: str = "", folder: str = "") -> str:
    """
    Lists all Grafana dashboards with title, UID, folder and URL.

    Args:
        query: Optional search filter (e.g. 'docker', 'network')
        folder: Optional folder name filter (e.g. 'Infrastructure', 'Docker')

    Returns:
        JSON list of dashboards with title, uid, folder, url, tags
    """
    params = {"type": "dash-db", "limit": 100}
    if query:
        params["query"] = query
    if folder:
        params["folderTitle"] = folder

    items = grafana_get("/api/search", params) or []

    result = []
    for item in items:
        result.append({
            "uid": item.get("uid"),
            "title": item.get("title"),
            "folder": item.get("folderTitle", "General"),
            "url": f"{GRAFANA_URL}{item.get('url', '')}",
            "tags": item.get("tags", []),
            "type": item.get("type"),
        })

    result.sort(key=lambda x: (x["folder"] or "", x["title"] or ""))

    return json.dumps({
        "dashboards": result,
        "total": len(result),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def dashboard_get(uid: str) -> str:
    """
    Gets a specific Grafana dashboard by UID, including panel list.

    Args:
        uid: Dashboard UID (from dashboards_list, e.g. 'prometheus-stats')

    Returns:
        JSON with dashboard title, description, panels list, and tags
    """
    data = grafana_get(f"/api/dashboards/uid/{uid}")
    db = data.get("dashboard", {})
    meta = data.get("meta", {})

    panels = []
    for panel in db.get("panels", []):
        # Handle rows (which contain nested panels)
        if panel.get("type") == "row":
            for sub in panel.get("panels", []):
                panels.append({
                    "id": sub.get("id"),
                    "title": sub.get("title"),
                    "type": sub.get("type"),
                    "datasource": sub.get("datasource", {}).get("type") if isinstance(sub.get("datasource"), dict) else sub.get("datasource"),
                })
        else:
            panels.append({
                "id": panel.get("id"),
                "title": panel.get("title"),
                "type": panel.get("type"),
                "datasource": panel.get("datasource", {}).get("type") if isinstance(panel.get("datasource"), dict) else panel.get("datasource"),
            })

    return json.dumps({
        "uid": uid,
        "title": db.get("title"),
        "description": db.get("description", ""),
        "folder": meta.get("folderTitle", "General"),
        "tags": db.get("tags", []),
        "panels_count": len(panels),
        "panels": panels[:30],
        "url": f"{GRAFANA_URL}{meta.get('url', '')}",
        "version": db.get("version"),
        "updated": meta.get("updated"),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def datasources_list() -> str:
    """
    Lists all configured Grafana datasources.

    Returns:
        JSON list of datasources with name, type, URL, and access mode
    """
    items = grafana_get("/api/datasources") or []

    result = []
    for ds in items:
        result.append({
            "id": ds.get("id"),
            "uid": ds.get("uid"),
            "name": ds.get("name"),
            "type": ds.get("type"),
            "url": ds.get("url"),
            "access": ds.get("access"),
            "is_default": ds.get("isDefault", False),
            "read_only": ds.get("readOnly", False),
        })

    return json.dumps({
        "datasources": result,
        "total": len(result),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def alerts_list() -> str:
    """
    Lists all Grafana alert rules with current state.

    Returns:
        JSON list of alert rules with name, state (firing/normal/pending), labels
    """
    # Try Prometheus-compatible rules endpoint (unified alerting)
    try:
        data = grafana_get("/api/prometheus/grafana/api/v1/rules")
        groups = data.get("data", {}).get("groups", [])

        rules = []
        for group in groups:
            for rule in group.get("rules", []):
                rules.append({
                    "name": rule.get("name"),
                    "group": group.get("name"),
                    "state": rule.get("state", "unknown"),
                    "health": rule.get("health", ""),
                    "labels": rule.get("labels", {}),
                    "annotations": rule.get("annotations", {}),
                    "alerts": [
                        {
                            "labels": a.get("labels", {}),
                            "state": a.get("state"),
                            "active_since": a.get("activeAt"),
                        }
                        for a in rule.get("alerts", [])
                    ],
                })

        firing = [r for r in rules if r["state"] == "firing"]

        return json.dumps({
            "rules_total": len(rules),
            "firing_count": len(firing),
            "rules": rules,
        }, ensure_ascii=False, indent=2)

    except RuntimeError:
        return json.dumps({"error": "Alert rules endpoint not available", "rules": []}, indent=2)


@mcp.tool()
def query_prometheus(expr: str, datasource: str = "Prometheus") -> str:
    """
    Runs an instant PromQL query against a Prometheus datasource in Grafana.

    Args:
        expr: PromQL expression (e.g. 'up', 'node_memory_MemAvailable_bytes/node_memory_MemTotal_bytes*100')
        datasource: Datasource name (default: 'Prometheus')

    Returns:
        JSON with query results — metric labels and current values
    """
    # Get datasource UID
    sources = grafana_get("/api/datasources") or []
    ds_uid = None
    for ds in sources:
        if ds.get("name") == datasource:
            ds_uid = ds.get("uid")
            break

    if not ds_uid:
        raise RuntimeError(f"Datasource '{datasource}' not found. Available: {[d.get('name') for d in sources]}")

    # Run instant query via Grafana's datasource proxy
    data = grafana_get(
        f"/api/datasources/proxy/uid/{ds_uid}/api/v1/query",
        {"query": expr},
    )

    results = data.get("data", {}).get("result", [])

    parsed = []
    for item in results:
        metric = item.get("metric", {})
        value = item.get("value", [None, None])
        parsed.append({
            "metric": metric,
            "value": float(value[1]) if value[1] is not None else None,
            "timestamp": value[0],
        })

    return json.dumps({
        "expr": expr,
        "datasource": datasource,
        "result_type": data.get("data", {}).get("resultType"),
        "results_count": len(parsed),
        "results": parsed[:50],
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def annotations_list(limit: int = 20, alert_only: bool = False) -> str:
    """
    Gets recent Grafana annotations (events, alerts, deployments).

    Args:
        limit: Number of recent annotations (default: 20, max: 100)
        alert_only: True = only alert state change annotations

    Returns:
        JSON list of annotations with time, text, tags, and alert info
    """
    limit = min(limit, 100)
    params: dict = {"limit": limit}
    if alert_only:
        params["type"] = "alert"

    items = grafana_get("/api/annotations", params) or []

    result = []
    for ann in items:
        result.append({
            "id": ann.get("id"),
            "time": ann.get("time"),
            "time_end": ann.get("timeEnd"),
            "text": ann.get("text", "")[:200],
            "tags": ann.get("tags", []),
            "alert_id": ann.get("alertId"),
            "alert_name": ann.get("alertName"),
            "new_state": ann.get("newState"),
            "prev_state": ann.get("prevState"),
            "dashboard_uid": ann.get("dashboardUID"),
        })

    return json.dumps({
        "annotations": result,
        "total_returned": len(result),
    }, ensure_ascii=False, indent=2)


def main():
    import sys

    if not GRAFANA_PASSWORD and not GRAFANA_TOKEN:
        print("ERROR: GRAFANA_PASSWORD or GRAFANA_TOKEN environment variable not set!", file=sys.stderr)
        print("Example: export GRAFANA_PASSWORD=yourpassword", file=sys.stderr)
        sys.exit(1)

    print(f"Grafana MCP Server starting...", file=sys.stderr)
    print(f"Grafana: {GRAFANA_URL} | User: {GRAFANA_USER}", file=sys.stderr)
    mcp.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
n8n MCP Server — PoC
Ermoeglicht AI-Agents Zugriff auf n8n Workflow Automation via Model Context Protocol.

Features:
- workflows/list      — Alle Workflows auflisten
- workflows/get       — Einzelnen Workflow abrufen
- workflows/execute   — Workflow per Webhook ausfuehren
- executions/list     — Ausfuehrungen auflisten
- executions/get      — Einzelne Ausfuehrung abrufen
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Any
from mcp.server.fastmcp import FastMCP

# Konfiguration
N8N_BASE_URL = os.environ.get("N8N_BASE_URL", "http://your-n8n-host:5678/api/v1")
N8N_API_KEY = os.environ.get("N8N_API_KEY", "")
N8N_WEBHOOK_BASE = os.environ.get("N8N_WEBHOOK_BASE", "http://your-n8n-host:5678/webhook")

mcp = FastMCP("n8n-mcp")


def n8n_request(method: str, path: str, data: dict = None) -> Any:
    """HTTP Request an n8n REST API."""
    if not N8N_API_KEY:
        raise ValueError("N8N_API_KEY nicht gesetzt. Bitte N8N_API_KEY Umgebungsvariable setzen.")

    url = f"{N8N_BASE_URL}{path}"
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise RuntimeError(f"n8n API Fehler {e.code}: {error_body}")


@mcp.tool()
def workflows_list(active_only: bool = False, limit: int = 20, cursor: str = None) -> str:
    """
    Listet alle n8n Workflows auf.

    Args:
        active_only: Nur aktive Workflows anzeigen
        limit: Anzahl Workflows (max 250)
        cursor: Pagination-Cursor fuer naechste Seite

    Returns:
        JSON-Liste der Workflows mit id, name, active, createdAt, updatedAt
    """
    path = f"/workflows?limit={limit}"
    if active_only:
        path += "&active=true"
    if cursor:
        path += f"&cursor={cursor}"

    resp = n8n_request("GET", path)
    workflows = resp.get("data", [])

    result = []
    for wf in workflows:
        result.append({
            "id": wf.get("id"),
            "name": wf.get("name"),
            "active": wf.get("active"),
            "is_archived": wf.get("isArchived", False),
            "created_at": wf.get("createdAt"),
            "updated_at": wf.get("updatedAt"),
            "tags": [t.get("name") for t in wf.get("tags", [])],
            "node_count": len(wf.get("nodes", [])),
        })

    return json.dumps({
        "workflows": result,
        "total": len(result),
        "next_cursor": resp.get("nextCursor"),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def workflows_get(workflow_id: str) -> str:
    """
    Ruft einen einzelnen Workflow ab (inkl. Nodes und Connections).

    Args:
        workflow_id: Workflow-ID (z.B. '3fjZhk51u5uYzCpq')

    Returns:
        JSON mit vollstaendigem Workflow inkl. Nodes
    """
    wf = n8n_request("GET", f"/workflows/{workflow_id}")

    result = {
        "id": wf.get("id"),
        "name": wf.get("name"),
        "active": wf.get("active"),
        "created_at": wf.get("createdAt"),
        "updated_at": wf.get("updatedAt"),
        "tags": [t.get("name") for t in wf.get("tags", [])],
        "nodes": [
            {
                "name": n.get("name"),
                "type": n.get("type"),
                "position": n.get("position"),
            }
            for n in wf.get("nodes", [])
        ],
        "settings": wf.get("settings", {}),
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def workflows_execute(webhook_path: str, payload: dict = None, method: str = "POST") -> str:
    """
    Fuehrt einen Workflow via Webhook aus.

    Args:
        webhook_path: Webhook-Pfad (z.B. 'my-workflow' fuer /webhook/my-workflow)
        payload: Optional — JSON-Daten fuer den Webhook
        method: HTTP-Methode (POST oder GET)

    Returns:
        JSON-Response des Webhooks

    Beispiel:
        workflows_execute('stripe-alert', {'amount': 100, 'currency': 'EUR'})
    """
    url = f"{N8N_WEBHOOK_BASE}/{webhook_path}"
    headers = {"Content-Type": "application/json"}

    body = json.dumps(payload or {}).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method=method.upper())

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            response_text = resp.read().decode()
            try:
                response_data = json.loads(response_text)
            except json.JSONDecodeError:
                response_data = {"raw_response": response_text}

            return json.dumps({
                "status": resp.status,
                "webhook_url": url,
                "response": response_data,
            }, ensure_ascii=False, indent=2)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise RuntimeError(f"Webhook Fehler {e.code}: {error_body}")


@mcp.tool()
def executions_list(workflow_id: str = None, status: str = None, limit: int = 20) -> str:
    """
    Listet Workflow-Ausfuehrungen auf.

    Args:
        workflow_id: Optional — nur Ausfuehrungen dieses Workflows
        status: Optional — Filter: 'success', 'error', 'running', 'waiting'
        limit: Anzahl Ausfuehrungen (max 250)

    Returns:
        JSON-Liste der Executions mit id, status, startedAt, stoppedAt, workflowId
    """
    path = f"/executions?limit={limit}"
    if workflow_id:
        path += f"&workflowId={workflow_id}"
    if status:
        path += f"&status={status}"

    resp = n8n_request("GET", path)
    executions = resp.get("data", [])

    result = []
    for ex in executions:
        result.append({
            "id": ex.get("id"),
            "workflow_id": ex.get("workflowId"),
            "status": ex.get("status"),
            "mode": ex.get("mode"),
            "started_at": ex.get("startedAt"),
            "stopped_at": ex.get("stoppedAt"),
            "finished": ex.get("finished"),
        })

    return json.dumps({
        "executions": result,
        "total": len(result),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def executions_get(execution_id: int) -> str:
    """
    Ruft Details einer einzelnen Workflow-Ausfuehrung ab.

    Args:
        execution_id: Execution-ID (Zahl)

    Returns:
        JSON mit Execution-Details inkl. Fehlerinfo
    """
    ex = n8n_request("GET", f"/executions/{execution_id}")

    result = {
        "id": ex.get("id"),
        "workflow_id": ex.get("workflowId"),
        "status": ex.get("status"),
        "mode": ex.get("mode"),
        "started_at": ex.get("startedAt"),
        "stopped_at": ex.get("stoppedAt"),
        "finished": ex.get("finished"),
        "data": {
            "result_data": ex.get("data", {}).get("resultData", {}).get("runData", {}),
            "error": ex.get("data", {}).get("resultData", {}).get("error"),
        } if ex.get("data") else None,
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys

    if not N8N_API_KEY:
        print("FEHLER: N8N_API_KEY Umgebungsvariable nicht gesetzt!", file=sys.stderr)
        print("API Key liegt in: ~/.claude/.n8n-api-key", file=sys.stderr)
        sys.exit(1)

    print(f"n8n MCP Server startet...", file=sys.stderr)
    print(f"Base URL: {N8N_BASE_URL}", file=sys.stderr)
    mcp.run()

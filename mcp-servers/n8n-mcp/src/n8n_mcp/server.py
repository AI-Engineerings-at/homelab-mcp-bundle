"""
n8n MCP Server
n8n REST API v1 via Model Context Protocol

Tools:
  - list_workflows      List all workflows (id, name, active, tags)
  - get_workflow        Get full details of a single workflow
  - activate_workflow   Activate a workflow
  - deactivate_workflow Deactivate a workflow
  - list_executions     List recent executions (optionally filter by workflow)
  - get_execution       Get details + output of a specific execution
  - trigger_webhook     POST to a webhook-triggered workflow
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
N8N_BASE_URL = os.environ.get("N8N_BASE_URL", "http://10.40.10.80:5678")
N8N_API_KEY  = os.environ.get("N8N_API_KEY", "")


# ── n8n API client ─────────────────────────────────────────────────────────────
class N8nClient:
    def __init__(self, base_url: str, api_key: str):
        self.api_base = base_url.rstrip("/") + "/api/v1"
        self.webhook_base = base_url.rstrip("/")
        self.headers = {
            "X-N8N-API-KEY": api_key,
            "Content-Type": "application/json",
        }

    async def _get(self, path: str, params: dict | None = None) -> Any:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(
                f"{self.api_base}{path}",
                headers=self.headers,
                params=params or {},
            )
            r.raise_for_status()
            return r.json()

    async def _post(self, path: str, body: dict | None = None, base: str | None = None) -> Any:
        url = f"{base or self.api_base}{path}"
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, headers=self.headers, json=body or {})
            r.raise_for_status()
            return r.json()

    # ── Workflows ───────────────────────────────────────────────────────────────
    async def list_workflows(self, active: bool | None = None, limit: int = 50) -> dict:
        params: dict = {"limit": limit}
        if active is not None:
            params["active"] = str(active).lower()
        return await self._get("/workflows", params)

    async def get_workflow(self, workflow_id: str) -> dict:
        return await self._get(f"/workflows/{workflow_id}")

    async def activate_workflow(self, workflow_id: str) -> dict:
        return await self._post(f"/workflows/{workflow_id}/activate")

    async def deactivate_workflow(self, workflow_id: str) -> dict:
        return await self._post(f"/workflows/{workflow_id}/deactivate")

    # ── Executions ─────────────────────────────────────────────────────────────
    async def list_executions(
        self,
        workflow_id: str | None = None,
        status: str | None = None,
        limit: int = 20,
    ) -> dict:
        params: dict = {"limit": limit, "includeData": "false"}
        if workflow_id:
            params["workflowId"] = workflow_id
        if status:
            params["status"] = status
        return await self._get("/executions", params)

    async def get_execution(self, execution_id: str) -> dict:
        return await self._get(f"/executions/{execution_id}", {"includeData": "true"})

    # ── Webhook trigger ────────────────────────────────────────────────────────
    async def trigger_webhook(self, webhook_path: str, payload: dict) -> Any:
        path = webhook_path if webhook_path.startswith("/") else f"/webhook/{webhook_path}"
        return await self._post(path, body=payload, base=self.webhook_base)


# ── MCP Server ─────────────────────────────────────────────────────────────────
server = Server("n8n-mcp")
n8n = N8nClient(N8N_BASE_URL, N8N_API_KEY)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_workflows",
            description=(
                "List all n8n workflows. Returns id, name, active status and tags. "
                "Optionally filter by active/inactive."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "active": {
                        "type": "boolean",
                        "description": "Filter: true = only active, false = only inactive. Omit for all.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max workflows to return (default 50)",
                        "default": 50,
                    },
                },
            },
        ),
        types.Tool(
            name="get_workflow",
            description="Get full details of a specific workflow including all nodes and connections.",
            inputSchema={
                "type": "object",
                "required": ["workflow_id"],
                "properties": {
                    "workflow_id": {"type": "string", "description": "The workflow ID (numeric string)"},
                },
            },
        ),
        types.Tool(
            name="activate_workflow",
            description="Activate a workflow so it responds to its triggers.",
            inputSchema={
                "type": "object",
                "required": ["workflow_id"],
                "properties": {
                    "workflow_id": {"type": "string", "description": "The workflow ID to activate"},
                },
            },
        ),
        types.Tool(
            name="deactivate_workflow",
            description="Deactivate a workflow so it no longer responds to triggers.",
            inputSchema={
                "type": "object",
                "required": ["workflow_id"],
                "properties": {
                    "workflow_id": {"type": "string", "description": "The workflow ID to deactivate"},
                },
            },
        ),
        types.Tool(
            name="list_executions",
            description=(
                "List recent workflow executions. Shows execution status, start time and duration. "
                "Filter by workflow ID or status."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_id": {
                        "type": "string",
                        "description": "Filter by specific workflow ID (optional)",
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by status: 'success', 'error', 'waiting', 'running'",
                        "enum": ["success", "error", "waiting", "running"],
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max executions to return (default 20)",
                        "default": 20,
                    },
                },
            },
        ),
        types.Tool(
            name="get_execution",
            description="Get full details of a specific execution including node outputs and error messages.",
            inputSchema={
                "type": "object",
                "required": ["execution_id"],
                "properties": {
                    "execution_id": {"type": "string", "description": "The execution ID (numeric string)"},
                },
            },
        ),
        types.Tool(
            name="trigger_webhook",
            description=(
                "Trigger a webhook-based n8n workflow by POSTing to its webhook URL. "
                "Use this to manually start workflows that have a Webhook trigger node."
            ),
            inputSchema={
                "type": "object",
                "required": ["webhook_path"],
                "properties": {
                    "webhook_path": {
                        "type": "string",
                        "description": (
                            "Webhook path — either the full path like 'webhook/my-trigger' "
                            "or just the path suffix 'my-trigger'"
                        ),
                    },
                    "payload": {
                        "type": "object",
                        "description": "JSON payload to send with the webhook request (optional)",
                        "default": {},
                    },
                },
            },
        ),
    ]


# ── Tool dispatcher ─────────────────────────────────────────────────────────────
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    args = arguments or {}

    try:
        if name == "list_workflows":
            active = args.get("active")  # None means all
            data = await n8n.list_workflows(active=active, limit=args.get("limit", 50))
            items = data.get("data", data) if isinstance(data, dict) else data
            summary = [
                {
                    "id": w.get("id"),
                    "name": w.get("name"),
                    "active": w.get("active"),
                    "tags": [t.get("name") for t in w.get("tags", [])],
                    "updatedAt": w.get("updatedAt"),
                }
                for w in items
            ]
            text = json.dumps(summary, indent=2, ensure_ascii=False)

        elif name == "get_workflow":
            data = await n8n.get_workflow(args["workflow_id"])
            # Return a trimmed view — full node list but skip raw position/etc
            result = {
                "id": data.get("id"),
                "name": data.get("name"),
                "active": data.get("active"),
                "tags": [t.get("name") for t in data.get("tags", [])],
                "createdAt": data.get("createdAt"),
                "updatedAt": data.get("updatedAt"),
                "nodes": [
                    {
                        "name": n.get("name"),
                        "type": n.get("type"),
                        "parameters": n.get("parameters", {}),
                    }
                    for n in data.get("nodes", [])
                ],
            }
            text = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "activate_workflow":
            data = await n8n.activate_workflow(args["workflow_id"])
            text = json.dumps({"status": "activated", "id": data.get("id"), "name": data.get("name")}, indent=2)

        elif name == "deactivate_workflow":
            data = await n8n.deactivate_workflow(args["workflow_id"])
            text = json.dumps({"status": "deactivated", "id": data.get("id"), "name": data.get("name")}, indent=2)

        elif name == "list_executions":
            data = await n8n.list_executions(
                workflow_id=args.get("workflow_id"),
                status=args.get("status"),
                limit=args.get("limit", 20),
            )
            items = data.get("data", data) if isinstance(data, dict) else data
            summary = [
                {
                    "id": e.get("id"),
                    "workflowId": e.get("workflowId"),
                    "status": e.get("status"),
                    "startedAt": e.get("startedAt"),
                    "stoppedAt": e.get("stoppedAt"),
                    "mode": e.get("mode"),
                }
                for e in items
            ]
            text = json.dumps(summary, indent=2, ensure_ascii=False)

        elif name == "get_execution":
            data = await n8n.get_execution(args["execution_id"])
            result = {
                "id": data.get("id"),
                "workflowId": data.get("workflowId"),
                "status": data.get("status"),
                "startedAt": data.get("startedAt"),
                "stoppedAt": data.get("stoppedAt"),
                "mode": data.get("mode"),
            }
            # Include error if present
            if data.get("data", {}).get("resultData", {}).get("error"):
                result["error"] = data["data"]["resultData"]["error"]
            # Include last node output (truncated)
            run_data = data.get("data", {}).get("resultData", {}).get("runData", {})
            if run_data:
                result["nodeOutputs"] = {
                    node: [
                        {k: v for k, v in item.items() if k != "binary"}
                        for item in items[:2]  # first 2 items per node
                    ]
                    for node, items in list(run_data.items())[:5]  # first 5 nodes
                }
            text = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "trigger_webhook":
            data = await n8n.trigger_webhook(
                webhook_path=args["webhook_path"],
                payload=args.get("payload", {}),
            )
            text = json.dumps({"status": "triggered", "response": data}, indent=2, ensure_ascii=False)

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as exc:
        text = json.dumps({"error": str(exc)}, indent=2)

    return [types.TextContent(type="text", text=text)]


# ── Entry point ─────────────────────────────────────────────────────────────────
async def main():
    if not N8N_API_KEY:
        print("ERROR: N8N_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="n8n-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

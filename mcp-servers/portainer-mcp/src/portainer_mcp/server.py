"""
Portainer MCP Server
Docker Swarm management via Portainer REST API and Model Context Protocol

Tools:
  - services_list     List all Swarm services (name, image, replicas, status)
  - service_logs      Stream recent logs for a specific service
  - stacks_list       List all Portainer stacks with status
  - stack_deploy      Deploy or update a stack with a compose file
  - node_status       List all Swarm nodes with health and role info
  - containers_list   List containers (optionally filtered by node)
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
PORTAINER_URL     = os.environ.get("PORTAINER_URL", "http://10.40.10.80:9000")
PORTAINER_TOKEN   = os.environ.get("PORTAINER_API_TOKEN", "")
PORTAINER_USER    = os.environ.get("PORTAINER_USER", "admin")
PORTAINER_PASS    = os.environ.get("PORTAINER_PASSWORD", "")
ENDPOINT_ID       = int(os.environ.get("PORTAINER_ENDPOINT_ID", "1"))


# ── Portainer API client ───────────────────────────────────────────────────────
class PortainerClient:
    def __init__(self):
        self.base = PORTAINER_URL.rstrip("/") + "/api"
        self.endpoint_id = ENDPOINT_ID
        self._jwt: str | None = None
        # If API token provided, use it directly
        self._api_token = PORTAINER_TOKEN or None

    def _auth_headers(self) -> dict:
        if self._api_token:
            return {"X-API-Key": self._api_token, "Content-Type": "application/json"}
        if self._jwt:
            return {"Authorization": f"Bearer {self._jwt}", "Content-Type": "application/json"}
        return {"Content-Type": "application/json"}

    async def _login(self) -> None:
        """Authenticate with username/password and cache the JWT."""
        if not PORTAINER_PASS:
            raise RuntimeError(
                "No auth configured. Set PORTAINER_API_TOKEN or PORTAINER_USER + PORTAINER_PASSWORD."
            )
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                f"{self.base}/auth",
                json={"username": PORTAINER_USER, "password": PORTAINER_PASS},
            )
            r.raise_for_status()
            self._jwt = r.json()["jwt"]

    async def _get(self, path: str, params: dict | None = None) -> Any:
        if not self._api_token and not self._jwt:
            await self._login()
        async with httpx.AsyncClient(timeout=30, verify=False) as client:
            r = await client.get(
                f"{self.base}{path}",
                headers=self._auth_headers(),
                params=params or {},
            )
            if r.status_code == 401 and not self._api_token:
                # JWT expired — re-login once
                await self._login()
                r = await client.get(
                    f"{self.base}{path}",
                    headers=self._auth_headers(),
                    params=params or {},
                )
            r.raise_for_status()
            return r.json()

    async def _post(self, path: str, body: dict | None = None) -> Any:
        if not self._api_token and not self._jwt:
            await self._login()
        async with httpx.AsyncClient(timeout=30, verify=False) as client:
            r = await client.post(
                f"{self.base}{path}",
                headers=self._auth_headers(),
                json=body or {},
            )
            r.raise_for_status()
            return r.json() if r.content else {}

    async def _put(self, path: str, body: dict | None = None) -> Any:
        if not self._api_token and not self._jwt:
            await self._login()
        async with httpx.AsyncClient(timeout=60, verify=False) as client:
            r = await client.put(
                f"{self.base}{path}",
                headers=self._auth_headers(),
                json=body or {},
            )
            r.raise_for_status()
            return r.json() if r.content else {}

    # ── Docker Swarm API (via Portainer proxy) ──────────────────────────────────
    def _ep(self, path: str) -> str:
        return f"/endpoints/{self.endpoint_id}/docker{path}"

    async def list_services(self) -> list:
        return await self._get(self._ep("/services"))

    async def get_service_logs(self, service_id: str, tail: int = 100) -> str:
        """Fetch logs as plain text from Docker API via Portainer."""
        if not self._api_token and not self._jwt:
            await self._login()
        url = f"{self.base}{self._ep(f'/services/{service_id}/logs')}"
        params = {
            "stdout": "true",
            "stderr": "true",
            "tail": str(tail),
            "timestamps": "true",
        }
        async with httpx.AsyncClient(timeout=30, verify=False) as client:
            r = await client.get(url, headers=self._auth_headers(), params=params)
            r.raise_for_status()
            # Docker multiplexed stream: strip 8-byte header per chunk
            return _strip_docker_log_headers(r.content)

    async def list_nodes(self) -> list:
        return await self._get(self._ep("/nodes"))

    async def list_containers(self, node_id: str | None = None) -> list:
        params: dict = {"all": "true"}
        if node_id:
            params["filters"] = json.dumps({"node": [node_id]})
        return await self._get(self._ep("/containers/json"), params)

    # ── Portainer Stacks API ────────────────────────────────────────────────────
    async def list_stacks(self) -> list:
        return await self._get("/stacks")

    async def get_stack_file(self, stack_id: int) -> str:
        data = await self._get(f"/stacks/{stack_id}/file")
        return data.get("StackFileContent", "")

    async def deploy_stack(
        self,
        stack_id: int,
        compose_content: str,
        env_vars: list[dict] | None = None,
    ) -> dict:
        """Update an existing stack with new compose file content."""
        # Fetch current env to preserve if not overridden
        current = await self._get(f"/stacks/{stack_id}")
        body = {
            "stackFileContent": compose_content,
            "env": env_vars if env_vars is not None else current.get("Env", []),
            "prune": False,
        }
        return await self._put(f"/stacks/{stack_id}", body)


def _strip_docker_log_headers(raw: bytes) -> str:
    """
    Docker log stream is multiplexed: each chunk has an 8-byte header
    [stream_type(1), 0,0,0, size(4BE)]. Strip those headers.
    Falls back to raw UTF-8 if parsing fails.
    """
    lines = []
    i = 0
    try:
        while i < len(raw):
            if i + 8 > len(raw):
                break
            size = int.from_bytes(raw[i + 4 : i + 8], "big")
            chunk = raw[i + 8 : i + 8 + size]
            lines.append(chunk.decode("utf-8", errors="replace"))
            i += 8 + size
        return "".join(lines).strip()
    except Exception:
        return raw.decode("utf-8", errors="replace").strip()


# ── MCP Server ─────────────────────────────────────────────────────────────────
server = Server("portainer-mcp")
portainer = PortainerClient()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="services_list",
            description=(
                "List all Docker Swarm services managed by Portainer. "
                "Returns service name, image, desired vs running replicas, and update status. "
                "Use this to get an overview of the entire Swarm cluster."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="service_logs",
            description=(
                "Fetch recent logs for a specific Docker Swarm service. "
                "Returns the last N log lines with timestamps. "
                "Use service name or service ID from services_list."
            ),
            inputSchema={
                "type": "object",
                "required": ["service_id"],
                "properties": {
                    "service_id": {
                        "type": "string",
                        "description": "Service ID or name (e.g. 'agents_service-monitor' or 'abc123xyz')",
                    },
                    "tail": {
                        "type": "integer",
                        "description": "Number of recent log lines to return (default: 100)",
                        "default": 100,
                    },
                },
            },
        ),
        types.Tool(
            name="stacks_list",
            description=(
                "List all Portainer stacks (Docker Compose / Swarm stacks). "
                "Returns stack name, status, number of services and creation date."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="stack_deploy",
            description=(
                "Deploy or update a Portainer stack with a new compose file. "
                "The stack must already exist in Portainer (use stacks_list to find the ID). "
                "Provide the full docker-compose YAML content as a string. "
                "WARNING: This applies changes to the live cluster immediately."
            ),
            inputSchema={
                "type": "object",
                "required": ["stack_id", "compose_content"],
                "properties": {
                    "stack_id": {
                        "type": "integer",
                        "description": "Portainer stack ID (numeric, from stacks_list)",
                    },
                    "compose_content": {
                        "type": "string",
                        "description": "Full docker-compose YAML content to deploy",
                    },
                    "env_vars": {
                        "type": "array",
                        "description": "Optional list of env vars [{\"name\": \"KEY\", \"value\": \"val\"}]. If omitted, existing env is preserved.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "value": {"type": "string"},
                            },
                        },
                    },
                },
            },
        ),
        types.Tool(
            name="node_status",
            description=(
                "List all Docker Swarm nodes with role, availability, and health status. "
                "Shows which nodes are Manager/Worker, Active/Drain/Pause, and Ready/Down."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="containers_list",
            description=(
                "List all containers across the Swarm cluster. "
                "Optionally filter by node ID. "
                "Returns container name, image, state, status and assigned node."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "node_id": {
                        "type": "string",
                        "description": "Filter containers by Swarm node ID (optional, from node_status)",
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
        if name == "services_list":
            data = await portainer.list_services()
            services = []
            for svc in data:
                spec = svc.get("Spec", {})
                mode = spec.get("Mode", {})
                replicated = mode.get("Replicated", {})
                status = svc.get("ServiceStatus", {})
                services.append({
                    "id": svc.get("ID", "")[:12],
                    "name": spec.get("Name", ""),
                    "image": spec.get("TaskTemplate", {})
                               .get("ContainerSpec", {})
                               .get("Image", "")
                               .split("@")[0],  # strip digest
                    "mode": "replicated" if "Replicated" in mode else "global",
                    "desired_replicas": replicated.get("Replicas"),
                    "running_replicas": status.get("RunningTasks"),
                    "desired_tasks": status.get("DesiredTasks"),
                    "update_state": svc.get("UpdateStatus", {}).get("State", "—"),
                })
            text = json.dumps(services, indent=2, ensure_ascii=False)

        elif name == "service_logs":
            logs = await portainer.get_service_logs(
                service_id=args["service_id"],
                tail=args.get("tail", 100),
            )
            text = logs if logs else "(no logs found)"

        elif name == "stacks_list":
            data = await portainer.list_stacks()
            stacks = [
                {
                    "id": s.get("Id"),
                    "name": s.get("Name"),
                    "status": s.get("Status"),  # 1=active, 2=inactive
                    "type": "swarm" if s.get("Type") == 1 else "compose",
                    "endpoint_id": s.get("EndpointId"),
                    "created_by": s.get("CreatedBy"),
                    "created": s.get("CreationDate"),
                    "updated": s.get("UpdateDate"),
                }
                for s in data
            ]
            text = json.dumps(stacks, indent=2, ensure_ascii=False)

        elif name == "stack_deploy":
            stack_id = int(args["stack_id"])
            result = await portainer.deploy_stack(
                stack_id=stack_id,
                compose_content=args["compose_content"],
                env_vars=args.get("env_vars"),
            )
            text = json.dumps({
                "status": "deployed",
                "stack_id": stack_id,
                "name": result.get("Name"),
                "updated": result.get("UpdateDate"),
            }, indent=2)

        elif name == "node_status":
            data = await portainer.list_nodes()
            nodes = []
            for node in data:
                spec = node.get("Spec", {})
                desc = node.get("Description", {})
                status = node.get("Status", {})
                mgr = node.get("ManagerStatus", {})
                nodes.append({
                    "id": node.get("ID", "")[:12],
                    "hostname": desc.get("Hostname", ""),
                    "role": spec.get("Role", ""),
                    "availability": spec.get("Availability", ""),
                    "state": status.get("State", ""),
                    "addr": status.get("Addr", ""),
                    "engine_version": desc.get("Engine", {}).get("EngineVersion", ""),
                    "is_leader": mgr.get("Leader", False),
                    "manager_reachability": mgr.get("Reachability", "—") if mgr else "—",
                })
            text = json.dumps(nodes, indent=2, ensure_ascii=False)

        elif name == "containers_list":
            data = await portainer.list_containers(node_id=args.get("node_id"))
            containers = [
                {
                    "id": c.get("Id", "")[:12],
                    "names": [n.lstrip("/") for n in c.get("Names", [])],
                    "image": c.get("Image", "").split("@")[0],
                    "state": c.get("State", ""),
                    "status": c.get("Status", ""),
                    "node": c.get("HostConfig", {}).get("NodeID", "")
                             or c.get("Labels", {}).get("com.docker.swarm.node.id", "")[:12],
                }
                for c in data
            ]
            text = json.dumps(containers, indent=2, ensure_ascii=False)

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as exc:
        text = json.dumps({"error": str(exc)}, indent=2)

    return [types.TextContent(type="text", text=text)]


# ── Entry point ─────────────────────────────────────────────────────────────────
async def main():
    if not PORTAINER_TOKEN and not PORTAINER_PASS:
        print(
            "ERROR: Set PORTAINER_API_TOKEN or PORTAINER_USER + PORTAINER_PASSWORD",
            file=sys.stderr,
        )
        sys.exit(1)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="portainer-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

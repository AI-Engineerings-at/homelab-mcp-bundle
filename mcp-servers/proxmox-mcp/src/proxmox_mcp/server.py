"""
Proxmox MCP Server
Proxmox VE REST API via Model Context Protocol

Tools:
  - list_nodes       List all PVE cluster nodes with status, CPU, memory
  - get_node_status  Get detailed resource usage for a specific node
  - list_vms         List all VMs on a node (or all nodes)
  - list_lxc         List all LXC containers on a node (or all nodes)
  - get_vm_status    Get runtime status of a specific VM
  - start_vm         Start a VM (requires confirmation flag)
  - stop_vm          Stop a VM gracefully (requires confirmation flag)
  - get_cluster_status  Get overall cluster health and quorum info
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
PVE_HOST     = os.environ.get("PVE_HOST", "https://10.40.10.14:8006")
PVE_USER     = os.environ.get("PVE_USER", "root@pam")
PVE_PASSWORD = os.environ.get("PVE_PASSWORD", "")
PVE_VERIFY_SSL = os.environ.get("PVE_VERIFY_SSL", "false").lower() == "true"


# ── Proxmox API client ─────────────────────────────────────────────────────────
class ProxmoxClient:
    def __init__(self, host: str, user: str, password: str, verify_ssl: bool = False):
        self.api_base = host.rstrip("/") + "/api2/json"
        self.user = user
        self.password = password
        self.verify_ssl = verify_ssl
        self._ticket: str | None = None
        self._csrf_token: str | None = None

    async def _authenticate(self) -> None:
        """Get PVE auth ticket via username/password."""
        async with httpx.AsyncClient(verify=self.verify_ssl, timeout=10) as client:
            r = await client.post(
                f"{self.api_base}/access/ticket",
                data={"username": self.user, "password": self.password},
            )
            r.raise_for_status()
            data = r.json()["data"]
            self._ticket = data["ticket"]
            self._csrf_token = data["CSRFPreventionToken"]

    def _cookies(self) -> dict:
        return {"PVEAuthCookie": self._ticket} if self._ticket else {}

    def _headers(self, with_csrf: bool = False) -> dict:
        h = {"Accept": "application/json"}
        if with_csrf and self._csrf_token:
            h["CSRFPreventionToken"] = self._csrf_token
        return h

    async def _get(self, path: str, params: dict | None = None) -> Any:
        if not self._ticket:
            await self._authenticate()
        async with httpx.AsyncClient(verify=self.verify_ssl, timeout=20) as client:
            r = await client.get(
                f"{self.api_base}{path}",
                headers=self._headers(),
                cookies=self._cookies(),
                params=params or {},
            )
            if r.status_code == 401:
                # Re-authenticate once
                await self._authenticate()
                r = await client.get(
                    f"{self.api_base}{path}",
                    headers=self._headers(),
                    cookies=self._cookies(),
                    params=params or {},
                )
            r.raise_for_status()
            return r.json().get("data", r.json())

    async def _post(self, path: str, body: dict | None = None) -> Any:
        if not self._ticket:
            await self._authenticate()
        async with httpx.AsyncClient(verify=self.verify_ssl, timeout=30) as client:
            r = await client.post(
                f"{self.api_base}{path}",
                headers=self._headers(with_csrf=True),
                cookies=self._cookies(),
                json=body or {},
            )
            r.raise_for_status()
            return r.json().get("data", r.json())

    # ── Cluster ─────────────────────────────────────────────────────────────────
    async def get_cluster_status(self) -> list:
        return await self._get("/cluster/status")

    # ── Nodes ───────────────────────────────────────────────────────────────────
    async def list_nodes(self) -> list:
        return await self._get("/nodes")

    async def get_node_status(self, node: str) -> dict:
        return await self._get(f"/nodes/{node}/status")

    # ── VMs (QEMU) ──────────────────────────────────────────────────────────────
    async def list_vms(self, node: str) -> list:
        return await self._get(f"/nodes/{node}/qemu")

    async def get_vm_status(self, node: str, vmid: str) -> dict:
        return await self._get(f"/nodes/{node}/qemu/{vmid}/status/current")

    async def start_vm(self, node: str, vmid: str) -> Any:
        return await self._post(f"/nodes/{node}/qemu/{vmid}/status/start")

    async def stop_vm(self, node: str, vmid: str) -> Any:
        return await self._post(f"/nodes/{node}/qemu/{vmid}/status/stop")

    # ── LXC Containers ──────────────────────────────────────────────────────────
    async def list_lxc(self, node: str) -> list:
        return await self._get(f"/nodes/{node}/lxc")

    async def get_lxc_status(self, node: str, vmid: str) -> dict:
        return await self._get(f"/nodes/{node}/lxc/{vmid}/status/current")


# ── MCP Server ─────────────────────────────────────────────────────────────────
server = Server("proxmox-mcp")
pve = ProxmoxClient(PVE_HOST, PVE_USER, PVE_PASSWORD, PVE_VERIFY_SSL)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_cluster_status",
            description=(
                "Get overall Proxmox VE cluster health, quorum status, and node count. "
                "Use this first to see if the cluster is healthy."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="list_nodes",
            description=(
                "List all Proxmox VE nodes with their status, CPU usage, memory usage, "
                "and uptime. Returns all nodes in the cluster."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="get_node_status",
            description=(
                "Get detailed resource usage for a specific Proxmox node: "
                "CPU, memory, disk, load average, kernel version."
            ),
            inputSchema={
                "type": "object",
                "required": ["node"],
                "properties": {
                    "node": {
                        "type": "string",
                        "description": "Node name (e.g. 'pve', 'pve1', 'pve3')",
                    },
                },
            },
        ),
        types.Tool(
            name="list_vms",
            description=(
                "List all QEMU VMs on a Proxmox node. Returns VM ID, name, status "
                "(running/stopped), CPU and memory usage."
            ),
            inputSchema={
                "type": "object",
                "required": ["node"],
                "properties": {
                    "node": {
                        "type": "string",
                        "description": "Node name (e.g. 'pve', 'pve1', 'pve3')",
                    },
                },
            },
        ),
        types.Tool(
            name="list_lxc",
            description=(
                "List all LXC containers on a Proxmox node. Returns container ID, name, "
                "status, CPU and memory usage."
            ),
            inputSchema={
                "type": "object",
                "required": ["node"],
                "properties": {
                    "node": {
                        "type": "string",
                        "description": "Node name (e.g. 'pve', 'pve1', 'pve3')",
                    },
                },
            },
        ),
        types.Tool(
            name="get_vm_status",
            description=(
                "Get detailed runtime status of a specific VM: CPU usage, memory, "
                "disk I/O, network I/O, uptime, and PID."
            ),
            inputSchema={
                "type": "object",
                "required": ["node", "vmid"],
                "properties": {
                    "node": {
                        "type": "string",
                        "description": "Node name where the VM runs (e.g. 'pve')",
                    },
                    "vmid": {
                        "type": "string",
                        "description": "VM ID (numeric string, e.g. '100')",
                    },
                },
            },
        ),
        types.Tool(
            name="start_vm",
            description=(
                "Start a stopped QEMU VM. Requires confirm=true to prevent accidental starts. "
                "The VM must be in 'stopped' state."
            ),
            inputSchema={
                "type": "object",
                "required": ["node", "vmid", "confirm"],
                "properties": {
                    "node": {
                        "type": "string",
                        "description": "Node name where the VM is located",
                    },
                    "vmid": {
                        "type": "string",
                        "description": "VM ID to start",
                    },
                    "confirm": {
                        "type": "boolean",
                        "description": "Must be true to confirm the start action",
                    },
                },
            },
        ),
        types.Tool(
            name="stop_vm",
            description=(
                "Gracefully shut down a running QEMU VM (ACPI shutdown). "
                "Requires confirm=true. The guest OS will receive a shutdown signal."
            ),
            inputSchema={
                "type": "object",
                "required": ["node", "vmid", "confirm"],
                "properties": {
                    "node": {
                        "type": "string",
                        "description": "Node name where the VM is running",
                    },
                    "vmid": {
                        "type": "string",
                        "description": "VM ID to stop",
                    },
                    "confirm": {
                        "type": "boolean",
                        "description": "Must be true to confirm the stop action",
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
        if name == "get_cluster_status":
            data = await pve.get_cluster_status()
            items = data if isinstance(data, list) else [data]
            result = []
            for item in items:
                entry = {
                    "name": item.get("name"),
                    "type": item.get("type"),
                    "id": item.get("id"),
                    "online": item.get("online"),
                    "quorate": item.get("quorate"),
                    "nodes": item.get("nodes"),
                }
                result.append({k: v for k, v in entry.items() if v is not None})
            text = json.dumps(result, indent=2)

        elif name == "list_nodes":
            data = await pve.list_nodes()
            nodes = data if isinstance(data, list) else [data]
            result = []
            for n in nodes:
                maxmem = n.get("maxmem", 1)
                mem = n.get("mem", 0)
                result.append({
                    "node": n.get("node"),
                    "status": n.get("status"),
                    "cpu_percent": round(n.get("cpu", 0) * 100, 1),
                    "mem_used_gb": round(mem / 1024**3, 2),
                    "mem_total_gb": round(maxmem / 1024**3, 2),
                    "mem_percent": round(mem / maxmem * 100, 1) if maxmem else 0,
                    "uptime_h": round(n.get("uptime", 0) / 3600, 1),
                })
            text = json.dumps(result, indent=2)

        elif name == "get_node_status":
            node = args["node"]
            data = await pve.get_node_status(node)
            mem = data.get("memory", {})
            cpu_info = data.get("cpuinfo", {})
            result = {
                "node": node,
                "uptime_h": round(data.get("uptime", 0) / 3600, 1),
                "cpu_usage_percent": round(data.get("cpu", 0) * 100, 1),
                "cpu_cores": cpu_info.get("cores"),
                "cpu_model": cpu_info.get("model"),
                "memory": {
                    "used_gb": round(mem.get("used", 0) / 1024**3, 2),
                    "total_gb": round(mem.get("total", 1) / 1024**3, 2),
                    "percent": round(mem.get("used", 0) / max(mem.get("total", 1), 1) * 100, 1),
                },
                "load_avg": data.get("loadavg"),
                "kernel": data.get("kversion"),
                "pveversion": data.get("pveversion"),
            }
            text = json.dumps(result, indent=2)

        elif name == "list_vms":
            node = args["node"]
            data = await pve.list_vms(node)
            vms = data if isinstance(data, list) else [data]
            result = []
            for vm in sorted(vms, key=lambda x: x.get("vmid", 0)):
                maxmem = vm.get("maxmem", 1)
                mem = vm.get("mem", 0)
                result.append({
                    "vmid": vm.get("vmid"),
                    "name": vm.get("name"),
                    "status": vm.get("status"),
                    "cpu_percent": round(vm.get("cpu", 0) * 100, 1),
                    "mem_used_mb": round(mem / 1024**2, 0),
                    "mem_total_mb": round(maxmem / 1024**2, 0),
                    "uptime_h": round(vm.get("uptime", 0) / 3600, 1),
                    "node": node,
                })
            text = json.dumps(result, indent=2)

        elif name == "list_lxc":
            node = args["node"]
            data = await pve.list_lxc(node)
            containers = data if isinstance(data, list) else [data]
            result = []
            for ct in sorted(containers, key=lambda x: x.get("vmid", 0)):
                maxmem = ct.get("maxmem", 1)
                mem = ct.get("mem", 0)
                result.append({
                    "vmid": ct.get("vmid"),
                    "name": ct.get("name"),
                    "status": ct.get("status"),
                    "cpu_percent": round(ct.get("cpu", 0) * 100, 1),
                    "mem_used_mb": round(mem / 1024**2, 0),
                    "mem_total_mb": round(maxmem / 1024**2, 0),
                    "uptime_h": round(ct.get("uptime", 0) / 3600, 1),
                    "node": node,
                })
            text = json.dumps(result, indent=2)

        elif name == "get_vm_status":
            node = args["node"]
            vmid = args["vmid"]
            data = await pve.get_vm_status(node, vmid)
            maxmem = data.get("maxmem", 1)
            mem = data.get("mem", 0)
            result = {
                "vmid": vmid,
                "name": data.get("name"),
                "status": data.get("status"),
                "node": node,
                "cpu_percent": round(data.get("cpu", 0) * 100, 1),
                "cpus": data.get("cpus"),
                "memory": {
                    "used_mb": round(mem / 1024**2, 0),
                    "total_mb": round(maxmem / 1024**2, 0),
                    "percent": round(mem / max(maxmem, 1) * 100, 1),
                },
                "disk_read_mb": round(data.get("diskread", 0) / 1024**2, 2),
                "disk_write_mb": round(data.get("diskwrite", 0) / 1024**2, 2),
                "net_in_mb": round(data.get("netin", 0) / 1024**2, 2),
                "net_out_mb": round(data.get("netout", 0) / 1024**2, 2),
                "uptime_h": round(data.get("uptime", 0) / 3600, 1),
                "pid": data.get("pid"),
            }
            text = json.dumps(result, indent=2)

        elif name == "start_vm":
            if not args.get("confirm"):
                text = json.dumps({"error": "confirm must be true to start a VM"}, indent=2)
            else:
                node = args["node"]
                vmid = args["vmid"]
                task = await pve.start_vm(node, vmid)
                text = json.dumps({"status": "start_task_created", "taskid": task, "vmid": vmid, "node": node}, indent=2)

        elif name == "stop_vm":
            if not args.get("confirm"):
                text = json.dumps({"error": "confirm must be true to stop a VM"}, indent=2)
            else:
                node = args["node"]
                vmid = args["vmid"]
                task = await pve.stop_vm(node, vmid)
                text = json.dumps({"status": "stop_task_created", "taskid": task, "vmid": vmid, "node": node}, indent=2)

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as exc:
        text = json.dumps({"error": str(exc)}, indent=2)

    return [types.TextContent(type="text", text=text)]


# ── Entry point ─────────────────────────────────────────────────────────────────
async def main():
    if not PVE_PASSWORD:
        print("ERROR: PVE_PASSWORD environment variable not set", file=sys.stderr)
        sys.exit(1)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="proxmox-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

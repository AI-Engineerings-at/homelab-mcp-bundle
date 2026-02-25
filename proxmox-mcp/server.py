#!/usr/bin/env python3
"""
Proxmox MCP Server
Enables AI agents to manage Proxmox VE via Model Context Protocol.

Features:
- nodes/list      — List all PVE cluster nodes with resource usage
- vms/list        — List all VMs and LXCs on a node
- vm/status       — Get current status of a VM or LXC
- vm/start        — Start a stopped VM or LXC
- vm/stop         — Stop a running VM or LXC (graceful shutdown)
"""

import os
import json
import urllib.request
import urllib.parse
import ssl
from typing import Any
from mcp.server.fastmcp import FastMCP

# Configuration
PVE_HOST = os.environ.get("PVE_HOST", "your-proxmox-host")
PVE_BASE_URL = os.environ.get("PVE_BASE_URL", f"https://{PVE_HOST}:8006/api2/json")
PVE_USER = os.environ.get("PVE_USER", "root@pam")
PVE_PASSWORD = os.environ.get("PVE_PASSWORD", "")
PVE_VERIFY_SSL = os.environ.get("PVE_VERIFY_SSL", "false").lower() == "true"

mcp = FastMCP("proxmox-mcp")

# SSL context (self-signed certs in homelab)
_ssl_ctx = ssl.create_default_context()
if not PVE_VERIFY_SSL:
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE

_auth_ticket: str | None = None
_csrf_token: str | None = None


def _authenticate() -> tuple[str, str]:
    """Authenticate against Proxmox API, return (ticket, csrf_token)."""
    global _auth_ticket, _csrf_token

    if not PVE_PASSWORD:
        raise ValueError("PVE_PASSWORD not set. Please set PVE_PASSWORD environment variable.")

    data = urllib.parse.urlencode({
        "username": PVE_USER,
        "password": PVE_PASSWORD,
    }).encode()

    req = urllib.request.Request(
        f"{PVE_BASE_URL}/access/ticket",
        data=data,
        method="POST",
    )

    with urllib.request.urlopen(req, context=_ssl_ctx, timeout=10) as resp:
        result = json.loads(resp.read())

    _auth_ticket = result["data"]["ticket"]
    _csrf_token = result["data"]["CSRFPreventionToken"]
    return _auth_ticket, _csrf_token


def pve_request(method: str, path: str, data: dict = None) -> Any:
    """HTTP request to Proxmox API with auto-auth."""
    ticket, csrf = _authenticate()

    url = f"{PVE_BASE_URL}{path}"
    headers = {
        "Cookie": f"PVEAuthCookie={ticket}",
        "CSRFPreventionToken": csrf,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    body = None
    if data:
        body = urllib.parse.urlencode(data).encode()

    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, context=_ssl_ctx, timeout=15) as resp:
            return json.loads(resp.read()).get("data")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise RuntimeError(f"Proxmox API error {e.code}: {error_body}")


@mcp.tool()
def nodes_list() -> str:
    """
    Lists all Proxmox VE cluster nodes with resource usage.

    Returns:
        JSON list of nodes with cpu, memory, disk usage and status
    """
    nodes = pve_request("GET", "/nodes") or []

    result = []
    for n in nodes:
        mem_pct = round(n.get("mem", 0) / n.get("maxmem", 1) * 100, 1) if n.get("maxmem") else 0
        disk_pct = round(n.get("disk", 0) / n.get("maxdisk", 1) * 100, 1) if n.get("maxdisk") else 0
        result.append({
            "node": n.get("node"),
            "status": n.get("status"),
            "cpu_usage_pct": round(n.get("cpu", 0) * 100, 1),
            "cpu_cores": n.get("maxcpu"),
            "mem_used_gb": round(n.get("mem", 0) / 1024**3, 2),
            "mem_total_gb": round(n.get("maxmem", 0) / 1024**3, 2),
            "mem_pct": mem_pct,
            "disk_used_gb": round(n.get("disk", 0) / 1024**3, 2),
            "disk_total_gb": round(n.get("maxdisk", 0) / 1024**3, 2),
            "disk_pct": disk_pct,
            "uptime_h": round(n.get("uptime", 0) / 3600, 1),
        })

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def vms_list(node: str = None) -> str:
    """
    Lists all VMs (QEMU) and LXC containers on a node or all nodes.

    Args:
        node: Node name (e.g. 'pve', 'pve1', 'pve3'). If omitted, lists all nodes.

    Returns:
        JSON list of VMs/LXCs with id, name, type, status, cpu, memory
    """
    nodes_to_query = []
    if node:
        nodes_to_query = [node]
    else:
        nodes_data = pve_request("GET", "/nodes") or []
        nodes_to_query = [n.get("node") for n in nodes_data if n.get("status") == "online"]

    result = []
    for n in nodes_to_query:
        # QEMU VMs
        try:
            vms = pve_request("GET", f"/nodes/{n}/qemu") or []
            for vm in vms:
                result.append({
                    "vmid": vm.get("vmid"),
                    "name": vm.get("name"),
                    "type": "qemu",
                    "node": n,
                    "status": vm.get("status"),
                    "cpu_usage_pct": round(vm.get("cpu", 0) * 100, 1),
                    "mem_used_mb": round(vm.get("mem", 0) / 1024**2, 0),
                    "mem_max_mb": round(vm.get("maxmem", 0) / 1024**2, 0),
                    "uptime_h": round(vm.get("uptime", 0) / 3600, 1),
                })
        except RuntimeError:
            pass

        # LXC Containers
        try:
            lxcs = pve_request("GET", f"/nodes/{n}/lxc") or []
            for lxc in lxcs:
                result.append({
                    "vmid": lxc.get("vmid"),
                    "name": lxc.get("name"),
                    "type": "lxc",
                    "node": n,
                    "status": lxc.get("status"),
                    "cpu_usage_pct": round(lxc.get("cpu", 0) * 100, 1),
                    "mem_used_mb": round(lxc.get("mem", 0) / 1024**2, 0),
                    "mem_max_mb": round(lxc.get("maxmem", 0) / 1024**2, 0),
                    "uptime_h": round(lxc.get("uptime", 0) / 3600, 1),
                })
        except RuntimeError:
            pass

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def vm_status(node: str, vmid: int, vm_type: str = "qemu") -> str:
    """
    Gets the current status of a specific VM or LXC container.

    Args:
        node: PVE node name (e.g. 'pve', 'pve1', 'pve3')
        vmid: VM/LXC ID (e.g. 100)
        vm_type: 'qemu' for VMs or 'lxc' for containers (default: qemu)

    Returns:
        JSON with current status, cpu, memory, disk, network stats
    """
    path = f"/nodes/{node}/{vm_type}/{vmid}/status/current"
    status = pve_request("GET", path) or {}

    return json.dumps({
        "vmid": vmid,
        "node": node,
        "type": vm_type,
        "status": status.get("status"),
        "name": status.get("name"),
        "cpu_usage_pct": round(status.get("cpu", 0) * 100, 1),
        "mem_used_mb": round(status.get("mem", 0) / 1024**2, 1),
        "mem_max_mb": round(status.get("maxmem", 0) / 1024**2, 1),
        "disk_read_mb": round(status.get("diskread", 0) / 1024**2, 1),
        "disk_write_mb": round(status.get("diskwrite", 0) / 1024**2, 1),
        "net_in_mb": round(status.get("netin", 0) / 1024**2, 1),
        "net_out_mb": round(status.get("netout", 0) / 1024**2, 1),
        "uptime_h": round(status.get("uptime", 0) / 3600, 1),
        "ha_state": status.get("ha", {}).get("state") if status.get("ha") else None,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def vm_start(node: str, vmid: int, vm_type: str = "qemu") -> str:
    """
    Starts a stopped VM or LXC container.

    Args:
        node: PVE node name (e.g. 'pve', 'pve1', 'pve3')
        vmid: VM/LXC ID (e.g. 100)
        vm_type: 'qemu' for VMs or 'lxc' for containers (default: qemu)

    Returns:
        JSON with task ID (UPID) to track the start operation
    """
    path = f"/nodes/{node}/{vm_type}/{vmid}/status/start"
    upid = pve_request("POST", path)

    return json.dumps({
        "action": "start",
        "vmid": vmid,
        "node": node,
        "type": vm_type,
        "task_id": upid,
        "status": "started",
        "message": f"Start task queued: {upid}",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def vm_stop(node: str, vmid: int, vm_type: str = "qemu", graceful: bool = True) -> str:
    """
    Stops a running VM or LXC container.

    Args:
        node: PVE node name (e.g. 'pve', 'pve1', 'pve3')
        vmid: VM/LXC ID (e.g. 100)
        vm_type: 'qemu' for VMs or 'lxc' for containers (default: qemu)
        graceful: True = ACPI shutdown (recommended), False = force stop (default: True)

    Returns:
        JSON with task ID (UPID) to track the stop operation
    """
    if graceful and vm_type == "qemu":
        path = f"/nodes/{node}/{vm_type}/{vmid}/status/shutdown"
    else:
        path = f"/nodes/{node}/{vm_type}/{vmid}/status/stop"

    upid = pve_request("POST", path)

    return json.dumps({
        "action": "stop" if not graceful else "shutdown",
        "vmid": vmid,
        "node": node,
        "type": vm_type,
        "task_id": upid,
        "status": "queued",
        "message": f"Stop task queued: {upid}",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def vm_resources(node: str = None) -> str:
    """
    Returns a resource overview of all VMs/LXCs, sorted by CPU and RAM usage.
    Shows top consumers and cluster totals.

    Args:
        node: Optional — filter by node name (e.g. 'pve', 'pve1', 'pve3')

    Returns:
        JSON with cluster summary and top CPU/RAM consumers
    """
    nodes_to_query = []
    if node:
        nodes_to_query = [node]
    else:
        nodes_data = pve_request("GET", "/nodes") or []
        nodes_to_query = [n.get("node") for n in nodes_data if n.get("status") == "online"]

    all_vms = []
    total_cpu = 0.0
    total_mem = 0
    total_maxmem = 0
    running_count = 0

    for n in nodes_to_query:
        for vm_type in ("qemu", "lxc"):
            try:
                vms = pve_request("GET", f"/nodes/{n}/{vm_type}") or []
                for vm in vms:
                    cpu = vm.get("cpu", 0)
                    mem = vm.get("mem", 0)
                    maxmem = vm.get("maxmem", 0)
                    status = vm.get("status")

                    if status == "running":
                        total_cpu += cpu
                        total_mem += mem
                        total_maxmem += maxmem
                        running_count += 1

                    all_vms.append({
                        "vmid": vm.get("vmid"),
                        "name": vm.get("name"),
                        "node": n,
                        "type": vm_type,
                        "status": status,
                        "cpu_pct": round(cpu * 100, 1),
                        "mem_used_mb": round(mem / 1024**2, 0),
                        "mem_max_mb": round(maxmem / 1024**2, 0),
                    })
            except RuntimeError:
                pass

    running_vms = [v for v in all_vms if v["status"] == "running"]
    top_cpu = sorted(running_vms, key=lambda x: x["cpu_pct"], reverse=True)[:5]
    top_mem = sorted(running_vms, key=lambda x: x["mem_used_mb"], reverse=True)[:5]

    return json.dumps({
        "cluster_summary": {
            "running_vms": running_count,
            "total_vms": len(all_vms),
            "total_cpu_pct": round(total_cpu * 100, 1),
            "total_mem_used_gb": round(total_mem / 1024**3, 1),
            "total_mem_max_gb": round(total_maxmem / 1024**3, 1),
            "mem_pct": round(total_mem / total_maxmem * 100, 1) if total_maxmem > 0 else 0,
        },
        "top_cpu": top_cpu,
        "top_mem": top_mem,
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys

    if not PVE_PASSWORD:
        print("ERROR: PVE_PASSWORD environment variable not set!", file=sys.stderr)
        print("Example: export PVE_PASSWORD=yourpassword", file=sys.stderr)
        sys.exit(1)

    print(f"Proxmox MCP Server starting...", file=sys.stderr)
    print(f"Host: {PVE_HOST} | User: {PVE_USER}", file=sys.stderr)
    mcp.run()

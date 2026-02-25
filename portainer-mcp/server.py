#!/usr/bin/env python3
"""
Portainer MCP Server
Enables AI agents to manage Docker Swarm via Portainer's REST API.

Features:
- services/list   — List all Swarm services with replica status
- service/logs    — Get recent logs from a service
- stacks/list     — List all deployed stacks
- nodes/list      — List Swarm nodes with health status
- containers/list — List containers on an endpoint
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Any
from mcp.server.fastmcp import FastMCP

# Configuration
PORTAINER_URL = os.environ.get("PORTAINER_URL", "http://10.40.10.80:9000")
PORTAINER_USER = os.environ.get("PORTAINER_USER", "admin")
PORTAINER_PASSWORD = os.environ.get("PORTAINER_PASSWORD", "")
PORTAINER_ENDPOINT_ID = int(os.environ.get("PORTAINER_ENDPOINT_ID", "1"))

mcp = FastMCP("portainer-mcp")

_jwt_token: str | None = None


def _get_token() -> str:
    """Authenticate against Portainer and return JWT token."""
    global _jwt_token

    if not PORTAINER_PASSWORD:
        raise ValueError("PORTAINER_PASSWORD not set. Please set PORTAINER_PASSWORD environment variable.")

    payload = json.dumps({
        "username": PORTAINER_USER,
        "password": PORTAINER_PASSWORD,
    }).encode()

    req = urllib.request.Request(
        f"{PORTAINER_URL}/api/auth",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())

    _jwt_token = data.get("jwt")
    if not _jwt_token:
        raise RuntimeError(f"Portainer auth failed: {data}")
    return _jwt_token


def portainer_request(method: str, path: str, data: dict = None) -> Any:
    """HTTP request to Portainer API with auto-auth."""
    token = _get_token()

    url = f"{PORTAINER_URL}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise RuntimeError(f"Portainer API error {e.code}: {error_body}")


def docker_request(method: str, path: str) -> Any:
    """Request via Portainer Docker proxy to the Swarm endpoint."""
    return portainer_request(method, f"/api/endpoints/{PORTAINER_ENDPOINT_ID}/docker{path}")


@mcp.tool()
def services_list() -> str:
    """
    Lists all Docker Swarm services with replica counts and image info.

    Returns:
        JSON list of services with name, image, replicas (running/desired), and update status
    """
    services = docker_request("GET", "/services") or []

    result = []
    for s in services:
        spec = s.get("Spec", {})
        mode = spec.get("Mode", {})
        status = s.get("ServiceStatus", {})
        replicated = mode.get("Replicated", {})

        result.append({
            "id": s.get("ID", "")[:12],
            "name": spec.get("Name"),
            "image": spec.get("TaskTemplate", {}).get("ContainerSpec", {}).get("Image", "").split("@")[0],
            "mode": "replicated" if "Replicated" in mode else "global",
            "replicas_desired": replicated.get("Replicas"),
            "replicas_running": status.get("RunningTasks"),
            "replicas_desired_from_status": status.get("DesiredTasks"),
            "update_state": s.get("UpdateStatus", {}).get("State"),
        })

    result.sort(key=lambda x: x["name"] or "")

    return json.dumps({
        "services": result,
        "total": len(result),
        "endpoint_id": PORTAINER_ENDPOINT_ID,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def service_logs(service_name: str, tail: int = 50) -> str:
    """
    Gets recent log lines from a Docker Swarm service.

    Args:
        service_name: Full service name (e.g. 'monitoring_grafana', 'agents_service-monitor')
        tail: Number of recent log lines to return (default: 50, max: 500)

    Returns:
        JSON with log lines and service metadata
    """
    # First find service ID by name
    services = docker_request("GET", "/services") or []
    service_id = None
    for s in services:
        if s.get("Spec", {}).get("Name") == service_name:
            service_id = s.get("ID")
            break

    if not service_id:
        raise RuntimeError(f"Service '{service_name}' not found. Use services_list() to get valid names.")

    tail_count = min(tail, 500)
    token = _get_token()
    url = f"{PORTAINER_URL}/api/endpoints/{PORTAINER_ENDPOINT_ID}/docker/services/{service_id}/logs?stdout=true&stderr=true&tail={tail_count}&timestamps=true"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Log fetch error {e.code}: {e.read().decode()}")

    # Docker multiplexed stream: each chunk has 8-byte header
    lines = []
    i = 0
    data = raw.encode("latin-1")
    while i + 8 <= len(data):
        frame_size = int.from_bytes(data[i+4:i+8], "big")
        if frame_size == 0:
            i += 8
            continue
        frame_data = data[i+8:i+8+frame_size]
        lines.append(frame_data.decode("utf-8", errors="replace").rstrip())
        i += 8 + frame_size

    if not lines:
        # Fallback: plain text (some Portainer versions don't multiplex)
        lines = [l for l in raw.splitlines() if l.strip()]

    return json.dumps({
        "service": service_name,
        "lines_returned": len(lines),
        "logs": lines[-tail_count:],
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def stacks_list() -> str:
    """
    Lists all deployed Docker Swarm stacks by inspecting service labels.

    Returns:
        JSON list of stacks with name, service count, and list of services
    """
    services = docker_request("GET", "/services") or []

    stacks: dict[str, list] = {}
    for s in services:
        spec = s.get("Spec", {})
        labels = spec.get("Labels", {})
        stack_name = labels.get("com.docker.stack.namespace")
        if stack_name:
            stacks.setdefault(stack_name, []).append(spec.get("Name"))

    result = [
        {
            "name": stack_name,
            "service_count": len(svcs),
            "services": sorted(svcs),
        }
        for stack_name, svcs in sorted(stacks.items())
    ]

    return json.dumps({
        "stacks": result,
        "total": len(result),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def nodes_list() -> str:
    """
    Lists all Docker Swarm nodes with health and availability status.

    Returns:
        JSON list of nodes with hostname, role, status, availability, and engine version
    """
    nodes = docker_request("GET", "/nodes") or []

    result = []
    for n in nodes:
        spec = n.get("Spec", {})
        status = n.get("Status", {})
        manager_status = n.get("ManagerStatus", {})
        description = n.get("Description", {})

        result.append({
            "id": n.get("ID", "")[:12],
            "hostname": description.get("Hostname"),
            "role": spec.get("Role"),
            "availability": spec.get("Availability"),
            "state": status.get("State"),
            "addr": status.get("Addr"),
            "manager_reachability": manager_status.get("Reachability") if manager_status else None,
            "is_leader": manager_status.get("Leader", False) if manager_status else False,
            "engine_version": description.get("Engine", {}).get("EngineVersion"),
        })

    return json.dumps({
        "nodes": result,
        "total": len(result),
        "leaders": [n["hostname"] for n in result if n["is_leader"]],
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def containers_list(all_containers: bool = False) -> str:
    """
    Lists containers on the Docker endpoint.

    Args:
        all_containers: True = include stopped containers (default: False = running only)

    Returns:
        JSON list of containers with name, image, status, and ports
    """
    all_param = "true" if all_containers else "false"
    containers = docker_request("GET", f"/containers/json?all={all_param}") or []

    result = []
    for c in containers:
        ports = {}
        for binding_key, bindings in (c.get("Ports") or {}).items() if isinstance(c.get("Ports"), dict) else []:
            if bindings:
                ports[binding_key] = [f"{b.get('HostIp', '')}:{b.get('HostPort', '')}" for b in bindings]

        # Handle list format for ports
        port_list = []
        if isinstance(c.get("Ports"), list):
            for p in c.get("Ports", []):
                if p.get("PublicPort"):
                    port_list.append(f"{p.get('IP', '0.0.0.0')}:{p['PublicPort']}->{p['PrivatePort']}/{p.get('Type', 'tcp')}")

        result.append({
            "id": c.get("Id", "")[:12],
            "names": [n.lstrip("/") for n in c.get("Names", [])],
            "image": c.get("Image", "").split("@")[0],
            "status": c.get("Status"),
            "state": c.get("State"),
            "ports": port_list,
        })

    result.sort(key=lambda x: x["names"][0] if x["names"] else "")

    return json.dumps({
        "containers": result,
        "total": len(result),
        "running": sum(1 for c in result if c["state"] == "running"),
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys

    if not PORTAINER_PASSWORD:
        print("ERROR: PORTAINER_PASSWORD environment variable not set!", file=sys.stderr)
        print("Example: export PORTAINER_PASSWORD=yourpassword", file=sys.stderr)
        sys.exit(1)

    print(f"Portainer MCP Server starting...", file=sys.stderr)
    print(f"Portainer: {PORTAINER_URL} | Endpoint: {PORTAINER_ENDPOINT_ID}", file=sys.stderr)
    mcp.run()

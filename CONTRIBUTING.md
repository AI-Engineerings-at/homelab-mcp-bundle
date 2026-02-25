# Contributing to homelab-mcp-bundle

Thank you for your interest in contributing! This guide covers everything you need to add a new MCP server, follow the project's code style, test locally, and submit a pull request.

---

## Table of Contents

1. [Adding a New MCP Server](#adding-a-new-mcp-server)
2. [Code Style Guidelines](#code-style-guidelines)
3. [Testing Locally](#testing-locally)
4. [PR Checklist](#pr-checklist)
5. [Reporting Bugs & Requesting Features](#reporting-bugs--requesting-features)

---

## Adding a New MCP Server

Use `portainer-mcp` as the reference template. Every server in this bundle follows the same structure.

### Step 1 — Create the directory

```bash
mkdir your-service-mcp
cd your-service-mcp
```

### Step 2 — Create `server.py`

Start from this skeleton (mirrors `portainer-mcp/server.py`):

```python
#!/usr/bin/env python3
"""
YourService MCP Server
Enables AI agents to interact with YourService via its REST API.

Features:
- resource/list  — List all resources
- resource/get   — Get details for a specific resource
- resource/action — Perform an action on a resource
"""

import os
import json
import urllib.request
from typing import Any
from mcp.server.fastmcp import FastMCP

# Configuration — always use os.environ.get() with a sensible default
YOUR_SERVICE_URL = os.environ.get("YOUR_SERVICE_URL", "http://localhost:8080")
YOUR_SERVICE_TOKEN = os.environ.get("YOUR_SERVICE_TOKEN", "")

mcp = FastMCP("your-service-mcp")


def your_service_request(method: str, path: str, data: dict = None) -> Any:
    """HTTP request to YourService API."""
    if not YOUR_SERVICE_TOKEN:
        raise ValueError("YOUR_SERVICE_TOKEN not set.")

    url = f"{YOUR_SERVICE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {YOUR_SERVICE_TOKEN}",
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise RuntimeError(f"API error {e.code}: {error_body}")


@mcp.tool()
def resources_list() -> str:
    """List all resources from YourService."""
    data = your_service_request("GET", "/api/resources")
    lines = [f"Found {len(data)} resources:"]
    for item in data:
        lines.append(f"  - {item['name']} ({item['status']})")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
```

### Step 3 — Create `requirements.txt`

```
mcp
```

Only add additional packages if absolutely necessary. The goal is zero external dependencies beyond `mcp`.

### Step 4 — Create `README.md`

Follow the `portainer-mcp/README.md` structure:

1. Short description (one sentence)
2. Available tools (table with tool name, description)
3. Configuration (environment variables table)
4. Claude Desktop config snippet
5. Natural language examples

### Step 5 — Add to the root `README.md`

Add a row to the "What's Inside" table and a line to the Claude Desktop config example in the main README.

### Step 6 — Open a Pull Request

See the [PR Checklist](#pr-checklist) below.

---

## Code Style Guidelines

### Framework

All servers use **FastMCP** from the `mcp` library:

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("your-service-mcp")
```

### Type Hints

All functions must have type hints on parameters and return values:

```python
# Good
def get_node_status(node_id: str) -> str:
    ...

# Bad
def get_node_status(node_id):
    ...
```

### Docstrings

Every tool function needs a docstring. The docstring becomes the tool description that Claude sees — make it clear and action-oriented:

```python
@mcp.tool()
def services_list() -> str:
    """List all running Docker Swarm services with replica count and status."""
    ...
```

Multi-line docstrings for tools with parameters:

```python
@mcp.tool()
def service_logs(service_name: str, lines: int = 50) -> str:
    """
    Get recent log output from a Docker Swarm service.

    Args:
        service_name: Name of the service (e.g. 'n8n_n8n')
        lines: Number of log lines to return (default: 50)
    """
    ...
```

### HTTP Requests

Use **only the standard library** (`urllib.request`) — no `requests`, no `httpx`:

```python
import urllib.request
import urllib.parse
```

This keeps the dependency footprint at zero (beyond `mcp` itself).

### Configuration

Always read from environment variables with `os.environ.get()`:

```python
SERVICE_URL = os.environ.get("SERVICE_URL", "http://localhost:8080")
SERVICE_TOKEN = os.environ.get("SERVICE_TOKEN", "")
```

Provide sensible defaults where possible. Raise a clear `ValueError` if a required variable is missing:

```python
if not SERVICE_TOKEN:
    raise ValueError("SERVICE_TOKEN not set. Please set SERVICE_TOKEN environment variable.")
```

### Error Handling

Catch `urllib.error.HTTPError` and re-raise as `RuntimeError` with the status code and body:

```python
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())
except urllib.error.HTTPError as e:
    error_body = e.read().decode()
    raise RuntimeError(f"API error {e.code}: {error_body}")
```

### Return Format

Tools return plain strings. Format output to be human-readable (Claude will present it directly):

```python
lines = [f"Found {len(items)} services:"]
for svc in items:
    lines.append(f"  - {svc['name']}: {svc['replicas']}/{svc['desired']} replicas")
return "\n".join(lines)
```

### File Header

Every `server.py` starts with the shebang and a module docstring listing all features:

```python
#!/usr/bin/env python3
"""
ServiceName MCP Server
One-line description.

Features:
- tool/name  — What it does
"""
```

---

## Testing Locally

### 1. Install dependencies

```bash
pip install mcp
# or
python3 -m venv .venv && source .venv/bin/activate && pip install mcp
```

### 2. Set environment variables

```bash
export YOUR_SERVICE_URL="http://your-service:8080"
export YOUR_SERVICE_TOKEN="your-token"
```

### 3. Run the server directly

```bash
python3 your-service-mcp/server.py
```

The server starts and waits for MCP stdio input. You won't see output — this is correct. If it crashes immediately, the error will be printed to stderr.

### 4. Test with Claude Desktop

Add your server to `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "your-service": {
      "command": "python3",
      "args": ["/absolute/path/to/homelab-mcp-bundle/your-service-mcp/server.py"],
      "env": {
        "YOUR_SERVICE_URL": "http://your-service:8080",
        "YOUR_SERVICE_TOKEN": "your-token"
      }
    }
  }
}
```

Restart Claude Desktop. The tools appear automatically. Ask Claude: "List all [your resource type]" to verify.

### 5. Check for errors

On macOS/Linux, Claude Desktop logs MCP server stderr output. Check:

```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp-server-your-service.log

# Linux
journalctl --user -f | grep your-service
```

---

## PR Checklist

Before opening a pull request, verify all of the following:

- [ ] **New directory** follows the naming convention: `service-name-mcp/`
- [ ] **`server.py`** present with shebang (`#!/usr/bin/env python3`) and module docstring
- [ ] **All tool functions** have type hints on all parameters and the return value
- [ ] **All tool functions** have a docstring (this is the description Claude sees)
- [ ] **`requirements.txt`** present — only `mcp` unless absolutely unavoidable
- [ ] **`README.md`** present with tool list, env var table, and Claude Desktop config snippet
- [ ] **Root `README.md`** updated — new row in the "What's Inside" table
- [ ] **Root `README.md`** updated — Claude Desktop config example includes the new server
- [ ] **No hardcoded credentials** — all secrets via `os.environ.get()`
- [ ] **Error handling** on all HTTP calls using `urllib.error.HTTPError`
- [ ] **Tested locally** against a real (or mock) instance of the service
- [ ] **PR title** follows the format: `feat: add service-name-mcp` or `fix: portainer-mcp timeout on large logs`

---

## Reporting Bugs & Requesting Features

### Bug Reports

Open an issue with the following information:

1. **Which server**: e.g. `portainer-mcp`
2. **What you expected**: "Should list all stacks"
3. **What happened**: Exact error message or unexpected output
4. **Your setup**: Service version (e.g. Portainer 2.19), Python version, OS
5. **Minimal reproduction**: The natural language prompt you used in Claude Desktop

### Feature Requests

Open an issue with:

1. **Which server** (or "new server: service-name")
2. **What you want to do**: "I want to be able to restart a Proxmox VM from Claude"
3. **The API endpoint**: Link to the service's API docs if available
4. **Priority**: Nice to have / Blocker for my use case

We prioritize features that work with commonly self-hosted, open-source services.

---

*Questions? Open an issue or start a Discussion on GitHub.*

# Proxmox MCP Server

**Manage your Proxmox VE homelab or datacenter from any MCP-capable AI assistant.**

> Built by [AI-Engineering.at](https://ai-engineering.at) — Self-Hosted AI Infrastructure.

---

## What is this?

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that gives AI assistants
(Claude, Cursor, etc.) direct access to your [Proxmox VE](https://www.proxmox.com/en/proxmox-virtual-environment/overview) cluster.

**Ask your AI to check VM health, inspect node resources, or start/stop virtual machines — in plain language.**

---

## Tools (8)

| Tool | Description |
|------|-------------|
| `get_cluster_status` | Cluster health, quorum, node count |
| `list_nodes` | All nodes with CPU%, memory%, uptime |
| `get_node_status` | Detailed resource usage for one node |
| `list_vms` | All QEMU VMs on a node with status |
| `list_lxc` | All LXC containers on a node |
| `get_vm_status` | Runtime status of a specific VM |
| `start_vm` | Start a stopped VM |
| `stop_vm` | Gracefully shut down a VM |

---

## Requirements

- Python 3.11+
- Proxmox VE 7.x or newer
- API user with at least `VM.Audit`, `Sys.Audit` privileges (read-only)
- For start/stop: `VM.PowerMgmt` privilege

---

## Quick Start

```bash
# 1. Install
pip install -e .

# 2. Configure
export PVE_HOST=https://your-proxmox-ip:8006
export PVE_USER=root@pam
export PVE_PASSWORD=your_password
export PVE_VERIFY_SSL=false   # for self-signed certs

# 3. Run
proxmox-mcp
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PVE_HOST` | *(required)* | Proxmox API URL, e.g. `https://10.0.0.1:8006` |
| `PVE_USER` | `root@pam` | Proxmox user (realm included) |
| `PVE_PASSWORD` | *(required)* | User password |
| `PVE_VERIFY_SSL` | `true` | Set `false` for self-signed certificates |

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "proxmox": {
      "command": "proxmox-mcp",
      "env": {
        "PVE_HOST": "https://YOUR_PVE_IP:8006",
        "PVE_USER": "root@pam",
        "PVE_PASSWORD": "your_password",
        "PVE_VERIFY_SSL": "false"
      }
    }
  }
}
```

### Claude Code CLI

```bash
claude mcp add proxmox proxmox-mcp \
  -e PVE_HOST=https://YOUR_PVE_IP:8006 \
  -e PVE_USER=root@pam \
  -e PVE_PASSWORD=your_password \
  -e PVE_VERIFY_SSL=false
```

---

## Example Prompts

```
"Show me all VMs and their CPU usage"
"Is the cluster healthy? Any nodes offline?"
"What's the memory usage on node pve3?"
"Start VM 100 on node pve"
"List all LXC containers on pve1"
"Which VMs are currently stopped?"
```

---

## Authentication

Uses Proxmox ticket-based auth (username + password → PVEAuthCookie).
Tickets are cached and auto-renewed on 401 responses.

**Security tip**: For production, create a dedicated API user with minimal permissions:

```bash
# On Proxmox shell
pveum user add mcp-reader@pam
pveum passwd mcp-reader@pam
pveum acl modify / -user mcp-reader@pam -role PVEAuditor
```

---

## Roadmap (v0.2+)

- [ ] `create_vm` — Clone from template
- [ ] `get_vm_config` — Full VM configuration
- [ ] `list_storage` — Storage pools and usage
- [ ] `get_task_status` — Monitor async PVE tasks
- [ ] API token support (no password required)
- [ ] Multi-cluster support

---

## License

MIT — use freely, modify and resell.

---

*Made with love by the AI-Engineering.at team.*

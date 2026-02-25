# 🏠 Homelab MCP Bundle — 8 Free MCP Servers for Claude Desktop

**Control your entire homelab through natural language. No more switching tabs.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Claude%20Desktop-green.svg)](https://modelcontextprotocol.io/)

> "Show me all running Docker services" → Portainer MCP: 22 services listed in 0.3s
>
> "Block ads.example.com" → AdGuard MCP: rule added
>
> "Are all monitors up?" → Uptime Kuma MCP: 28/28 UP ✅

---

## What's Inside

8 production-tested MCP servers covering the most common self-hosted stack:

| Server | Tools | What you can do |
|--------|-------|-----------------|
| [portainer-mcp](./portainer-mcp/) | 5 | List Docker Swarm services, stacks, nodes, read logs |
| [proxmox-mcp](./proxmox-mcp/) | 6 | List VMs/LXCs, check node resources, start/stop/reboot |
| [n8n-mcp](./n8n-mcp/) | 5 | List workflows, trigger executions, check failed runs |
| [ollama-mcp](./ollama-mcp/) | 4 | Generate text, chat, list local models, pull new ones |
| [uptime-kuma-mcp](./uptime-kuma-mcp/) | 3 | Check service status, uptime %, monitor dashboard |
| [mattermost-mcp](./mattermost-mcp/) | 5 | Read/write channels, search posts, list users |
| [adguard-mcp](./adguard-mcp/) | 6 | DNS stats, query log, filter lists, block/unblock domains |
| [grafana-mcp](./grafana-mcp/) | 6 | Query dashboards, run PromQL, check alerts, add annotations |

**40 tools total — all with zero external dependencies beyond `mcp`**

---

## Quick Install

### 1. Install the MCP library

```bash
pip install mcp
# or in a virtual environment:
python3 -m venv .venv && source .venv/bin/activate && pip install mcp
```

### 2. Clone this repo

```bash
git clone https://github.com/AI-Engineerings-at/homelab-mcp-bundle.git
cd homelab-mcp-bundle
```

### 3. Configure Claude Desktop

Edit `~/.config/claude/claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "portainer": {
      "command": "python3",
      "args": ["/path/to/homelab-mcp-bundle/portainer-mcp/server.py"],
      "env": {
        "PORTAINER_URL": "http://your-portainer:9000",
        "PORTAINER_USER": "admin",
        "PORTAINER_PASSWORD": "your-password"
      }
    },
    "proxmox": {
      "command": "python3",
      "args": ["/path/to/homelab-mcp-bundle/proxmox-mcp/server.py"],
      "env": {
        "PVE_HOST": "your-proxmox-ip",
        "PVE_USER": "root@pam",
        "PVE_PASSWORD": "your-password"
      }
    },
    "n8n": {
      "command": "python3",
      "args": ["/path/to/homelab-mcp-bundle/n8n-mcp/server.py"],
      "env": {
        "N8N_API_KEY": "your-n8n-api-key",
        "N8N_BASE_URL": "http://your-n8n:5678/api/v1"
      }
    },
    "ollama": {
      "command": "python3",
      "args": ["/path/to/homelab-mcp-bundle/ollama-mcp/server.py"],
      "env": {
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "OLLAMA_DEFAULT_MODEL": "llama3.2:3b"
      }
    },
    "uptime-kuma": {
      "command": "python3",
      "args": ["/path/to/homelab-mcp-bundle/uptime-kuma-mcp/server.py"],
      "env": {
        "KUMA_BASE_URL": "http://your-uptime-kuma:3001",
        "KUMA_STATUS_PAGE": "homelab"
      }
    },
    "mattermost": {
      "command": "python3",
      "args": ["/path/to/homelab-mcp-bundle/mattermost-mcp/server.py"],
      "env": {
        "MM_TOKEN": "your-mattermost-bot-token",
        "MM_BASE_URL": "http://your-mattermost:8065/api/v4"
      }
    },
    "adguard": {
      "command": "python3",
      "args": ["/path/to/homelab-mcp-bundle/adguard-mcp/server.py"],
      "env": {
        "ADGUARD_URL": "http://your-adguard:3000",
        "ADGUARD_USER": "admin",
        "ADGUARD_PASSWORD": "your-password"
      }
    },
    "grafana": {
      "command": "python3",
      "args": ["/path/to/homelab-mcp-bundle/grafana-mcp/server.py"],
      "env": {
        "GRAFANA_URL": "http://your-grafana:3000",
        "GRAFANA_API_KEY": "your-grafana-api-key"
      }
    }
  }
}
```

Restart Claude Desktop — the servers will appear as tools automatically.

---

## What You Can Say to Claude

```
"Show me all VMs on my Proxmox cluster"
→ proxmox-mcp: vms_list() → 12 VMs/LXCs across 3 nodes

"Are all my services up?"
→ uptime-kuma-mcp: monitors_status() → 28/28 UP

"Which n8n workflows failed today?"
→ n8n-mcp: executions_list(status="error") → 2 failed

"Write to #general: Deployment is done"
→ mattermost-mcp: posts_create(channel="general", message="Deployment is done")

"Generate a 3-sentence summary of this log with llama3"
→ ollama-mcp: generate(prompt="...", model="llama3.2:3b")

"Show me all running Docker Swarm services"
→ portainer-mcp: services_list() → 22 services

"How many DNS queries were blocked today?"
→ adguard-mcp: stats() → 45,230 queries | 12,847 blocked (28.4%)

"Block ads.example.com"
→ adguard-mcp: block_domain("ads.example.com") → Rule added

"Show me the current Grafana alerts"
→ grafana-mcp: alerts_list() → 1 firing: HighMemory on node-1
```

---

## Architecture

```
Claude Desktop
     |
     +-- portainer-mcp  -->  Portainer REST API --> Docker Swarm
     +-- proxmox-mcp    -->  Proxmox VE API (HTTPS, cookie auth)
     +-- n8n-mcp        -->  n8n REST API v1
     +-- ollama-mcp     -->  Ollama API (local LLMs)
     +-- uptime-kuma-mcp-->  Uptime Kuma Status Page API
     +-- mattermost-mcp -->  Mattermost REST API v4
     +-- adguard-mcp    -->  AdGuard Home REST API
     +-- grafana-mcp    -->  Grafana HTTP API (dashboards, PromQL, alerts)
```

Each server runs as a local process started by Claude Desktop. Communication is via stdio using the MCP protocol. No cloud dependencies, no proxies — direct API calls to your self-hosted services.

---

## Requirements

- Python 3.10+
- `pip install mcp` (the only dependency)
- Running instances of the services you want to connect

Each server works independently — use only the ones you need.

---

## Individual Server Docs

- [Portainer MCP](./portainer-mcp/README.md)
- [Proxmox MCP](./proxmox-mcp/README.md)
- [n8n MCP](./n8n-mcp/README.md)
- [Ollama MCP](./ollama-mcp/README.md)
- [Uptime Kuma MCP](./uptime-kuma-mcp/README.md)
- [Mattermost MCP](./mattermost-mcp/README.md)
- [AdGuard Home MCP](./adguard-mcp/README.md)
- [Grafana MCP](./grafana-mcp/README.md)

---

## Want the Full Homelab AI Stack?

This bundle is part of **Playbook 01 — Der Lokale AI-Stack**, a complete guide to building a production-grade, self-hosted AI infrastructure with Docker Swarm, n8n automation, Grafana monitoring, and Claude Desktop integration.

**[Get the full Playbook at ai-engineering.at](https://www.ai-engineering.at)**

Includes:
- Complete Docker Swarm setup (Portainer, Grafana, Prometheus, n8n, Ollama)
- 13 ready-to-import n8n AI workflows
- 22 Grafana dashboards for homelab monitoring
- AIOps alert pipeline with LLM analysis
- Step-by-step setup guide (DE/EN)

---

## License

MIT — see [LICENSE](./LICENSE)

Free to use, modify, and distribute. Attribution appreciated but not required.

---

## Contributing

Issues and PRs welcome. If you add a new MCP server for a self-hosted service, open a PR!

Star this repo if it saved you time. It helps others find it.

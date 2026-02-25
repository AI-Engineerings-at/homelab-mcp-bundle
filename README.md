# Homelab MCP Bundle — 8 Free MCP Servers for Claude Desktop

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/AI-Engineerings-at/homelab-mcp-bundle?style=flat&color=gold)](https://github.com/AI-Engineerings-at/homelab-mcp-bundle/stargazers)
[![MCP Compatible](https://img.shields.io/badge/MCP-Claude%20Desktop-brightgreen.svg)](https://modelcontextprotocol.io/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

**Control your entire homelab through natural language. No more switching tabs.**

Ask Claude "Are all my services up?" and get a live status across Portainer, Uptime Kuma, Proxmox, n8n, AdGuard, Grafana, Ollama, and Mattermost — all from one conversation.

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

Edit `~/.config/claude/claude_desktop_config.json`
(macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`)

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

Restart Claude Desktop — the servers appear as tools automatically.

---

## What's Inside

8 production-tested MCP servers. 40 tools. Zero external dependencies beyond `mcp`.

| Server | Tools | What you can say |
|--------|:-----:|-----------------|
| [portainer-mcp](./portainer-mcp/) | 5 | "Show all running Docker Swarm services" / "Which container has the most restarts?" / "Tail the logs for my n8n service" |
| [proxmox-mcp](./proxmox-mcp/) | 6 | "List all VMs across my cluster" / "How loaded is pve3 right now?" / "Reboot the UbuntuDesktop VM" |
| [n8n-mcp](./n8n-mcp/) | 5 | "Which workflows failed today?" / "Trigger the daily report workflow" / "Show me all active automations" |
| [ollama-mcp](./ollama-mcp/) | 4 | "Summarize this log file with llama3" / "What models do I have locally?" / "Pull mistral:7b" |
| [uptime-kuma-mcp](./uptime-kuma-mcp/) | 3 | "Are all my services up?" / "What's the uptime for Grafana this month?" / "Show me anything that's currently down" |
| [mattermost-mcp](./mattermost-mcp/) | 5 | "Post 'Deployment done' to #general" / "What did the team write in #devops today?" / "Search for messages about the last outage" |
| [adguard-mcp](./adguard-mcp/) | 6 | "How many DNS queries were blocked today?" / "Block ads.youtube-nocookie.com" / "What's my current blocklist count?" |
| [grafana-mcp](./grafana-mcp/) | 6 | "Are there any firing alerts?" / "Run a PromQL query for CPU usage" / "Add an annotation to the dashboard for tonight's maintenance" |

---

## How It Works

Each MCP server runs as a local Python process started and managed by Claude Desktop. Claude sends tool calls via the MCP protocol (stdio), and each server translates them into direct REST API calls to your self-hosted service.

```
Claude Desktop (your laptop)
        |
        +--[stdio]--> portainer-mcp  --[HTTP]--> Portainer  --> Docker Swarm
        +--[stdio]--> proxmox-mcp    --[HTTPS]--> Proxmox VE API
        +--[stdio]--> n8n-mcp        --[HTTP]--> n8n REST API v1
        +--[stdio]--> ollama-mcp     --[HTTP]--> Ollama (local LLMs)
        +--[stdio]--> uptime-kuma-mcp --[HTTP]--> Uptime Kuma Status API
        +--[stdio]--> mattermost-mcp --[HTTP]--> Mattermost REST API v4
        +--[stdio]--> adguard-mcp    --[HTTP]--> AdGuard Home REST API
        +--[stdio]--> grafana-mcp    --[HTTP]--> Grafana HTTP API + PromQL
```

No cloud. No proxy. No data leaves your network. Each server is independent — use only the ones that match your stack.

---

## Requirements

- **Claude Desktop** (with MCP support enabled)
- **Python 3.9+** and `pip install mcp` (the only library dependency)
- **Self-hosted services** you want to connect:
  - Portainer CE or BE (Docker Swarm or standalone)
  - Proxmox VE (any recent version)
  - n8n (self-hosted, API key enabled)
  - Ollama (local LLM runtime)
  - Uptime Kuma (status page configured)
  - Mattermost (self-hosted, bot token)
  - AdGuard Home
  - Grafana + Prometheus

You don't need all of them — each server is fully independent.

---

## Natural Language Examples

```
"Show me all VMs on my Proxmox cluster"
  -> proxmox-mcp: vms_list() -> 12 VMs/LXCs across 3 nodes

"Are all my services up?"
  -> uptime-kuma-mcp: monitors_status() -> 28/28 UP

"Which n8n workflows failed today?"
  -> n8n-mcp: executions_list(status="error") -> 2 failed

"Write to #general: Deployment is done"
  -> mattermost-mcp: posts_create(channel="general", ...) -> Posted

"Summarize this error log with llama3"
  -> ollama-mcp: generate(prompt="...", model="llama3.2:3b") -> Summary

"Show me all running Docker Swarm services"
  -> portainer-mcp: services_list() -> 22 services across 3 nodes

"How many DNS queries were blocked today?"
  -> adguard-mcp: stats() -> 45,230 queries | 12,847 blocked (28.4%)

"Block ads.example.com"
  -> adguard-mcp: block_domain("ads.example.com") -> Rule added

"Show current Grafana alerts"
  -> grafana-mcp: alerts_list() -> 1 firing: HighMemory on node-1
```

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

## Get the Full Homelab AI Stack

This bundle is part of **Playbook 01 — Der Lokale AI-Stack**, a complete guide to building a production-grade, self-hosted AI infrastructure with Docker Swarm, n8n automation, Grafana monitoring, and Claude Desktop integration.

**[Get Playbook 01 at ai-engineering.at](https://www.ai-engineering.at)**

Includes:
- Complete Docker Swarm setup (Portainer, Grafana, Prometheus, n8n, Ollama)
- 13 ready-to-import n8n AI automation workflows
- 22 Grafana dashboards for homelab monitoring
- AIOps alert pipeline with local LLM analysis
- Step-by-step setup guide (70 pages, DE/EN)

---

## License

MIT — see [LICENSE](./LICENSE)

Free to use, modify, and distribute. Attribution appreciated but not required.

---

## Contributing

Issues and PRs welcome. If you add a new MCP server for a self-hosted service, open a PR!

Star this repo if it saved you time. It helps others find it.

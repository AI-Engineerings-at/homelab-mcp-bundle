# MCP Server Bundle — Self-Hosted AI Infrastructure

**6 production-ready MCP servers for self-hosted homelab and infrastructure.**

> Built by [AI-Engineering.at](https://ai-engineering.at)

Give your AI assistant (Claude, Cursor, Windsurf, ...) full access to your self-hosted stack:
Mattermost, n8n, Proxmox, Uptime Kuma, Ollama and Portainer — all via the [Model Context Protocol](https://modelcontextprotocol.io).

---

## The Bundle

| Server | Tools | What it does |
|--------|-------|-------------|
| [mattermost-mcp](./mattermost-mcp/) | 7 | Read channels, post messages, search across your Mattermost workspace |
| [n8n-mcp](./n8n-mcp/) | 7 | Manage workflows, check executions, trigger webhooks in n8n |
| [proxmox-mcp](./proxmox-mcp/) | 8 | Monitor nodes, list VMs, start/stop virtual machines in Proxmox VE |
| [uptime-kuma-mcp](./uptime-kuma-mcp/) | 5 | Query service health, incidents and response times from Uptime Kuma |
| [ollama-mcp](./ollama-mcp/) | 4 | List models, generate text, chat and pull models from Ollama |
| [portainer-mcp](./portainer-mcp/) | 6 | Manage Docker Swarm — services, stacks, nodes, containers and logs |

**Total: 37 tools** across 6 servers.

---

## Why this bundle?

Most MCP servers target cloud services (GitHub, Notion, Slack).
This bundle is for people running their own infrastructure:

- **Self-hosted chat** (Mattermost, not Slack)
- **Self-hosted automation** (n8n, not Zapier)
- **Self-hosted VMs** (Proxmox, not AWS)
- **Self-hosted monitoring** (Uptime Kuma, not Datadog)
- **Local LLMs** (Ollama, not OpenAI)

---

## Quick Start — All 5 Servers

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mattermost": {
      "command": "python3",
      "args": ["/path/to/mattermost-mcp/src/mattermost_mcp/server.py"],
      "env": {
        "MM_BASE_URL": "https://your-mattermost.example.com",
        "MM_TOKEN":    "your_personal_access_token",
        "MM_TEAM_ID":  "your_team_id"
      }
    },
    "n8n": {
      "command": "python",
      "args": ["-m", "n8n_mcp.server"],
      "env": {
        "N8N_BASE_URL": "http://your-n8n-host:5678",
        "N8N_API_KEY":  "your_api_key"
      }
    },
    "proxmox": {
      "command": "proxmox-mcp",
      "env": {
        "PVE_HOST":       "https://YOUR_PVE_IP:8006",
        "PVE_USER":       "root@pam",
        "PVE_PASSWORD":   "your_password",
        "PVE_VERIFY_SSL": "false"
      }
    },
    "uptime-kuma": {
      "command": "uptime-kuma-mcp",
      "env": {
        "KUMA_BASE_URL": "http://YOUR_KUMA_IP:3001",
        "KUMA_USERNAME": "your_username",
        "KUMA_PASSWORD": "your_password"
      }
    },
    "ollama": {
      "command": "python3",
      "args": ["/path/to/ollama-mcp/src/ollama_mcp/server.py"],
      "env": {
        "OLLAMA_BASE_URL": "http://localhost:11434"
      }
    },
    "portainer": {
      "command": "python3",
      "args": ["-m", "portainer_mcp.server"],
      "env": {
        "PORTAINER_URL":         "http://YOUR_PORTAINER_IP:9000",
        "PORTAINER_API_TOKEN":   "ptr_your_token_here",
        "PORTAINER_ENDPOINT_ID": "1"
      }
    }
  }
}
```

---

## Installation

```bash
# Clone the repo
git clone https://github.com/AI-Engineerings-at/Playbook01
cd Playbook01/mcp-servers

# Install all servers
pip install -e mattermost-mcp/
pip install -e n8n-mcp/
pip install -e proxmox-mcp/
pip install -e uptime-kuma-mcp/
pip install -e ollama-mcp/
pip install -e portainer-mcp/
```

---

## What can you do with all 6?

Once connected, you can have conversations like:

> *"Check if all services are UP, and if Grafana is down, restart it on the Proxmox VM."*

> *"Post a summary of today's n8n workflow failures to the #ops channel in Mattermost."*

> *"Which Ollama models do I have? Run the infrastructure-check prompt on llama3.1:8b."*

> *"Show me all stopped VMs in Proxmox and tell me if any critical monitors are down in Uptime Kuma."*

> *"List all Swarm services in Portainer — which ones have fewer replicas than expected?"*

> *"Get the last 100 log lines from the agents_service-monitor container."*

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.11+ |
| Claude Desktop / Cursor / Windsurf | Latest |
| MCP SDK (`mcp`) | 1.0+ |

Each server has its own additional requirements — see individual READMEs.

---

## Server Details

- [Mattermost MCP →](./mattermost-mcp/README.md)
- [n8n MCP →](./n8n-mcp/README.md)
- [Proxmox MCP →](./proxmox-mcp/README.md)
- [Uptime Kuma MCP →](./uptime-kuma-mcp/README.md)
- [Ollama MCP →](./ollama-mcp/README.md)
- [Portainer MCP →](./portainer-mcp/README.md)

---

## License

MIT — use freely, modify and resell.

---

*Made with love by the AI-Engineering.at team.*
*[ai-engineering.at](https://ai-engineering.at) | Self-Hosted AI Infrastructure*

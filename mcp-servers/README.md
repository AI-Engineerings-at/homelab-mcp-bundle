# Homelab MCP Bundle

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![MCP Version](https://img.shields.io/badge/MCP-1.0+-blue.svg)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow.svg)](https://python.org)
[![Servers](https://img.shields.io/badge/MCP_Servers-8-purple.svg)](#the-bundle)
[![Tools](https://img.shields.io/badge/Total_Tools-51-orange.svg)](#the-bundle)

**Give your AI assistant full access to your self-hosted infrastructure.**

8 production-ready MCP servers for the homelab + DevOps stack most people actually run.
No cloud. No third-party data. Everything on your own hardware.

> Built by [AI-Engineering.at](https://ai-engineering.at) — Self-Hosted AI Infrastructure

---

## The Problem

Every MCP server is built for cloud services.

GitHub ✓ Notion ✓ Slack ✓ Linear ✓ Salesforce ✓

But what about people running their own stack?

| You're running... | Instead of... |
|-------------------|---------------|
| Mattermost | Slack |
| n8n | Zapier |
| Proxmox | AWS EC2 |
| Uptime Kuma | Datadog |
| Ollama | OpenAI |
| Grafana | Datadog |
| Portainer | ECS / Rancher |
| AdGuard Home | OpenDNS |

**This bundle covers all of them.**

---

## The Bundle

| Server | Tools | What it does |
|--------|-------|--------------|
| [mattermost-mcp](./mattermost-mcp/) | 7 | Read channels, post messages, search across your Mattermost workspace |
| [n8n-mcp](./n8n-mcp/) | 7 | Manage workflows, check executions, trigger webhooks in n8n |
| [proxmox-mcp](./proxmox-mcp/) | 8 | Monitor nodes, list VMs, start/stop virtual machines in Proxmox VE |
| [uptime-kuma-mcp](./uptime-kuma-mcp/) | 5 | Query service health, incidents and response times from Uptime Kuma |
| [ollama-mcp](./ollama-mcp/) | 4 | List models, generate text, chat and pull models from Ollama |
| [grafana-mcp](./grafana-mcp/) | 6 | Query dashboards, run PromQL and monitor alert rules in Grafana |
| [portainer-mcp](./portainer-mcp/) | 6 | Manage Docker Swarm — services, stacks, nodes, containers and logs |
| [adguard-mcp](./adguard-mcp/) | 8 | Manage DNS filtering, query logs and custom rules in AdGuard Home |

**51 tools across 8 servers. MIT licensed. Free forever.**

---

## What you can do with all 8

Once connected, conversations like these just work:

```
"Check if all services are UP. If Grafana is down, restart the VM on Proxmox."

"Post a summary of today's n8n workflow failures to the #ops channel in Mattermost."

"Show me all Uptime Kuma monitors that are currently down."

"Which Ollama models do I have? Run the infra-check prompt on llama3.1:8b."

"List all stopped VMs in Proxmox and tell me which critical monitors are down in Uptime Kuma."

"Get the last 100 log lines from the agents_service-monitor container."

"What are the top 10 blocked domains in AdGuard today?"

"Query Grafana: which nodes have memory usage above 80%? Show me the firing alerts."
```

No browser. No SSH. No clicking through dashboards.

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/AI-Engineerings-at/homelab-mcp-bundle
cd homelab-mcp-bundle/mcp-servers
```

### 2. Install

```bash
# Install all 8 servers
pip install -e mattermost-mcp/
pip install -e n8n-mcp/
pip install -e proxmox-mcp/
pip install -e uptime-kuma-mcp/
pip install -e ollama-mcp/
pip install -e grafana-mcp/
pip install -e portainer-mcp/
pip install -e adguard-mcp/
```

### 3. Configure — Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "mattermost": {
      "command": "python3",
      "args": ["-m", "mattermost_mcp.server"],
      "env": {
        "MM_BASE_URL": "https://your-mattermost.example.com",
        "MM_TOKEN":    "your_personal_access_token",
        "MM_TEAM_ID":  "your_team_id"
      }
    },
    "n8n": {
      "command": "python3",
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
      "args": ["-m", "ollama_mcp.server"],
      "env": {
        "OLLAMA_BASE_URL": "http://localhost:11434"
      }
    },
    "grafana": {
      "command": "python3",
      "args": ["-m", "grafana_mcp.server"],
      "env": {
        "GRAFANA_URL":      "http://YOUR_GRAFANA_IP:3000",
        "GRAFANA_USER":     "admin",
        "GRAFANA_PASSWORD": "your_password"
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
    },
    "adguard": {
      "command": "python3",
      "args": ["-m", "adguard_mcp.server"],
      "env": {
        "ADGUARD_URL":      "http://YOUR_ADGUARD_IP:3053",
        "ADGUARD_USER":     "admin",
        "ADGUARD_PASSWORD": "your_password"
      }
    }
  }
}
```

### 4. Configure — Claude Code CLI

```bash
claude mcp add proxmox proxmox-mcp \
  -e PVE_HOST=https://YOUR_PVE_IP:8006 \
  -e PVE_USER=root@pam \
  -e PVE_PASSWORD=your_password \
  -e PVE_VERIFY_SSL=false
```

Repeat for each server. See individual READMEs for full config options.

---

## vs. Alternatives

| Feature | This Bundle | cloud-tools-mcp | manual SSH |
|---------|------------|-----------------|------------|
| Proxmox support | ✅ | ❌ | partial |
| n8n support | ✅ | ❌ | ❌ |
| Mattermost support | ✅ | ❌ | ❌ |
| Uptime Kuma support | ✅ | ❌ | ❌ |
| Ollama support | ✅ | partial | ❌ |
| AdGuard Home support | ✅ | ❌ | ❌ |
| Portainer / Docker Swarm | ✅ | ❌ | partial |
| Grafana + PromQL | ✅ | ❌ | ❌ |
| Data stays on-prem | ✅ | ❌ | ✅ |
| GDPR friendly | ✅ | ❌ | ✅ |
| Works with Claude / Cursor / Windsurf | ✅ | varies | ❌ |
| MIT licensed | ✅ | varies | — |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  AI Assistant                            │
│          (Claude Desktop / Cursor / Windsurf)            │
└──────────────────────┬──────────────────────────────────┘
                       │  MCP (stdio / SSE)
        ┌──────────────┼──────────────────┐
        │              │                  │
   ┌────▼─────┐  ┌─────▼────┐  ┌────────▼──────┐
   │Proxmox   │  │   n8n    │  │  Mattermost   │
   │   MCP    │  │   MCP    │  │     MCP       │
   └────┬─────┘  └─────┬────┘  └────────┬──────┘
        │              │                │
   ┌────▼─────┐  ┌─────▼────┐  ┌────────▼──────┐
   │Proxmox VE│  │  n8n     │  │  Mattermost   │
   │  Cluster │  │ Instance │  │   Server      │
   └──────────┘  └──────────┘  └───────────────┘

        ... plus Uptime Kuma, Ollama, Grafana,
            Portainer and AdGuard Home.

        Everything runs on YOUR hardware.
        No data leaves your network.
```

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.11+ |
| Claude Desktop / Cursor / Windsurf | Latest |
| MCP SDK (`mcp`) | 1.0+ |

Each server has its own requirements — see individual READMEs.

---

## Server Details

| Server | README | Tools | Status |
|--------|--------|-------|--------|
| Mattermost MCP | [→ README](./mattermost-mcp/README.md) | 7 | Stable |
| n8n MCP | [→ README](./n8n-mcp/README.md) | 7 | Stable |
| Proxmox MCP | [→ README](./proxmox-mcp/README.md) | 8 | Stable |
| Uptime Kuma MCP | [→ README](./uptime-kuma-mcp/README.md) | 5 | Stable |
| Ollama MCP | [→ README](./ollama-mcp/README.md) | 4 | Stable |
| Grafana MCP | [→ README](./grafana-mcp/README.md) | 6 | Stable |
| Portainer MCP | [→ README](./portainer-mcp/README.md) | 6 | Stable |
| AdGuard MCP | [→ README](./adguard-mcp/README.md) | 8 | Stable |

---

## Tested On

- Proxmox VE 8.x (3-node cluster)
- Docker Swarm (3 managers, 1 worker)
- n8n 1.x
- Uptime Kuma 1.23+
- Ollama 0.3+
- Grafana 10.x
- Portainer CE 2.x
- AdGuard Home 0.107+

---

## Want More?

The free bundle gets you connected. For teams that want to go further:

**[AI-Engineering.at](https://ai-engineering.at)** — Premium guides, setup walkthroughs, and support for running AI assistants on self-hosted infrastructure.

- Complete Homelab AI Setup Guide (Proxmox + Docker Swarm + all 8 MCP servers)
- Config templates and tested configurations
- n8n workflow bundles for automated incident response

---

## FAQ

**Does this work with Claude Desktop on Windows / macOS / Linux?**
Yes. All servers run as Python processes over stdio. Works wherever Python 3.11+ and `pip` are available.

**Do I need to run all 8 servers?**
No. Each server is fully independent — install only what you need. Running just Proxmox + Uptime Kuma already gives you solid infrastructure visibility.

**Will this work with Cursor / Windsurf / other MCP clients?**
Yes. All servers use standard MCP stdio transport and are compatible with any client that supports the MCP 1.0 spec.

**Does my data leave my network?**
Never. All MCP servers run locally and talk directly to your self-hosted services over your LAN. No telemetry, no cloud relay.

**I get SSL errors connecting to Proxmox.**
Set `PVE_VERIFY_SSL=false` in the config. Self-signed certificates are common in homelab Proxmox setups and this disables the verification.

**The Uptime Kuma or Grafana server connects but returns no data.**
Check that the credentials have at least read access. Uptime Kuma requires the API key to be enabled under *Settings → API Keys*. Grafana requires a service account with the Viewer role.

**Can I add my own MCP server to the bundle?**
Yes — see the Contributing section below. Follow the structure of an existing server (e.g. `ollama-mcp/`) as a template.

**Portainer asks for an API token, not username/password. Where do I get it?**
In Portainer: *Account Settings → Access Tokens → Add access token*. Copy the generated token and use it as `PORTAINER_API_TOKEN`.

**How do I update to the latest version?**
```bash
git pull
pip install -e mcp-servers/mattermost-mcp/ -e mcp-servers/n8n-mcp/ # etc.
```
Then restart your MCP client (Claude Desktop / Cursor).

---

## Contributing

Issues, PRs and feature requests are welcome. This is a community project built for homelab users — contributions from real-world deployments are especially valuable.

### How to contribute

```bash
# 1. Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/homelab-mcp-bundle
cd homelab-mcp-bundle

# 2. Create a branch for your change
git checkout -b feat/your-feature-name

# 3. Make your changes and test locally
pip install -e mcp-servers/your-server/
python3 -m your_server.server  # confirm it starts without errors

# 4. Commit and push
git add .
git commit -m "feat(your-server): short description"
git push origin feat/your-feature-name

# 5. Open a Pull Request on GitHub
```

### What we're looking for

- **Bug reports** — include your OS, Python version, and the exact error message
- **New MCP servers** — good candidates: Home Assistant, Vaultwarden, Gitea, Jellyfin, Netdata
- **Tool improvements** — better descriptions, edge case handling, richer return data
- **Docs and examples** — real-world prompts and use cases from your homelab

### Adding a new MCP server

Use an existing server as a template (e.g. `ollama-mcp/` is the smallest and cleanest):

```
your-service-mcp/
├── your_service_mcp/
│   ├── __init__.py
│   └── server.py        # MCP tools defined here
├── .env.example         # Required env vars, no real values
├── pyproject.toml       # Package metadata
└── README.md            # Setup + tool list
```

Rules:
- All config via environment variables — no hardcoded defaults
- Each tool must have a clear `description` string (the AI reads this)
- Include a `.env.example` with every required variable documented
- Test against a real instance before submitting

---

## License

MIT — use freely, modify and redistribute, commercial use allowed.

---

*Made by the [AI-Engineering.at](https://ai-engineering.at) team.*
*Self-Hosted AI Infrastructure — no cloud required.*

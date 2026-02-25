# We Built 6 MCP Servers for Our Homelab in One Day — Open Source, Self-Hosted, GDPR-Ready

> **TL;DR**: We got tired of switching between Claude and our infrastructure dashboards. So we built 6 MCP servers that give Claude (and any AI assistant) direct access to our entire self-hosted stack. All open source. All running locally. No data leaves the house.

---

## The Problem

If you run a homelab, you know the drill.

Something breaks at midnight. You're checking Proxmox, switching to Portainer, tailing logs, checking Uptime Kuma, then copy-pasting error messages into Claude to ask "what is this?"

**Copy. Paste. Switch. Repeat.**

We had Claude Desktop open next to 6 different dashboards — and we were doing all the context-switching manually.

Then we discovered the **Model Context Protocol (MCP)** — and we stopped switching.

---

## What Is MCP?

[Model Context Protocol](https://modelcontextprotocol.io) is an open standard by Anthropic that lets AI assistants connect directly to external tools and data sources. Instead of the AI knowing only what you paste into the chat, it can *call tools directly* — read data, trigger actions, stream logs — all in context.

Think of it as a "plugin system for AI assistants" that works across Claude Desktop, Cursor, Windsurf, and more.

The ecosystem is growing fast. But when we looked at the available MCP servers, almost everything targets **cloud services**: GitHub, Notion, Slack, Google Drive.

**Nothing for self-hosters.**

So we built it ourselves.

---

## The Stack We Built For

Our homelab runs:

| Service | What it does |
|---------|--------------|
| **Proxmox VE** | 3-node cluster, hosts all VMs |
| **Docker Swarm** | Container orchestration (3 managers + 1 worker) |
| **Portainer CE** | Docker Swarm UI + API |
| **Mattermost** | Self-hosted team chat |
| **n8n** | Workflow automation |
| **Uptime Kuma** | Service monitoring (28 monitors) |
| **Ollama** | Local LLM inference (llama3.1:8b on RTX 3090) |

All self-hosted. All on-premise. All GDPR-compliant by default.

---

## The 6 MCP Servers We Built

### 1. Proxmox MCP — 8 Tools

Talk to your Proxmox cluster in plain language.

```
"Which VMs are running on pve3 right now?"
"How much memory is pve1 using?"
"Start VM 104 on node pve"
"Is the cluster quorate? Any nodes offline?"
```

**Tools**: `get_cluster_status`, `list_nodes`, `get_node_status`, `list_vms`, `list_lxc`, `get_vm_status`, `start_vm`, `stop_vm`

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "proxmox": {
      "command": "proxmox-mcp",
      "env": {
        "PVE_HOST": "https://10.0.0.1:8006",
        "PVE_USER": "root@pam",
        "PVE_PASSWORD": "your_password",
        "PVE_VERIFY_SSL": "false"
      }
    }
  }
}
```

For read-only access, create a dedicated API user:
```bash
pveum user add mcp-reader@pam
pveum acl modify / -user mcp-reader@pam -role PVEAuditor
```

---

### 2. Portainer MCP — 6 Tools

Docker Swarm management via natural language. No more clicking through the Portainer UI.

```
"Show me all running Swarm services and their replica counts"
"Get the last 200 log lines from agents_service-monitor"
"Which Swarm nodes are currently healthy?"
"List all stacks — which ones are inactive?"
```

**Tools**: `services_list`, `service_logs`, `stacks_list`, `stack_deploy`, `node_status`, `containers_list`

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "portainer": {
      "command": "python3",
      "args": ["-m", "portainer_mcp.server"],
      "env": {
        "PORTAINER_URL": "http://10.0.0.80:9000",
        "PORTAINER_API_TOKEN": "ptr_your_token_here",
        "PORTAINER_ENDPOINT_ID": "1"
      }
    }
  }
}
```

Get an API token in Portainer → your username → My Account → Access Tokens.

---

### 3. Mattermost MCP — 7 Tools

Your AI assistant reads your team channels, posts answers, and searches across your workspace.

```
"Read the last 20 messages in #ops"
"Post a Grafana alert summary to #monitoring"
"Search all posts mentioning 'disk full' from last week"
"Who mentioned @admin today?"
```

**Tools**: `list_channels`, `get_channel_info`, `read_channel`, `post_message`, `list_users`, `get_mentions`, `search_posts`

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "mattermost": {
      "command": "python3",
      "args": ["/path/to/mattermost-mcp/src/mattermost_mcp/server.py"],
      "env": {
        "MM_BASE_URL": "http://your-mattermost:8065",
        "MM_TOKEN": "your_personal_access_token",
        "MM_TEAM_ID": "your_team_id"
      }
    }
  }
}
```

Works with HTTP (self-signed certs fine). Get your team ID:
```bash
curl -H "Authorization: Bearer TOKEN" \
  http://your-mattermost:8065/api/v4/teams | python3 -m json.tool
```

---

### 4. n8n MCP — 7 Tools

Manage your automation workflows without leaving the AI chat.

```
"List all active workflows"
"What failed in the last 10 executions of 'Daily Report'?"
"Trigger the 'Backup Sync' webhook"
"Deactivate the broken workflow"
```

**Tools**: `list_workflows`, `get_workflow`, `activate_workflow`, `deactivate_workflow`, `list_executions`, `get_execution`, `trigger_webhook`

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "n8n": {
      "command": "python",
      "args": ["-m", "n8n_mcp.server"],
      "env": {
        "N8N_BASE_URL": "http://your-n8n:5678",
        "N8N_API_KEY": "your_api_key"
      }
    }
  }
}
```

---

### 5. Uptime Kuma MCP — 5 Tools

Query your monitoring data from AI context. No more opening the dashboard just to check if something is down.

```
"Are all services up?"
"Which monitors had incidents in the last 24 hours?"
"What's the average response time for the Grafana monitor?"
"Show me all monitors in the 'Critical Services' group"
```

**Tools**: `list_monitors`, `get_monitor`, `get_monitor_beats`, `get_status_page`, `get_incidents`

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "uptime-kuma": {
      "command": "uptime-kuma-mcp",
      "env": {
        "KUMA_BASE_URL": "http://your-kuma:3001",
        "KUMA_USERNAME": "joe",
        "KUMA_PASSWORD": "your_password"
      }
    }
  }
}
```

---

### 6. Ollama MCP — 4 Tools

Use your local LLMs from within AI conversations. Inception-level stuff: Claude calling your local llama3.

```
"What models do I have installed on the GPU server?"
"Pull llama3.2:3b if it's not there yet"
"Run this prompt through llama3.1:8b: [...]"
"How much VRAM is the 8B model using?"
```

**Tools**: `list_models`, `generate`, `chat`, `pull_model`

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "ollama": {
      "command": "python3",
      "args": ["/path/to/ollama-mcp/src/ollama_mcp/server.py"],
      "env": {
        "OLLAMA_BASE_URL": "http://10.0.0.90:11434"
      }
    }
  }
}
```

---

## All 6 Together — The Full Config

```json
{
  "mcpServers": {
    "mattermost": {
      "command": "python3",
      "args": ["/path/to/mattermost-mcp/src/mattermost_mcp/server.py"],
      "env": {
        "MM_BASE_URL": "http://your-mattermost:8065",
        "MM_TOKEN": "your_token",
        "MM_TEAM_ID": "your_team_id"
      }
    },
    "n8n": {
      "command": "python",
      "args": ["-m", "n8n_mcp.server"],
      "env": {
        "N8N_BASE_URL": "http://your-n8n:5678",
        "N8N_API_KEY": "your_api_key"
      }
    },
    "proxmox": {
      "command": "proxmox-mcp",
      "env": {
        "PVE_HOST": "https://your-pve:8006",
        "PVE_USER": "root@pam",
        "PVE_PASSWORD": "your_password",
        "PVE_VERIFY_SSL": "false"
      }
    },
    "uptime-kuma": {
      "command": "uptime-kuma-mcp",
      "env": {
        "KUMA_BASE_URL": "http://your-kuma:3001",
        "KUMA_USERNAME": "joe",
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
        "PORTAINER_URL": "http://your-portainer:9000",
        "PORTAINER_API_TOKEN": "ptr_your_token",
        "PORTAINER_ENDPOINT_ID": "1"
      }
    }
  }
}
```

With all 6 connected, you can do things like:

> *"Check if all services are UP in Uptime Kuma. If Grafana is down, find the container in Portainer and show me the last 50 log lines."*

> *"Post a summary of today's n8n workflow failures to the #ops channel in Mattermost."*

> *"List all stopped VMs in Proxmox. Are any of them running critical services according to Uptime Kuma?"*

---

## Why Self-Hosted Matters Here

Every MCP server in this bundle talks **only to your local network**.

- No data goes to third-party APIs
- No telemetry, no cloud logging
- Works fully offline (airgapped labs included)
- GDPR compliant by architecture — the data never leaves your premises

Most commercial MCP servers route your infra data through their cloud. We deliberately don't. The credentials stay in your `claude_desktop_config.json`, on your machine, talking to your local services.

---

## Installation

```bash
# Clone the repo
git clone https://github.com/AI-Engineerings-at/Playbook01
cd Playbook01/mcp-servers

# Install all 6 servers
pip install -e mattermost-mcp/
pip install -e n8n-mcp/
pip install -e proxmox-mcp/
pip install -e uptime-kuma-mcp/
pip install -e ollama-mcp/
pip install -e portainer-mcp/
```

Each server is a standalone Python package. Install only what you need.

**Requirements**: Python 3.11+, Claude Desktop / Cursor / Windsurf (anything with MCP support)

---

## What's Next (v2)

We're already working on the next round:

- **AdGuard Home MCP** — manage DNS blocklists and query logs from AI
- **Grafana MCP** — query dashboards, create annotations, read alert states
- **Neo4j MCP** — query your knowledge graph in natural language

If you're running other self-hosted tools and want an MCP server for them — open an issue or PR. We built this in one day, and every server followed the same pattern. New servers are straightforward to add.

---

## The Ecosystem Gap

The MCP ecosystem needs more self-hosted coverage.

Right now it's dominated by SaaS: GitHub, Notion, Linear, Salesforce. That's great for those users. But there's an entire world of self-hosters — people running Proxmox, TrueNAS, Jellyfin, Home Assistant, Gitea, Forgejo, Nextcloud — who get nothing.

We're trying to change that, one server at a time.

---

## Links

- **GitHub**: [github.com/AI-Engineerings-at/Playbook01](https://github.com/AI-Engineerings-at/Playbook01) — ⭐ Stars help us know people care
- **Website**: [ai-engineering.at](https://ai-engineering.at) — Newsletter for updates (new servers, tutorials, homelab AI patterns)
- **License**: MIT — use freely, modify, even sell

---

*If this is useful to you, star the repo. It genuinely helps us prioritize what to build next.*

*Questions? Drop them in the comments — we read everything.*

---

**Tags**: `#homelab` `#selfhosted` `#mcp` `#claude` `#proxmox` `#docker` `#n8n` `#opensource` `#gdpr` `#devops`

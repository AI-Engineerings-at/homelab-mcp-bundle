# The Homelab MCP Quickstart Guide
## Connect Claude to Your Self-Hosted Infrastructure in 15 Minutes

> **Free Download** · AI-Engineering.at · 2026
> 8 MCP servers · 51 tools · MIT licensed · Works with Claude Desktop & Claude Code

---

## What You're Getting

This guide shows you how to connect Claude to the tools you already run at home — Proxmox, Docker, Grafana, n8n, Uptime Kuma, and more.

After following this guide, you'll be able to ask Claude things like:

- *"Are all my services online right now?"*
- *"Which VMs are running on pve3 and how much RAM are they using?"*
- *"Trigger the n8n backup workflow and send me a summary in Mattermost."*
- *"Show me the current Grafana alerts and explain what's wrong."*

No more clicking through UIs. No copy-pasting logs. Just ask.

---

## What is MCP (and why should you care)?

**Model Context Protocol** (MCP) is Anthropic's open standard for connecting AI models to external tools and data sources in real time.

Without MCP, Claude knows a lot — but it's isolated. It can't see your current CPU usage. It can't check if your Uptime Kuma monitors are green. It can't restart a Docker service.

With MCP, Claude becomes a live ops interface for your homelab:

```
You → Claude Desktop → MCP Server → Your Infrastructure
                                        ↓
                               Proxmox / Docker / Grafana / n8n / ...
```

The key: **everything stays on your network.** No data goes to the cloud except the natural language query itself.

---

## The 8 MCP Servers in This Bundle

| Server | Tools | What it controls |
|--------|-------|-----------------|
| **Proxmox MCP** | 8 | VMs, nodes, cluster status, snapshots |
| **Portainer MCP** | 6 | Docker Swarm services, stacks, containers |
| **Grafana MCP** | 6 | Dashboards, PromQL queries, alert rules |
| **n8n MCP** | 7 | Workflows, executions, webhook triggers |
| **Uptime Kuma MCP** | 5 | Monitor status, incidents, response times |
| **Ollama MCP** | 4 | Local LLM models, text generation, model management |
| **Mattermost MCP** | 7 | Channels, messages, search, notifications |
| **AdGuard MCP** | 8 | DNS filtering, blocklists, query log |
| **Total** | **51** | |

All servers are MIT licensed and available at:
**[github.com/AI-Engineerings-at/homelab-mcp-bundle](https://github.com/AI-Engineerings-at/homelab-mcp-bundle)**

---

## Requirements

Before you start, you need:

- **Claude Desktop** (free) or **Claude Code** (Pro plan)
- **Python 3.11+** on the machine running the MCP servers
- At least one of the supported services running in your homelab
- Basic familiarity with JSON config files

That's it. No cloud accounts. No API keys to external services.

---

## 15-Minute Setup: Step by Step

### Step 1 — Clone the Bundle

```bash
git clone https://github.com/AI-Engineerings-at/homelab-mcp-bundle.git
cd homelab-mcp-bundle
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

Or per server if you only want specific ones:

```bash
cd proxmox-mcp && pip install -r requirements.txt
```

### Step 3 — Configure Your Servers

Each MCP server has a `.env.example` file. Copy and fill in your values:

```bash
cp proxmox-mcp/.env.example proxmox-mcp/.env
```

**Example — Proxmox MCP** (`.env`):
```ini
PROXMOX_HOST=10.40.10.14
PROXMOX_USER=root@pam
PROXMOX_PASSWORD=your_password_here
PROXMOX_VERIFY_SSL=false
```

**Example — Grafana MCP** (`.env`):
```ini
GRAFANA_URL=http://10.40.10.80:3000
GRAFANA_TOKEN=your_api_token
```

### Step 4 — Add to Claude Desktop Config

Open your Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Add your MCP servers:

```json
{
  "mcpServers": {
    "proxmox": {
      "command": "python3",
      "args": ["/path/to/homelab-mcp-bundle/proxmox-mcp/server.py"]
    },
    "grafana": {
      "command": "python3",
      "args": ["/path/to/homelab-mcp-bundle/grafana-mcp/server.py"]
    },
    "portainer": {
      "command": "python3",
      "args": ["/path/to/homelab-mcp-bundle/portainer-mcp/server.py"]
    }
  }
}
```

Add only the servers you need. You don't have to run all 8.

### Step 5 — Restart Claude Desktop

Quit and reopen Claude Desktop. You should see the MCP tools appear in the toolbar (hammer icon).

**Test it:**
> "Use the Proxmox MCP to show me the status of all nodes in my cluster."

---

## Real-World Use Cases

### Infrastructure Health Check (30 seconds)

> "Check all my services: query Uptime Kuma for any down monitors, then check Grafana for active alerts, then check if all Docker Swarm services are running. Give me a summary."

Claude will run all three queries in parallel and give you a consolidated status report.

### Incident Response

> "Uptime Kuma says Grafana is down. Check the Portainer MCP to see if the Grafana container is running. If it's stopped, tell me the last 20 log lines."

No SSH needed. No terminal. Just ask.

### Automation Ops

> "Show me all active n8n workflows. Which ones had failed executions in the last 24 hours? Give me the error messages."

### Local AI Benchmarking

> "Use Ollama MCP to list all models I have installed. Run the prompt 'Explain what MCP is in 2 sentences' against each one and compare the responses."

---

## Frequently Asked Questions

**Q: Does this work with Claude Code (not just Claude Desktop)?**

Yes. Claude Code supports MCP natively. Add the servers to your project's `.mcp.json` or use `claude mcp add` from the CLI.

**Q: Is this GDPR-compliant?**

Your infrastructure data (IPs, VM names, service status) stays on your network and never leaves it. Only the natural language query goes to Anthropic's API. For EU users running self-hosted infrastructure: this is as GDPR-friendly as MCP gets.

**Q: What if a service isn't in the bundle?**

The bundle covers the most common self-hosted stack. If you're running something else (Home Assistant, Vaultwarden, Nextcloud), the MCP SDK makes it straightforward to write additional servers. The bundle code is well-documented and serves as a reference.

**Q: Do I need to run the MCP servers 24/7?**

The MCP servers only run when Claude Desktop is active. They're lightweight Python processes that start when you open Claude and stop when you close it.

---

## What's Next

You've got Claude talking to your infrastructure. Here's what to explore next:

### Go deeper with the free bundle
→ **[github.com/AI-Engineerings-at/homelab-mcp-bundle](https://github.com/AI-Engineerings-at/homelab-mcp-bundle)**
Full docs, all 8 servers, examples for every tool.

### Automate with n8n
If you want Claude to trigger automated workflows (not just read data), the **n8n Starter Bundle** gives you 3 production-ready workflow templates:
- Stripe → automated download delivery
- Local AI pipeline with Ollama (no OpenAI, GDPR-safe)
- GDPR Art. 30 register automation

→ **[ai-engineering.at/products/n8n-starter-bundle](https://ai-engineering.at)** · EUR 29

### Build a full AI agent team
Want multiple Claude agents working in parallel — one for DevOps, one for code, one for QA — all communicating through Mattermost? The **AI Agent Team Blueprint** shows the exact architecture we run in production.

→ **[ai-engineering.at/products/ai-agent-team-blueprint](https://ai-engineering.at)** · EUR 19

### Monitor everything with Grafana
Five production-ready Grafana dashboards for Docker Swarm, Node Exporter, infrastructure overview, network traffic, and alerts. Works with the Grafana MCP server out of the box.

→ **[ai-engineering.at/products/grafana-dashboard-pack](https://ai-engineering.at)** · EUR 39

---

## About AI-Engineering.at

We build open-source tools for homelab operators and DevOps engineers who want to use AI locally — without cloud dependencies, without vendor lock-in, and with full data control.

Everything we publish comes from our own production setup: a 3-node Proxmox cluster, Docker Swarm, Grafana, n8n, and a team of Claude Code agents running 24/7.

**Website**: [ai-engineering.at](https://ai-engineering.at)
**GitHub**: [github.com/AI-Engineerings-at](https://github.com/AI-Engineerings-at)

---

*MIT Licensed · Free to use, share, and modify*
*Questions? hello@ai-engineering.at*

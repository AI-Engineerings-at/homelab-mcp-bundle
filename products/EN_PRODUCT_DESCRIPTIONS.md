# EN Product Descriptions — AI-Engineering.at
> Ready for: Landing Page · Gumroad · Stripe
> Erstellt von @lisa01 | 2026-02-25

---

## Product 1 — AI Agent Team Blueprint
**Price: EUR 19** | `gumroad.com/l/ai-agent-team-blueprint`

### Title
Build a fully automated AI agent team — that actually works

### Subtitle
Real architecture from a production system. 4 Claude agents, Mattermost as hub, n8n for automation.

### Short Description (150 chars max)
```
Complete blueprint: 4 Claude agents + Mattermost hub. Templates, code, security rules from a production system. Ready to use.
```

### Full Description
What if your AI team worked 24/7 for you — without you supervising every step?

This blueprint shows you how to build a multi-agent system that truly works. Not theory. Not "could work in theory." Real architecture we've been running in production for months.

**Our setup:**
- 4 specialized Claude Code agents (Manager, Frontend, Backend, QA)
- Mattermost as the communication hub (self-hosted, free)
- n8n for workflow automation
- Shared MEMORY.md system for agent knowledge

**What you get:**

✓ **Complete architecture** — Diagrams, infrastructure, deployment
✓ **CLAUDE.md templates** — Ready to use for manager & specialist agents
✓ **mm_wait.py pattern** — The polling mechanism that holds everything together
✓ **Communication protocol** — How agents hand off tasks without chaos
✓ **5 security rules** — Learned from real incidents (rm -rf, wrong identity, etc.)
✓ **Docker Compose** — Self-host Mattermost in 5 minutes
✓ **Step-by-step plan** — From zero to a running team in 2 weeks
✓ **Failure log** — The most common mistakes and how to avoid them
✓ **Readiness checklist** — Is your team actually ready?

**Who is this for?**
- Developers already using Claude Code who want to get more out of it
- Teams looking to automate repetitive tasks
- Homelab operators with their own infrastructure
- AI enthusiasts who want to build multi-agent systems hands-on

**Requirements:**
- Claude Code (Pro, ~$20/month)
- A server/VPS (from €5/month) or homelab
- Basic Linux/Docker knowledge

### Tags
```
claude, claude-code, ai-agents, mattermost, n8n, automation, multi-agent, homelab, blueprint, template
```

---

## Product 2 — n8n Starter Bundle
**Price: EUR 29** | `gumroad.com/l/n8n-starter-bundle`

### Title
3 production-ready n8n workflows — plug & play, GDPR-compliant

### Subtitle
AI automation for European businesses — no OpenAI dependency, fully self-hosted.

### Short Description (150 chars max)
```
3 battle-tested n8n workflows: Stripe delivery, local AI (Ollama), GDPR Art.30 register. GDPR-safe, self-hosted, ready to import.
```

### Full Description
Stop building automation from scratch. Get 3 battle-tested n8n workflows for European businesses and homelab operators:

**Workflow 1: Stripe → Automated Download Delivery**
Auto-send download links after purchase — no manual steps.
- Stripe webhook verification included
- Automatic email delivery of download links
- Perfect for: eBooks, templates, software licenses

**Workflow 2: Local AI Analysis with Ollama**
Run AI analysis locally with llama3.1/3.2 — no OpenAI, no data leaks, GDPR-safe.
- Webhook-triggered analysis pipeline
- Results sent via Mattermost or Slack
- 100% data stays on your server

**Workflow 3: GDPR Art.30 Processing Register**
REST API to track and document data processing activities as required by GDPR Art.30.
- All mandatory fields with validation
- Structured JSON export for audits

**What's included:**
- ✅ 3 ready-to-import JSON files
- ✅ English README with setup guide
- ✅ Tested on n8n 1.x (Self-Hosted & Cloud)

**Requirements:**
- n8n >= 1.0
- Workflow 1: Stripe account
- Workflow 2: Ollama running locally or remotely
- Workflow 3: No external dependencies

### Tags
```
n8n, automation, gdpr, ai, ollama, stripe, self-hosted, workflow, template
```

---

## Product 3 — Grafana Dashboard Pack
**Price: EUR 39** | `gumroad.com/l/grafana-dashboard-pack`

### Title
6 Production-Ready Grafana Dashboards — Import & Monitor in Minutes

### Subtitle
Battle-tested monitoring dashboards for homelab & DevOps — Docker Swarm, Prometheus, Node Exporter.

### Short Description (150 chars max)
```
6 Grafana dashboards: Infrastructure, Docker Swarm, Node Exporter, Network, Services, Alerts. Import & done. Prometheus-ready.
```

### Full Description
Stop spending hours configuring Grafana dashboards from scratch.

This pack includes **6 battle-tested JSON dashboards** — running in production on a real Docker Swarm cluster with Prometheus, Node Exporter, and cAdvisor.

**Dashboard 1: Infrastructure Overview**
CPU, RAM, Disk for all nodes at a glance — uptime indicators, critical thresholds pre-configured.

**Dashboard 2: Docker Swarm Cluster**
Services, Tasks, Replicas in real time — stack overviews, container status.

**Dashboard 3: Node Exporter Full**
Deep-dive system metrics — CPU per core, memory breakdown, disk I/O, network throughput.

**Dashboard 4: Network Overview**
Bandwidth per interface, packets/sec, error rates — for routers, firewalls, switches.

**Dashboard 5: Services Status**
All HTTP endpoints at a glance — uptime overview, response time trends.

**Dashboard 6: Alerts Overview**
Active Prometheus alerts collected — alert history and frequency for on-call teams.

**You get:**
- ✅ 6 JSON files — import directly into Grafana
- ✅ Bash import script (all 6 via API in one command)
- ✅ Install guide with step-by-step instructions
- ✅ Requirements: Grafana >= 9.0, Prometheus + Node Exporter

**Who this is for:**
- Homelab operators (Proxmox, Docker, Synology, Pi)
- SME IT admins: enterprise monitoring without enterprise costs
- DevOps engineers: fast start, then customize
- GDPR-conscious teams: 100% local, no cloud dependency

### Tags
```
grafana, prometheus, homelab, devops, monitoring, docker, node-exporter, dashboard, json
```

---

## Product 4 — GDPR Art.30 Processing Register Template
**Price: EUR 79** | `gumroad.com/l/gdpr-art30-template`

### Title
GDPR Art.30 Processing Register — production-ready template, legally compliant

### Subtitle
n8n workflow with REST API — set up once, document your data processing activities properly.

### Short Description (150 chars max)
```
GDPR Art.30 compliant processing register as n8n workflow. Validates all mandatory fields. Self-hosted, no cloud dependency.
```

### Full Description
Every business needs it — few get it right.

Article 30 of the GDPR requires companies to maintain a record of processing activities. This template makes it easy: set it up once, then fill it in with a structured process.

**What you get:**

✓ **n8n workflow (JSON)** — REST API for recording processing activities
✓ **All mandatory Art.30 fields** — Validation built directly into the workflow
✓ **Structured JSON output** — Export for authorities, audits, internal systems
✓ **No cloud dependency** — 100% local, GDPR-compliant by design
✓ **Commented code** — Adaptable to your company structure

**Who this is for:**
- SMEs without a dedicated data protection department
- Data protection officers who want to digitize their processes
- IT admins looking to automate compliance workflows
- Tax advisors and law firms managing multiple clients

**Requirements:**
- n8n >= 1.0 (Self-Hosted or Cloud)
- No external APIs required

### Tags
```
gdpr, dsgvo, art30, compliance, data-protection, n8n, template, self-hosted, eu, europe, privacy
```

---

## Product 5 — Playbook01: The Local AI Stack
**Price: EUR 49** | `gumroad.com/l/playbook01`

### Title
Playbook01: The Local AI Stack — Complete Setup Guide

### Subtitle
Build a production-ready, fully self-hosted AI infrastructure — Proxmox, Docker Swarm, n8n, Ollama, Mattermost, and more.

### Short Description (150 chars max)
```
Complete guide to building your own local AI stack. Proxmox + Docker Swarm + n8n + Ollama. No cloud needed.
```

### Full Description
Everything you need to set up a production-grade, self-hosted AI infrastructure from scratch.

This guide walks you through the exact setup used in production — a 3-node Proxmox cluster, Docker Swarm overlay, n8n automation, Ollama local LLMs, and Mattermost for team communication.

**What's included:**
- Step-by-step Proxmox cluster setup (3 nodes, HA-ready)
- Docker Swarm overlay with 9 stacks, 22 services
- n8n workflow automation (5 production workflows)
- Ollama local LLM setup (RTX GPU + fallback)
- Mattermost self-hosted communication hub
- Monitoring stack: Prometheus + Grafana + Uptime Kuma
- AIOps agent with bidirectional Mattermost integration
- All configs, scripts, and troubleshooting guides included

**For:** Homelab operators, DevOps engineers, privacy-conscious teams, EU businesses (GDPR-compliant by design)

**Requirements:** 3+ servers or VMs, Proxmox VE, basic Linux knowledge

### Tags
```
homelab, self-hosted, proxmox, docker, swarm, n8n, ollama, mattermost, grafana, ai, local, gdpr, devops
```

---

## Product 6 — Homelab MCP Bundle
**Price: FREE** | `github.com/AI-Engineerings-at/homelab-mcp-bundle`

### Title
Homelab MCP Bundle — 8 MCP Servers for Self-Hosted Infrastructure

### Subtitle
Give Claude (or any AI) full access to your homelab — Proxmox, n8n, Mattermost, Uptime Kuma, Ollama, Grafana, Portainer, AdGuard.

### Short Description (150 chars max)
```
8 open-source MCP servers, 51 tools. Connect Claude to your entire homelab stack. MIT licensed.
```

### Full Description
Give your AI assistant (Claude, Cursor, Windsurf) full access to your self-hosted infrastructure — without sending data to the cloud.

**8 open-source MCP servers. 51 tools. MIT licensed.**

| MCP Server | Tools | What it does |
|------------|-------|-------------|
| 🗨️ **Mattermost MCP** | 7 | Read channels, post messages, search, manage users |
| ⚙️ **n8n MCP** | 7 | List/trigger workflows, check executions, manage webhooks |
| 🖥️ **Proxmox MCP** | 8 | Monitor nodes, list/start/stop VMs, cluster status |
| 📡 **Uptime Kuma MCP** | 5 | Query monitor health, incidents, response times |
| 🤖 **Ollama MCP** | 4 | List local models, generate text, pull new models |
| 📊 **Grafana MCP** | 5 | Query dashboards, PromQL, manage alerts |
| 🐳 **Portainer MCP** | 5 | Docker Swarm services, stacks, container logs |
| 🛡️ **AdGuard MCP** | ? | DNS filtering, blocklists, query logs |

**Real-world examples — ask your AI:**

> *"Check Uptime Kuma. If anything is down, find the VM on Proxmox and restart it. Then post a summary to #ops in Mattermost."*

> *"Which n8n workflows failed in the last 24 hours? Summarize the errors."*

**Why self-hosted MCP?**

Every existing MCP server is built for cloud services — GitHub, Notion, Slack, Linear. This bundle covers the self-hosted equivalents used by homelab operators and privacy-conscious teams.

- No data leaves your network
- GDPR-friendly by design — ideal for EU teams
- Works fully air-gapped (except Ollama model pulls)

**Requirements:**
- Python 3.11+
- Claude Desktop / Cursor / Windsurf (any MCP-compatible client)
- Self-hosted instances of the tools you want to connect

**Quick install:**
```bash
git clone https://github.com/AI-Engineerings-at/homelab-mcp-bundle
cd homelab-mcp-bundle
pip install -e mattermost-mcp/ n8n-mcp/ proxmox-mcp/ uptime-kuma-mcp/ ollama-mcp/ grafana-mcp/ portainer-mcp/ adguard-mcp/
```

### Tags
```
mcp, model context protocol, homelab, self-hosted, proxmox, n8n, mattermost, uptime-kuma, ollama, claude, free, open-source, gdpr
```

---

## Landing Page Card Format (for all 6 products)

Quick copy-paste for `/en` Landing Page product section:

```
Product Cards (EN):

1. AI Agent Team Blueprint — EUR 19
   "Build a fully automated AI agent team that actually works.
   4 Claude agents + Mattermost hub. Production-proven architecture."

2. n8n Starter Bundle — EUR 29
   "3 plug-and-play automation workflows: Stripe delivery,
   local AI analysis, GDPR Art.30 register."

3. Grafana Dashboard Pack — EUR 39
   "6 production-ready monitoring dashboards for homelab & DevOps.
   Import & monitor in minutes."

4. GDPR Compliance Bundle — EUR 79
   "Legally compliant processing register as n8n workflow.
   Self-hosted, no cloud dependency."

5. Playbook01: The Local AI Stack — EUR 49
   "Complete guide to building your self-hosted AI infrastructure.
   Proxmox + Docker Swarm + n8n + Ollama. Production-proven."

6. Homelab MCP Bundle — FREE (Open Source)
   "8 MCP servers, 51 tools. Give Claude full access
   to your entire homelab stack. GitHub: homelab-mcp-bundle"
```

---

*@lisa01 | AI-Engineering.at | 2026-02-25*

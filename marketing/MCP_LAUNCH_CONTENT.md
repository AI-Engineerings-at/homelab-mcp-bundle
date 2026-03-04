# MCP Bundle — Launch Announcement Content

> **Stand**: 2026-02-25 | Erstellt von @lisa01
> **Für**: Show HN, Reddit, LinkedIn, Twitter/X, Dev.to
> **GitHub**: https://github.com/AI-Engineerings-at/homelab-mcp-bundle
> **Website**: https://ai-engineering.at

---

## Facts (immer stimmen lassen)

- **8 MCP Server**: Mattermost, n8n, Proxmox, Uptime Kuma, Ollama, Grafana, Portainer, AdGuard
- **51 Tools total**: 7 + 7 + 8 + 5 + 4 + 6 + 6 + 8 = 51
- **Lizenz**: MIT (gratis, auch für kommerzielle Nutzung)
- **Sprache**: Python 3.11+
- **Zielgruppe**: Homelab, Self-Hosted, DevOps, Sysadmins
- **First Mover**: Einzige MCP Server für diese spezifischen Tools

---

## 1. Show HN Post (Hacker News)

**Titel:**
```
Show HN: Homelab MCP Bundle – 8 Open-Source MCP Servers for Self-Hosted Infrastructure
```

**Body:**
```
Hey HN,

I built 8 MCP servers for the self-hosted infrastructure stack I run at home.
Most existing MCP servers target cloud services (GitHub, Notion, Slack, Linear).
This bundle covers the self-hosted equivalents:

- Mattermost MCP (7 tools) — read channels, post messages, search
- n8n MCP (7 tools) — manage workflows, check executions, trigger webhooks
- Proxmox MCP (8 tools) — monitor nodes, list/start/stop VMs
- Uptime Kuma MCP (5 tools) — query service health, incidents, response times
- Ollama MCP (4 tools) — list models, generate text, pull new models
- Grafana MCP (6 tools) — dashboards, PromQL queries, alerts
- Portainer MCP (6 tools) — Docker Swarm services, stacks, containers
- AdGuard MCP (8 tools) — DNS filtering, blocklists, query log

51 tools total. MIT licensed. Python 3.11+.

Works with Claude Desktop, Cursor, Windsurf — anything that speaks MCP.

Once connected you can do things like:

"Check if all services are UP, and if Grafana is down, restart the VM on Proxmox."
"Post a summary of today's n8n workflow failures to the #ops channel in Mattermost."
"Which Ollama models do I have? Run a prompt against llama3.1:8b."

I'm running this in production on a 3-node Proxmox cluster with a Docker Swarm overlay.
Everything stays on-prem — no data leaves your network (GDPR-friendly for EU folks).

GitHub: https://github.com/AI-Engineerings-at/homelab-mcp-bundle

Happy to answer questions. Feedback welcome — especially on the Proxmox and n8n servers.
```

---

## 2. Reddit Posts

### r/selfhosted

**Titel:**
```
I built MCP servers for Mattermost, n8n, Proxmox, Uptime Kuma and Ollama — give your AI assistant full access to your self-hosted stack
```

**Body:**
```
Hey r/selfhosted,

I got tired of every MCP server being for cloud services, so I built the self-hosted equivalents.

**What is MCP?**
Model Context Protocol — lets AI assistants (Claude, Cursor, etc.) call tools and APIs directly.
Think of it as function calling that works across different AI clients.

**The Bundle (MIT, free, open-source):**

| Server | Tools | What it does |
|--------|-------|-------------|
| Mattermost MCP | 7 | Read channels, post messages, search |
| n8n MCP | 7 | Manage workflows, check executions, trigger webhooks |
| Proxmox MCP | 8 | Monitor nodes, list/start/stop VMs |
| Uptime Kuma MCP | 5 | Query service health, incidents, response times |
| Ollama MCP | 4 | List models, generate text, pull models |
| Grafana MCP | 6 | Dashboards, PromQL queries, alerts |
| Portainer MCP | 6 | Docker Swarm services, stacks, containers |
| AdGuard MCP | 8 | DNS filtering, blocklists, query log |

**51 tools total.** Everything stays on your hardware.

**Real use cases I'm using this for:**
- Ask Claude to check Uptime Kuma and if something's down, restart it on Proxmox
- Post n8n execution summaries automatically to Mattermost
- Query my local Ollama instead of sending data to OpenAI

**Install:**
```bash
git clone https://github.com/AI-Engineerings-at/homelab-mcp-bundle
cd homelab-mcp-bundle
pip install -e mattermost-mcp/ n8n-mcp/ proxmox-mcp/ uptime-kuma-mcp/ ollama-mcp/ grafana-mcp/ portainer-mcp/ adguard-mcp/
```

Then add to your `claude_desktop_config.json` — full config in the README.

Running this on a 3-node Proxmox cluster + Docker Swarm in production.
GDPR-friendly — nothing leaves your network.

GitHub: https://github.com/AI-Engineerings-at/homelab-mcp-bundle

Would love feedback from anyone running similar stacks!
```

---

### r/homelab

**Titel:**
```
Give Claude / Cursor full access to your homelab — 8 open-source MCP servers for Proxmox, n8n, Mattermost, Uptime Kuma, Ollama, Grafana, Portainer, AdGuard
```

**Body:**
```
Long-time lurker, first-time poster with something actually useful (hopefully).

I run a homelab with:
- 3-node Proxmox cluster
- Docker Swarm overlay (4 nodes)
- n8n for automation
- Mattermost for team comms
- Uptime Kuma for monitoring
- Ollama for local LLMs (RTX 3090)

I got frustrated that every AI tool integration requires cloud services.
So I built MCP servers for the self-hosted stack.

**MCP = Model Context Protocol** — lets Claude Desktop, Cursor, Windsurf etc. call your APIs directly.

**What I built (all MIT licensed):**
- **Proxmox MCP** — 8 tools: list nodes/VMs, get status, start/stop VMs
- **n8n MCP** — 7 tools: list/trigger/monitor workflows
- **Mattermost MCP** — 7 tools: read channels, post, search messages
- **Uptime Kuma MCP** — 5 tools: monitor health, incidents, response times
- **Ollama MCP** — 4 tools: list models, generate, chat, pull
- **Grafana MCP** — 6 tools: dashboards, PromQL queries, alerts
- **Portainer MCP** — 6 tools: Docker Swarm services, stacks, containers
- **AdGuard MCP** — 8 tools: DNS filtering, blocklists, query log

51 tools. Everything local. Nothing goes to the cloud.

Example conversation I had yesterday:
> "Check all my Uptime Kuma monitors. If anything is down, find the VM on Proxmox and restart it. Then post a summary to #ops in Mattermost."

Claude did all of it without me touching a browser.

Repo: https://github.com/AI-Engineerings-at/homelab-mcp-bundle

What self-hosted tools would you want MCP servers for next?
(thinking about Home Assistant MCP next)
```

---

## 3. LinkedIn Post (für Joe's Profil)

```
🔧 We just open-sourced 8 MCP servers for self-hosted infrastructure.

Most AI integrations are built for cloud services — GitHub, Notion, Slack, Linear.

We built the self-hosted equivalents:

✅ Mattermost MCP — 7 tools for team communication
✅ n8n MCP — 7 tools for workflow automation
✅ Proxmox MCP — 8 tools for VM management
✅ Uptime Kuma MCP — 5 tools for service monitoring
✅ Ollama MCP — 4 tools for local AI models
✅ Grafana MCP — 6 tools for dashboards & monitoring
✅ Portainer MCP — 6 tools for Docker Swarm management
✅ AdGuard MCP — 8 tools for DNS filtering

51 tools. MIT licensed. Everything runs on your own hardware.

Why this matters:
→ Full AI assistant access to your infra — without sending data to third parties
→ GDPR-friendly: all data stays on-prem, ideal for EU businesses
→ Works with Claude Desktop, Cursor, Windsurf — anything that speaks MCP
→ First MCP servers built specifically for this self-hosted stack

Real example:
Ask Claude: "Check if all services are UP. If Grafana is down, restart the VM on Proxmox and notify #ops in Mattermost."
→ Claude does all of it. No browser needed.

This is the future of infrastructure management: conversational, AI-assisted, but 100% self-hosted.

→ GitHub (free): https://github.com/AI-Engineerings-at/homelab-mcp-bundle
→ More: https://ai-engineering.at

#MCP #SelfHosted #Homelab #AI #OpenSource #DevOps #Privacy #GDPR
```

---

## 4. Twitter/X Thread

**Tweet 1 (Hook):**
```
We just open-sourced 8 MCP servers for self-hosted infrastructure.

Give Claude / Cursor direct access to your homelab:
→ Proxmox VMs
→ n8n workflows
→ Mattermost channels
→ Uptime Kuma monitors
→ Ollama models

51 tools. MIT. Free.

🧵 Thread:
```

**Tweet 2 (Problem):**
```
Every MCP server is built for cloud services.

GitHub ✓ Notion ✓ Slack ✓ Linear ✓

But what about people running their own stack?

Mattermost instead of Slack.
n8n instead of Zapier.
Proxmox instead of AWS.
Ollama instead of OpenAI.

We fixed that. ↓
```

**Tweet 3 (The servers):**
```
The bundle:

🗨️ Mattermost MCP — read channels, post messages, search (7 tools)
⚙️ n8n MCP — manage workflows, trigger webhooks (7 tools)
🖥️ Proxmox MCP — list/start/stop VMs, monitor nodes (8 tools)
📡 Uptime Kuma MCP — health checks, incidents, response times (5 tools)
🤖 Ollama MCP — local LLMs, model management (4 tools)
📊 Grafana MCP — dashboards, PromQL, alerts (6 tools)
🐳 Portainer MCP — Docker Swarm, stacks, containers (6 tools)
🛡️ AdGuard MCP — DNS filtering, blocklists, query log (8 tools)
```

**Tweet 4 (Demo):**
```
Real conversation with Claude yesterday:

"Check Uptime Kuma. If anything's down, find the VM on Proxmox and restart it. Post a summary to #ops in Mattermost."

→ Claude did all of it.
No browser. No SSH. No clicking.

This is what AI + self-hosted infra looks like.
```

**Tweet 5 (Privacy angle):**
```
And the best part?

Everything stays on your hardware.

No data sent to third parties.
GDPR-friendly by design.

Works with Claude Desktop, Cursor, Windsurf — anything that speaks MCP.
```

**Tweet 6 (CTA):**
```
MIT licensed. Free forever.

→ GitHub: github.com/AI-Engineerings-at/homelab-mcp-bundle

⭐ Star if this is useful.
🔁 RT if you know someone running a homelab.

What self-hosted tool should we build next?
(Home Assistant?)
```

---

## 5. Dev.to Artikel Outline

**Titel:**
```
I Built 8 MCP Servers for the Entire Self-Hosted Stack (Proxmox, n8n, Mattermost, Grafana, Ollama, AdGuard + more)
```

**Subtitle/Tagline:**
```
51 tools that give your AI assistant full access to your homelab — without touching the cloud
```

**Tags:** `mcp`, `selfhosted`, `homelab`, `ai`, `opensource`

**Cover Image:** Screenshot von Claude Desktop mit allen 8 MCP Servern connected

---

### Artikel-Outline:

```
## Introduction
- Problem: Every MCP server is for cloud services
- My homelab setup (Proxmox, Docker Swarm, n8n, Mattermost, Ollama)
- The gap: no MCP servers for self-hosted tools
- What I built: 8 open-source MCP servers, 51 tools total

## What is MCP?
- Model Context Protocol — 2 paragraphs max
- Works with: Claude Desktop, Cursor, Windsurf
- Why it matters for homelab users

## The 8 Servers

### Mattermost MCP (7 tools)
- Tools list with descriptions
- Code example: posting a message
- Use case: AI-generated ops summaries

### n8n MCP (7 tools)
- Tools list with descriptions
- Code example: listing active workflows
- Use case: troubleshoot failed executions via AI

### Proxmox MCP (8 tools)
- Tools list with descriptions
- Code example: listing VMs
- Use case: AI-assisted VM management

### Uptime Kuma MCP (5 tools)
- Tools list with descriptions
- Code example: querying monitor status
- Use case: proactive incident response

### Ollama MCP (4 tools)
- Tools list with descriptions
- Code example: listing models
- Use case: AI-to-AI workflows (Claude calls Ollama)

### Grafana MCP (6 tools)
- Tools list with descriptions
- Code example: querying dashboard panels
- Use case: AI-driven monitoring insights

### Portainer MCP (6 tools)
- Tools list with descriptions
- Code example: listing Swarm services
- Use case: AI-assisted container management

### AdGuard MCP (8 tools)
- Tools list with descriptions
- Code example: checking DNS query log
- Use case: AI-powered DNS filtering management

## Installation & Setup
- Prerequisites
- Clone + pip install (all 8)
- claude_desktop_config.json snippet
- Quick test to verify connection

## Real-World Examples
- Example 1: Cross-service incident response
  "Check Uptime Kuma, if X is down restart on Proxmox, notify Mattermost"
- Example 2: Workflow audit
  "Which n8n workflows failed in the last 24h? Summarize in Mattermost"
- Example 3: Local AI pipeline
  "What Ollama models do I have? Run the infra-check prompt against llama3.1:8b"

## Architecture & Privacy
- Everything stays on-prem
- No data leaves the network
- GDPR implications for EU teams
- Diagram: Claude ↔ MCP Server ↔ Self-Hosted Service

## What's Next
- Planned: Home Assistant MCP
- Premium: Setup guide + support (coming soon)
- Community: PRs welcome

## Conclusion
- GitHub link
- CTA: Star / share / contribute
- "What should we build next?"
```

---

## Posting-Empfehlungen

| Platform | Bester Zeitpunkt | Ziel |
|----------|-----------------|------|
| **Hacker News** | Dienstag–Donnerstag, 9–11 Uhr ET | Front Page / Top Comments |
| **Reddit r/selfhosted** | Samstag Morgen | Upvotes, Community-Feedback |
| **Reddit r/homelab** | Sonntag Morgen | Community-Diskussion |
| **LinkedIn** | Dienstag, 8–9 Uhr | Professional reach, B2B |
| **Twitter/X** | Montag–Mittwoch, 12–14 Uhr | Virality, Retweets |
| **Dev.to** | Montag Früh | Devs, SEO-Langzeitwirkung |

**Reihenfolge empfohlen:**
1. GitHub (README polieren) → 2. Dev.to (SEO Basis) → 3. HN + Reddit (selber Tag) → 4. Twitter Thread → 5. LinkedIn

---

## Monetarisierung (Upsell — später)

> Nicht in den ersten Posts erwähnen. Erst Community aufbauen, dann pitchen.

**Phase 1 (Launch):** 100% gratis, MIT, Build community
**Phase 2 (nach 500 GitHub Stars):** Premium Setup Guide
- Komplettes Homelab-Setup (Proxmox + Swarm + alle 8 MCP Server)
- Video-Walkthrough
- Config-Templates
- Preis: ~29-49 EUR (Gumroad)

**Phase 3 (nach 1k Stars):** Premium Support
- 1-on-1 Setup-Hilfe
- Discord Community (paid tier)
- Custom MCP Server Development
- Preis: ~99-199 EUR/Monat

---

*Erstellt von @lisa01 für AI-Engineering.at | 2026-02-25*

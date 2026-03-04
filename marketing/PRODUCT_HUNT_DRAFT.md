# Product Hunt Launch Draft — Homelab MCP Bundle

> Stand: 2026-02-25 | Erstellt von @lisa01
> GitHub: https://github.com/AI-Engineerings-at/homelab-mcp-bundle

---

## Research: MCP Server auf Product Hunt

### Aktuelle Lage (Feb 2026)

MCP Server auf Product Hunt sind noch sehr dünn gesät. Die meisten Launches:
- **Anthropic MCP SDK** selbst — der Original-Launch
- Einzelne Cloud-Service-Server (GitHub MCP, Notion MCP, Linear MCP)
- Keine bekannten Bundles für Self-Hosted / Homelab

**Das ist unsere Chance**: Wir sind First Mover für die Self-Hosted / Homelab-Kategorie auf PH.

### Beste Format-Empfehlungen für PH Launch

1. **Tagline unter 60 Zeichen** — prägnant, nutzen-orientiert
2. **Thumbnail/Logo**: 240x240px, erkennbar bei kleiner Darstellung
3. **Gallery**: 4-6 Screenshots — Claude Desktop + connected MCP + Demo-Prompt
4. **Description**: 300 Wörter max, Problem → Solution → Features
5. **First comment vom Maker**: Persönliche Story + technische Details
6. **Kategorie**: Developer Tools > AI / Productivity
7. **Launch-Tag**: Dienstag oder Mittwoch, 00:01 PST

### Was gut performt bei PH

- Klares, visuelles Demo (Screenshot oder kurzes GIF)
- "First of its kind" Angle — wir haben ihn
- Starke Maker-Story in den Comments
- Frühzeitig Upvotes aus der Community (HN, Reddit)
- Auf PH aktiv sein und alle Kommentare beantworten

---

## Product Hunt Launch Draft

### Produkt-Name

```
Homelab MCP Bundle
```

### Tagline (unter 60 Zeichen)

```
8 MCP servers for your self-hosted infrastructure
```

**Alternativen:**
```
Give Claude full access to your homelab (8 MCP servers)
MCP servers for Proxmox, n8n, Mattermost, Ollama & more
The missing MCP bundle for self-hosted infrastructure
```

### Kategorie

`Developer Tools` → Subcategory: `AI`

### Thumbnail (240x240)

Vorschlag: Schwarzer Hintergrund, weißes Logo AI-Engineering.at + "51 tools" + die 8 Service-Icons (Proxmox, n8n, Mattermost etc.) in einem 4x2 Grid.

---

### Description (300 Wörter)

```
Every MCP server is built for cloud services — GitHub, Notion, Slack, Linear.

But a lot of us run our own stack: Mattermost instead of Slack, n8n instead of Zapier, Proxmox instead of AWS. There were no MCP servers for any of that.

We built them.

**The Homelab MCP Bundle** gives your AI assistant (Claude Desktop, Cursor, Windsurf) direct access to your entire self-hosted infrastructure:

🖥️ **Proxmox MCP** — Monitor nodes, list VMs, start/stop virtual machines
⚙️ **n8n MCP** — Manage workflows, check executions, trigger webhooks
🗨️ **Mattermost MCP** — Read channels, post messages, search across your workspace
📡 **Uptime Kuma MCP** — Query service health, incidents and response times
🤖 **Ollama MCP** — List local models, generate text, pull new models
📊 **Grafana MCP** — Query dashboards, run PromQL, monitor alerts
🐳 **Portainer MCP** — Manage Docker Swarm services, stacks and containers
🛡️ **AdGuard MCP** — DNS filtering, query logs, manage custom rules

**51 tools total. MIT licensed. Everything stays on your hardware.**

Real conversations you can have:

> "Check if all services are UP. If Grafana is down, restart the VM on Proxmox and post a summary to #ops in Mattermost."

> "Which n8n workflows failed in the last 24 hours?"

> "Show me top 10 blocked domains in AdGuard today."

Claude (or your AI of choice) does all of it. No browser. No SSH. No clicking.

100% self-hosted. GDPR-friendly. No data leaves your network.

We're running this in production on a 3-node Proxmox cluster with Docker Swarm. Happy to answer questions about the setup.

→ GitHub (free): github.com/AI-Engineerings-at/homelab-mcp-bundle
→ Premium guides + setup: ai-engineering.at
```

---

### Maker Comment (erster Kommentar nach Launch)

```
Hey Product Hunt! 👋

I'm Joe, and I run a homelab with Proxmox, Docker Swarm, n8n, and Mattermost.

When MCP came out, I immediately wanted to connect Claude to my infrastructure. But every existing MCP server was for cloud services — nothing for the self-hosted tools I actually use.

So I built them over a few weeks. 8 servers, 51 tools, all MIT licensed.

The use case that really convinced me: I asked Claude to "check Uptime Kuma, and if any service is down, find the VM on Proxmox, restart it, and post a summary to the #ops channel in Mattermost." It did all of it — no browser, no SSH, no clicking through dashboards.

**A few technical notes:**
- All servers are pure Python (3.11+), using the official MCP SDK
- Authentication is handled per-server (tokens, passwords, API keys)
- SSL verification is configurable — important for self-signed homelab certs
- Tested on Proxmox 8.x, n8n 1.x, Uptime Kuma 1.23+, Grafana 10.x

**What's coming next:**
- Home Assistant MCP (most requested)
- API token support for Proxmox (instead of password)
- Better error messages across all servers

Happy to answer any questions about MCP, homelab setups, or the specific implementation details. This is a passion project and I want it to be genuinely useful.

GitHub: https://github.com/AI-Engineerings-at/homelab-mcp-bundle
More: https://ai-engineering.at
```

---

### Screenshots für Gallery (4-6 Stück)

**Screenshot 1 — Hero Shot**
- Claude Desktop mit allen 8 MCP Servern in der Sidebar
- Caption: "8 MCP servers connected in Claude Desktop"

**Screenshot 2 — Cross-Service Demo**
- Claude führt einen Multi-Step Befehl aus (Uptime Kuma → Proxmox → Mattermost)
- Caption: "Cross-service automation in plain language"

**Screenshot 3 — Proxmox MCP**
- Claude listet VMs und Nodes auf
- Caption: "Manage Proxmox VMs without leaving your AI assistant"

**Screenshot 4 — n8n MCP**
- Claude zeigt Workflow-Executions
- Caption: "Monitor n8n workflows and trigger them on demand"

**Screenshot 5 — Grafana MCP**
- Claude führt PromQL Query aus und zeigt Ergebnisse
- Caption: "Query Grafana metrics in natural language"

**Screenshot 6 — Architektur-Diagramm**
- Simples ASCII/Visual Diagram: Claude ↔ MCP Servers ↔ Self-Hosted Services
- Caption: "Everything stays on your hardware. No data leaves your network."

---

### Tags / Topics

```
mcp, homelab, self-hosted, ai, developer-tools, proxmox, n8n, claude, open-source
```

---

## Launch Timeline Empfehlung

| Tag | Aktion |
|-----|--------|
| T-7 | Screenshots vorbereiten, Gallery finalisieren |
| T-3 | PH Draft einreichen, "upcoming" aktivieren |
| T-1 | Team informieren, Upvote-Links vorbereiten |
| T-0 | Launch (Dienstag 00:01 PST), Maker Comment posten |
| T-0 +1h | HN Show HN + Reddit gleichzeitig launchen |
| T-0 +4h | Twitter Thread |
| T-0 +8h | LinkedIn Post |
| T-0 alle | Alle PH Kommentare aktiv beantworten |

---

## KPIs für Erfolg

| Metrik | Ziel (Tag 1) | Langfristig |
|--------|-------------|-------------|
| PH Upvotes | 100+ | Top 5 of the Day |
| GitHub Stars | 50 | 500 in 30 Tagen |
| HN Comments | 20+ | — |
| Reddit Upvotes | 100+ | — |

---

*Erstellt von @lisa01 für AI-Engineering.at | 2026-02-25*

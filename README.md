# Homelab MCP Bundle

**8 Model Context Protocol Server für selbst-gehostete Infrastruktur**

Ermöglicht AI-Agents wie Claude Desktop direkten Zugriff auf die wichtigsten Homelab-Dienste — über natürliche Sprache.

> **Stand**: 2026-02 | **Alle Server live getestet** | **Python, keine Abhängigkeiten außer `mcp`**

---

## MCP Server Übersicht

| Server | Tools | Beschreibung |
|--------|-------|--------------|
| [mattermost-mcp](./mattermost-mcp/) | 5 | Channels, Posts lesen/schreiben, User, Suche |
| [n8n-mcp](./n8n-mcp/) | 5 | Workflows auflisten, ausführen, Executions prüfen |
| [proxmox-mcp](./proxmox-mcp/) | 6 | VMs/LXCs verwalten, Node-Status, Ressourcen |
| [uptime-kuma-mcp](./uptime-kuma-mcp/) | 3 | Service-Status, Uptime-%, Monitor-Dashboard |
| [ollama-mcp](./ollama-mcp/) | 4 | Lokale LLMs: generate, chat, models, pull |
| [portainer-mcp](./portainer-mcp/) | 5 | Docker Swarm Services, Stacks, Nodes, Logs |
| [adguard-mcp](./adguard-mcp/) | 6 | DNS-Stats, Querylog, Filter-Listen, Domain blockieren |
| [grafana-mcp](./grafana-mcp/) | 6 | Dashboards, PromQL-Queries, Alerts, Datasources, Annotations |

**40 Tools gesamt — alle ohne externe Abhängigkeiten**

---

## Schnellstart

### 1. Installation

```bash
# Alle Server auf einmal installieren
pip install mcp

# Optional: Virtuelle Umgebung
python3 -m venv .venv && source .venv/bin/activate
pip install mcp
```

### 2. Claude Desktop — Alle 6 Server konfigurieren

`~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mattermost": {
      "command": "python3",
      "args": ["/path/to/mcp-servers/mattermost-mcp/server.py"],
      "env": {
        "MM_TOKEN": "<dein-mattermost-token>",
        "MM_BASE_URL": "http://your-mattermost:8065/api/v4"
      }
    },
    "n8n": {
      "command": "python3",
      "args": ["/path/to/mcp-servers/n8n-mcp/server.py"],
      "env": {
        "N8N_API_KEY": "<dein-n8n-api-key>",
        "N8N_BASE_URL": "http://your-n8n:5678/api/v1"
      }
    },
    "proxmox": {
      "command": "python3",
      "args": ["/path/to/mcp-servers/proxmox-mcp/server.py"],
      "env": {
        "PVE_HOST": "your-proxmox-ip",
        "PVE_PASSWORD": "<dein-passwort>"
      }
    },
    "uptime-kuma": {
      "command": "python3",
      "args": ["/path/to/mcp-servers/uptime-kuma-mcp/server.py"],
      "env": {
        "KUMA_BASE_URL": "http://your-uptime-kuma:3001",
        "KUMA_STATUS_PAGE": "homelab"
      }
    },
    "ollama": {
      "command": "python3",
      "args": ["/path/to/mcp-servers/ollama-mcp/server.py"],
      "env": {
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "OLLAMA_DEFAULT_MODEL": "llama3.2:3b"
      }
    },
    "portainer": {
      "command": "python3",
      "args": ["/path/to/mcp-servers/portainer-mcp/server.py"],
      "env": {
        "PORTAINER_URL": "http://your-portainer:9000",
        "PORTAINER_PASSWORD": "<dein-passwort>"
      }
    },
    "adguard": {
      "command": "python3",
      "args": ["/path/to/mcp-servers/adguard-mcp/server.py"],
      "env": {
        "ADGUARD_URL": "http://your-adguard:3000",
        "ADGUARD_USER": "admin",
        "ADGUARD_PASSWORD": "<dein-passwort>"
      }
    }
  }
}
```

---

## Was du damit machen kannst

```
"Zeig mir alle VMs auf pve1"
→ Proxmox MCP: vms_list(node="pve1")

"Sind alle Services oben?"
→ Uptime Kuma MCP: monitors_status() → 24/24 UP ✅

"Schreib in #general: Deployment fertig"
→ Mattermost MCP: posts_create(channel_id="...", message="Deployment fertig")

"Welche n8n Workflows sind heute fehlgeschlagen?"
→ n8n MCP: executions_list(status="error")

"Generiere eine kurze Zusammenfassung mit llama3"
→ Ollama MCP: generate(prompt="...", model="llama3.2:3b")

"Zeig mir alle laufenden Docker Services"
→ Portainer MCP: services_list() → 31 services

"Was steht in den Grafana Logs?"
→ Portainer MCP: service_logs("monitoring_grafana", tail=30)

"Wie viele DNS-Anfragen wurden heute geblockt?"
→ AdGuard MCP: stats() → 45,230 queries | 12,847 blocked (28.4%)

"Blockiere ads.example.com"
→ AdGuard MCP: block_domain("ads.example.com") → Rule added
```

---

## Architektur

```
Claude Desktop
     │
     ├── mattermost-mcp ──→ Mattermost API (REST v4)
     ├── n8n-mcp ─────────→ n8n REST API v1
     ├── proxmox-mcp ─────→ Proxmox VE API (HTTPS)
     ├── uptime-kuma-mcp ─→ Uptime Kuma Status-Page API
     ├── ollama-mcp ──────→ Ollama API (localhost:11434)
     ├── portainer-mcp ───→ Portainer REST API → Docker Swarm
     ├── adguard-mcp ─────→ AdGuard Home REST API (DNS filtering)
     └── grafana-mcp ─────→ Grafana REST API (dashboards, PromQL, alerts)
```

---

## Anforderungen

- Python 3.10+
- `pip install mcp` (einzige Abhängigkeit)
- Laufende Dienste: Mattermost, n8n, Proxmox VE, Uptime Kuma, Ollama, Portainer CE, AdGuard Home, Grafana

---

## Alle Server im Detail

- [Mattermost MCP →](./mattermost-mcp/README.md)
- [n8n MCP →](./n8n-mcp/README.md)
- [Proxmox MCP →](./proxmox-mcp/README.md)
- [Uptime Kuma MCP →](./uptime-kuma-mcp/README.md)
- [Ollama MCP →](./ollama-mcp/README.md)
- [Portainer MCP →](./portainer-mcp/README.md)
- [AdGuard Home MCP →](./adguard-mcp/README.md)
- [Grafana MCP →](./grafana-mcp/README.md)

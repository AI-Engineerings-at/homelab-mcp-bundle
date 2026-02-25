# Uptime Kuma MCP Server

Model Context Protocol Server für Uptime Kuma — ermöglicht AI-Agents Zugriff auf Service-Monitoring-Daten.

> **Marktlücke**: Kein kommerzieller Uptime Kuma MCP Server existiert (Stand: 2026-02)

## Features

| Tool | Beschreibung |
|------|--------------|
| `monitors_list` | Alle Monitors einer Status-Page auflisten |
| `monitors_status` | Aktueller UP/DOWN-Status aller Monitors mit Latenz |
| `status_overview` | Vollständiges Dashboard mit Uptime-% aus Heartbeat-History |

## Installation

```bash
pip install mcp
```

## Konfiguration

```bash
export KUMA_BASE_URL=http://localhost:3001      # Uptime Kuma URL (optional)
export KUMA_STATUS_PAGE=homelab                 # Status-Page Slug (optional)
```

> **Hinweis**: Verwendet die **öffentliche** Status-Page API — kein Login erforderlich, solange die Status-Page öffentlich ist.

## Claude Desktop Konfiguration

`~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "uptime-kuma": {
      "command": "python3",
      "args": ["/path/to/uptime-kuma-mcp/server.py"],
      "env": {
        "KUMA_BASE_URL": "http://your-uptime-kuma:3001",
        "KUMA_STATUS_PAGE": "homelab"
      }
    }
  }
}
```

## Beispiele

```
# Alle Monitors auflisten
monitors_list()
→ 24 Monitors in 7 Gruppen

# Aktuellen Status prüfen
monitors_status()
→ 24/24 UP | Health: 100%
→ Avg latency: 6ms

# Vollständiges Dashboard
status_overview()
→ docker-swarm: UP, 6ms, 99.8% uptime
→ pve: UP, 1ms, 100% uptime
```

## Status-Page einrichten

Die Uptime Kuma Status-Page muss öffentlich zugänglich sein:
1. Uptime Kuma → Status Pages → Neue Seite erstellen
2. Slug festlegen (z.B. `homelab`)
3. Monitors zuweisen
4. Öffentlich schalten

## Anforderungen

- Uptime Kuma 1.21+
- Python 3.10+
- `mcp[cli]>=1.0.0`

# Portainer MCP Server

Model Context Protocol Server für Portainer CE — ermöglicht AI-Agents Zugriff auf Docker Swarm via Portainer REST API.

> **Marktlücke**: Kein kommerzieller Portainer MCP Server existiert (Stand: 2026-02)

## Features

| Tool | Beschreibung |
|------|--------------|
| `services_list` | Alle Swarm Services mit Replikas-Status und Image |
| `service_logs` | Log-Zeilen eines Services abrufen |
| `stacks_list` | Alle Stacks aus Service-Labels (10 Stacks aus 31 Services) |
| `nodes_list` | Swarm-Nodes mit Leader, Status, Verfügbarkeit |
| `containers_list` | Container-Übersicht (laufend oder alle) |

## Installation

```bash
pip install mcp
```

## Konfiguration

```bash
export PORTAINER_URL=http://your-portainer:9000
export PORTAINER_USER=admin
export PORTAINER_PASSWORD=<dein-passwort>
export PORTAINER_ENDPOINT_ID=1   # optional, Standard: 1
```

## Claude Desktop Konfiguration

`~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "portainer": {
      "command": "python3",
      "args": ["/path/to/portainer-mcp/server.py"],
      "env": {
        "PORTAINER_URL": "http://your-portainer:9000",
        "PORTAINER_PASSWORD": "<dein-passwort>"
      }
    }
  }
}
```

## Beispiele

```
services_list()
→ 31 Swarm Services (adguard, monitoring, agents, ...)

service_logs("monitoring_grafana", tail=30)
→ Letzte 30 Log-Zeilen von Grafana

stacks_list()
→ 10 Stacks: adguard (3), monitoring (7), agents (1), ...

nodes_list()
→ docker-swarm3: Leader | docker-swarm: Reachable | docker-swarm2: Reachable

containers_list()
→ Alle laufenden Container mit Ports
```

## Anforderungen

- Portainer CE 2.x
- Python 3.10+
- `mcp[cli]>=1.0.0`

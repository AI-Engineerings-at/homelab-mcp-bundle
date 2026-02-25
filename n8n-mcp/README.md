# n8n MCP Server

Model Context Protocol Server für n8n Workflow Automation — ermöglicht AI-Agents direkten Zugriff auf n8n.

> **Marktlücke**: Kein kommerzieller n8n MCP Server existiert (Stand: 2026-02)

## Features

| Tool | Beschreibung |
|------|--------------|
| `workflows_list` | Alle Workflows auflisten (mit Pagination) |
| `workflows_get` | Einzelnen Workflow abrufen (inkl. Nodes) |
| `workflows_execute` | Workflow via Webhook ausführen |
| `executions_list` | Ausführungen auflisten (Filter: status, workflow) |
| `executions_get` | Einzelne Ausführung abrufen (inkl. Fehlerdetails) |

## Installation

```bash
pip install mcp
```

## Konfiguration

```bash
export N8N_API_KEY=<dein-n8n-api-key>
export N8N_BASE_URL=http://your-n8n-host:5678/api/v1   # optional
export N8N_WEBHOOK_BASE=http://your-n8n-host:5678/webhook  # optional
```

API Key liegt in: `~/.claude/.n8n-api-key`

## Nutzung

### Direkt starten

```bash
N8N_API_KEY=$(cat ~/.claude/.n8n-api-key) python3 server.py
```

### Claude Desktop Konfiguration

`~/.claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "n8n": {
      "command": "python3",
      "args": ["/home/joe/Playbook01/mcp-servers/n8n-mcp/server.py"],
      "env": {
        "N8N_API_KEY": "<api-key>",
        "N8N_BASE_URL": "http://your-n8n-host:5678/api/v1",
        "N8N_WEBHOOK_BASE": "http://your-n8n-host:5678/webhook"
      }
    }
  }
}
```

## Test

```bash
cd /home/joe/Playbook01/mcp-servers/n8n-mcp
N8N_API_KEY=$(cat ~/.claude/.n8n-api-key) python3 test.py
```

## Use Cases

- AI-Agent löst Workflows automatisch aus (z.B. "Sende jetzt den Newsletter")
- Monitoring: "Welche Workflows sind in den letzten 24h fehlgeschlagen?"
- Orchestrierung: AI koordiniert mehrere n8n Workflows
- Debugging: "Was ist beim letzten Stripe-Workflow schiefgelaufen?"

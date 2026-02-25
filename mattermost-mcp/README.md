# Mattermost MCP Server

Model Context Protocol Server für Mattermost — ermöglicht AI-Agents direkten Zugriff auf Mattermost.

## Features

| Tool | Beschreibung |
|------|--------------|
| `channels_list` | Alle Channels auflisten (mit Pagination) |
| `posts_read` | Posts aus Channel lesen (neueste zuerst) |
| `posts_create` | Neuen Post erstellen (inkl. Thread-Replies) |
| `users_list` | User auflisten |
| `posts_search` | Posts nach Stichworten suchen |

## Installation

```bash
pip install mcp
```

## Konfiguration

```bash
export MM_TOKEN=<dein-mattermost-token>
export MM_BASE_URL=http://10.40.10.83:8065/api/v4   # optional
export MM_TEAM_ID=yhtr94a73pd7tmwg6arr34k1ow         # optional
```

## Nutzung

### Direkt starten (stdio mode — fuer Claude Desktop)

```bash
MM_TOKEN=pd5bcjnin3gi5bsuoqi4atyoyc python3 server.py
```

### Claude Desktop Konfiguration

`~/.claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mattermost": {
      "command": "python3",
      "args": ["/home/joe/Playbook01/mcp-servers/mattermost-mcp/server.py"],
      "env": {
        "MM_TOKEN": "pd5bcjnin3gi5bsuoqi4atyoyc",
        "MM_BASE_URL": "http://10.40.10.83:8065/api/v4",
        "MM_TEAM_ID": "yhtr94a73pd7tmwg6arr34k1ow"
      }
    }
  }
}
```

## Test

```bash
cd /home/joe/Playbook01/mcp-servers/mattermost-mcp
MM_TOKEN=pd5bcjnin3gi5bsuoqi4atyoyc python3 test.py
```

## Token-Übersicht (Teambot-Tokens)

| Bot | Token-Variable |
|-----|---------------|
| lisa01 | `MM_LISA01_TOKEN` |
| claude | `MM_CLAUDE_TOKEN` |
| jim | `MM_JIM_TOKEN` |
| gemini | `MM_GEMINI_TOKEN` |

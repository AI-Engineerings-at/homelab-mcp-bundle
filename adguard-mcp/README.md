# AdGuard Home MCP Server

Model Context Protocol Server for AdGuard Home — enables AI agents to monitor and manage DNS filtering via natural language.

> **Market gap**: No AdGuard Home MCP Server exists (as of 2026-02)

## Features

| Tool | Description |
|------|-------------|
| `status` | AdGuard version, protection state, DNS addresses |
| `stats` | 24h query statistics: total queries, blocked %, top domains/clients |
| `querylog` | Recent DNS query log with block reason and latency |
| `filtering_status` | Filter lists with rule counts and last update time |
| `block_domain` | Add a domain to the custom blocklist |
| `toggle_protection` | Enable/disable DNS protection |

**6 Tools — stdlib only, no extra dependencies**

## Installation

```bash
pip install mcp
```

## Configuration

```bash
export ADGUARD_URL=http://localhost:3000       # AdGuard Home URL
export ADGUARD_USER=admin                      # Username (default: admin)
export ADGUARD_PASSWORD=yourpassword           # Required
```

## Claude Desktop Configuration

`~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "adguard": {
      "command": "python3",
      "args": ["/path/to/adguard-mcp/server.py"],
      "env": {
        "ADGUARD_URL": "http://10.40.10.80:3053",
        "ADGUARD_USER": "admin",
        "ADGUARD_PASSWORD": "<your-password>"
      }
    }
  }
}
```

## Examples

```
# Check protection status
status()
→ v0.107.71 | Protection: ON | DNS: :53

# Get blocking stats
stats()
→ 45,230 queries today | 12,847 blocked (28.4%)
→ Top blocked: doubleclick.net (341), ads.google.com (289)

# Browse DNS query log
querylog(limit=20)
→ 20 recent queries | 6 blocked

# Search for specific domain
querylog(search="ads.youtube.com")
→ 3 entries | 3 blocked

# Block a tracker
block_domain("tracker.example.com")
→ Rule "||tracker.example.com^" added to custom blocklist

# Temporarily disable protection
toggle_protection(enabled=False)
→ DNS protection disabled
```

## High Availability Setup

Works with both primary and secondary AdGuard instances:

```json
{
  "mcpServers": {
    "adguard-primary": {
      "command": "python3",
      "args": ["/path/to/adguard-mcp/server.py"],
      "env": {
        "ADGUARD_URL": "http://10.40.10.80:3053",
        "ADGUARD_PASSWORD": "<password>"
      }
    },
    "adguard-secondary": {
      "command": "python3",
      "args": ["/path/to/adguard-mcp/server.py"],
      "env": {
        "ADGUARD_URL": "http://10.40.10.82:3054",
        "ADGUARD_PASSWORD": "<password>"
      }
    }
  }
}
```

## Requirements

- AdGuard Home v0.107+
- Python 3.10+
- `mcp[cli]>=1.0.0`

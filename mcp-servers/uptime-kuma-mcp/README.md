# Uptime Kuma MCP Server

**Query your Uptime Kuma monitoring from any MCP-capable AI assistant.**

> Built by [AI-Engineering.at](https://ai-engineering.at) — Self-Hosted AI Infrastructure.

---

## What is this?

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that gives AI assistants
(Claude, Cursor, etc.) direct access to your [Uptime Kuma](https://github.com/louislam/uptime-kuma) instance.

**Ask your AI about service health, incidents and response times — in plain language.**

No webhooks, no extra config. Reads directly from Uptime Kuma's Prometheus metrics endpoint.

---

## Tools (5)

| Tool | Description |
|------|-------------|
| `get_summary` | Health overview: UP/DOWN counts, active incidents |
| `list_monitors` | All monitors with status + response time |
| `get_monitors_down` | Only DOWN/PENDING monitors (incident view) |
| `get_monitor` | Details for one monitor by name |
| `list_status_pages` | Public status page list with URLs |

---

## Requirements

- Python 3.11+
- Uptime Kuma 1.18+ with Prometheus metrics enabled
- Uptime Kuma username and password

---

## Quick Start

```bash
# 1. Install
pip install -e .

# 2. Configure
export KUMA_BASE_URL=http://your-kuma-host:3001
export KUMA_USERNAME=your_username
export KUMA_PASSWORD=your_password

# 3. Run
uptime-kuma-mcp
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KUMA_BASE_URL` | *(required)* | Uptime Kuma URL, e.g. `http://10.0.0.1:3001` |
| `KUMA_USERNAME` | *(required)* | Uptime Kuma login username |
| `KUMA_PASSWORD` | *(required)* | Uptime Kuma login password |

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "uptime-kuma": {
      "command": "uptime-kuma-mcp",
      "env": {
        "KUMA_BASE_URL": "http://YOUR_KUMA_IP:3001",
        "KUMA_USERNAME": "your_username",
        "KUMA_PASSWORD": "your_password"
      }
    }
  }
}
```

### Claude Code CLI

```bash
claude mcp add uptime-kuma uptime-kuma-mcp \
  -e KUMA_BASE_URL=http://YOUR_KUMA_IP:3001 \
  -e KUMA_USERNAME=your_username \
  -e KUMA_PASSWORD=your_password
```

---

## Example Prompts

```
"Are all my services UP right now?"
"What's currently down or in trouble?"
"Show me the response time for Grafana and n8n"
"Which monitors have been flapping recently?"
"Give me a status summary of all monitors"
```

---

## How it works

Reads the Prometheus `/metrics` endpoint exposed by Uptime Kuma.
This provides real-time monitor status, response times and SSL certificate expiry —
without needing the socket.io API or additional tokens.

**Status values**: `1=UP`, `0=DOWN`, `2=PENDING`, `3=MAINTENANCE`

---

## Enable Prometheus in Uptime Kuma

Settings → General → Enable Prometheus metrics endpoint → Save

The endpoint will be available at: `http://your-kuma:3001/metrics`

---

## Roadmap (v0.2+)

- [ ] `get_heartbeat_history` — Response time trends over time
- [ ] `get_ssl_expiry` — SSL certificate expiry dates
- [ ] `pause_monitor` / `resume_monitor` — Temporarily silence alerts
- [ ] Webhook-based real-time alerts push to AI
- [ ] Docker image for zero-config deployment

---

## License

MIT — use freely, modify and resell.

---

*Made with love by the AI-Engineering.at team.*

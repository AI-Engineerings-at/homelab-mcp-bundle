# n8n MCP Server

> **Manage n8n workflows directly from Claude, Cursor or any MCP-capable AI.**

Connect your n8n automation platform to any AI assistant via the [Model Context Protocol](https://modelcontextprotocol.io). List workflows, check execution history, activate/deactivate automations, and trigger webhooks — all from a natural-language conversation.

---

## Why this exists

There is **no commercial n8n MCP server** on the market. If you run n8n for automation and want AI to manage your workflows, this is your solution.

---

## Tools (7)

| Tool | Description |
|------|-------------|
| `list_workflows` | List all workflows with id, name, active status and tags |
| `get_workflow` | Full details of a workflow incl. all nodes |
| `activate_workflow` | Activate a workflow (enable its triggers) |
| `deactivate_workflow` | Deactivate a workflow |
| `list_executions` | Recent executions — filter by workflow or status |
| `get_execution` | Full execution details incl. node outputs and errors |
| `trigger_webhook` | POST to a webhook-triggered workflow |

---

## Quick Start

### 1. Install

```bash
git clone https://github.com/AI-Engineerings-at/Playbook01
cd mcp-servers/n8n-mcp
pip install -e .
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your n8n URL and API key
```

Get your API key: n8n → Settings → API → Create new API key

### 3. Add to Claude Desktop

Copy `claude_desktop_config.example.json` into your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "n8n": {
      "command": "python",
      "args": ["-m", "n8n_mcp.server"],
      "env": {
        "N8N_BASE_URL": "http://your-n8n-host:5678",
        "N8N_API_KEY": "your_api_key"
      }
    }
  }
}
```

---

## Example Prompts

```
"List all active n8n workflows"
"Show me the last 10 executions of workflow 42"
"Why did the Stripe workflow fail? Check the last execution"
"Activate the daily-report workflow"
"Trigger the webhook at /webhook/process-order with payload {order_id: 123}"
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `N8N_BASE_URL` | `http://10.40.10.80:5678` | Your n8n instance URL |
| `N8N_API_KEY` | *(required)* | n8n API key |

---

## Requirements

- Python 3.11+
- n8n with API access enabled (Settings → API)
- `mcp>=1.0.0`, `httpx>=0.27.0`

---

## n8n API Reference

This server uses the [n8n REST API v1](https://docs.n8n.io/api/api-reference/).

---

*Built by [ai-engineering.at](https://ai-engineering.at) — Self-Hosted AI Infrastructure*

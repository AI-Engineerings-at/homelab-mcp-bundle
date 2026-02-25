# Portainer MCP Server

**Docker Swarm management via Model Context Protocol**

Connect any MCP-capable AI (Claude, Cursor, Zed, ...) directly to your Portainer instance. Inspect services, stream logs, check node health and deploy stacks — all from natural language.

---

## Tools

| Tool | Description |
|------|-------------|
| `services_list` | List all Swarm services with replica counts and update state |
| `service_logs` | Stream recent logs for any service (last N lines) |
| `stacks_list` | List all Portainer stacks (name, status, type) |
| `stack_deploy` | Deploy or update a stack with a compose file |
| `node_status` | List Swarm nodes with role, availability and health |
| `containers_list` | List all containers (optionally filtered by node) |

---

## Requirements

- Python ≥ 3.11
- Portainer CE or EE ≥ 2.x
- Docker Swarm cluster

```bash
pip install -r requirements.txt
# or
pip install -e .
```

---

## Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

### Auth: API Access Token (recommended)

1. Log into Portainer → click your username (top right) → **My Account**
2. Scroll to **Access Tokens** → **Add access token**
3. Give it a name (e.g. `mcp-server`) and copy the token

```env
PORTAINER_URL=http://10.40.10.80:9000
PORTAINER_API_TOKEN=ptr_your_token_here
PORTAINER_ENDPOINT_ID=1
```

### Auth: Username + Password (fallback)

```env
PORTAINER_URL=http://10.40.10.80:9000
PORTAINER_USER=admin
PORTAINER_PASSWORD=your_password
PORTAINER_ENDPOINT_ID=1
```

---

## Usage

### Standalone

```bash
PORTAINER_API_TOKEN=ptr_... python3 -m portainer_mcp.server
```

### Claude Desktop

Add to `claude_desktop_config.json` (see `claude_desktop_config.example.json`):

```json
{
  "mcpServers": {
    "portainer": {
      "command": "python3",
      "args": ["-m", "portainer_mcp.server"],
      "env": {
        "PORTAINER_URL": "http://10.40.10.80:9000",
        "PORTAINER_API_TOKEN": "ptr_your_token_here",
        "PORTAINER_ENDPOINT_ID": "1"
      }
    }
  }
}
```

---

## Example Prompts

```
"Show me all running Swarm services and their replica counts"
"Get the last 200 log lines from the agents_service-monitor service"
"Which Swarm nodes are currently healthy?"
"List all stacks and tell me which ones are inactive"
"Deploy the updated compose file to the monitoring stack"
```

---

## Finding the Endpoint ID

```bash
curl -s -H "X-API-Key: ptr_your_token" http://10.40.10.80:9000/api/endpoints | python3 -m json.tool
```

The `Id` field of your Docker/Swarm endpoint is the `PORTAINER_ENDPOINT_ID`.

---

## Security Notes

- **Never** commit your `.env` file (it's in `.gitignore`)
- Use API access tokens instead of username/password where possible
- API tokens can be revoked individually in Portainer
- The `stack_deploy` tool applies changes immediately to the live cluster — use with care

---

## Part of the AI-Engineering Homelab MCP Bundle

This is one of 6 MCP servers in the bundle:

| Server | Description |
|--------|-------------|
| `portainer-mcp` | Docker Swarm via Portainer |
| `n8n-mcp` | Workflow automation |
| `proxmox-mcp` | VM & node management |
| `uptime-kuma-mcp` | Uptime monitoring |
| `ollama-mcp` | Local LLM inference |
| `mattermost-mcp` | Team messaging |

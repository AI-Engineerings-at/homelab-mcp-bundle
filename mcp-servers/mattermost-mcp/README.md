# Mattermost MCP Server

**Read, post and search Mattermost from any MCP-capable AI assistant.**

> Built by [AI-Engineering.at](https://ai-engineering.at) — the first commercial Mattermost MCP Server.

---

## What is this?

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that gives AI assistants
(Claude, Cursor, etc.) full access to your Mattermost workspace.

**No more copy-pasting from Mattermost into your AI chat.**
The AI reads your channels, posts answers and searches messages — directly.

---

## Features (v0.1)

| Tool             | Description                                              |
|------------------|----------------------------------------------------------|
| `list_channels`  | List all public channels in the team                     |
| `get_channel_info` | Get channel metadata by name or ID                    |
| `read_channel`   | Read recent posts from any channel                       |
| `post_message`   | Post a message (plain text or Markdown, with threading)  |
| `list_users`     | List all team members                                    |
| `get_mentions`   | Get all posts that mention a specific user               |
| `search_posts`   | Full-text search across all team posts                   |

---

## Requirements

- Python 3.11+
- Mattermost 7.x or newer (REST API v4)
- Personal Access Token with `read_channel`, `post`, `read_users` permissions

---

## Quick Start

```bash
# 1. Install dependencies
pip install mcp httpx

# 2. Set environment variables
export MM_BASE_URL="https://your-mattermost.example.com"
export MM_TOKEN="your_personal_access_token"
export MM_TEAM_ID="your_team_id"

# 3. Run the server
python3 src/mattermost_mcp/server.py
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mattermost": {
      "command": "python3",
      "args": ["/path/to/mattermost-mcp/src/mattermost_mcp/server.py"],
      "env": {
        "MM_BASE_URL": "https://your-mattermost.example.com",
        "MM_TOKEN":    "your_personal_access_token",
        "MM_TEAM_ID":  "your_team_id"
      }
    }
  }
}
```

---

## Getting Your Team ID

```bash
# Via API (replace TOKEN and URL)
curl -H "Authorization: Bearer TOKEN" \
     https://your-mattermost.example.com/api/v4/teams \
     | python3 -m json.tool | grep '"id"'
```

---

## Self-Hosted Mattermost

Works perfectly with self-hosted instances (HTTP or HTTPS). Just set `MM_BASE_URL` accordingly:

```bash
export MM_BASE_URL="http://10.40.10.83:8065"
```

---

## Security Notes

- Use a **Personal Access Token** — never your password
- Create a dedicated bot account for production use
- Tokens can be revoked anytime in Mattermost → Settings → Security
- Never commit `.env` to git (it's in `.gitignore`)

---

## Roadmap (v0.2+)

- [ ] `create_channel` — Create new channels
- [ ] `get_file` — Download file attachments
- [ ] `add_reaction` — React to posts with emoji
- [ ] `get_thread` — Read full thread replies
- [ ] Docker image for zero-config deployment
- [ ] OAuth 2.0 support (no personal token needed)
- [ ] Webhook-based real-time notifications

---

## License

MIT — use freely, modify and resell.

---

*Made with love by the AI-Engineering.at team.*

# Mattermost MCP Server

Model Context Protocol Server for Mattermost — gives AI agents direct access to Mattermost channels, posts, and users.

## Features

| Tool | Description |
|------|-------------|
| `channels_list` | List all channels (with pagination) |
| `posts_read` | Read posts from a channel (newest first) |
| `posts_create` | Create a new post (incl. thread replies) |
| `users_list` | List users |
| `posts_search` | Search posts by keyword |

## Installation

```bash
pip install mcp
```

## Configuration

```bash
export MM_TOKEN=your-mattermost-bot-token       # required
export MM_BASE_URL=http://your-mattermost:8065/api/v4   # optional, default shown
export MM_TEAM_ID=your-team-id                  # optional
```

## Usage

### Start directly (stdio mode — for Claude Desktop)

```bash
export MM_TOKEN=your-mattermost-bot-token
python3 server.py
```

### Claude Desktop Configuration

`~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mattermost": {
      "command": "python3",
      "args": ["/path/to/mattermost-mcp/server.py"],
      "env": {
        "MM_TOKEN": "your-mattermost-bot-token",
        "MM_BASE_URL": "http://your-mattermost:8065/api/v4",
        "MM_TEAM_ID": "your-team-id"
      }
    }
  }
}
```

## Running Tests

```bash
cd mattermost-mcp
export MM_TOKEN=your-mattermost-bot-token
export MM_TEST_CHANNEL_ID=your-channel-id
export MM_TEAM_ID=your-team-id
python3 test.py
```

## Getting a Mattermost Token

1. Log in to Mattermost
2. Go to **Profile → Security → Personal Access Tokens**
3. Click **Create Token**
4. Copy the token and set it as `MM_TOKEN`

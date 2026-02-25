# 8 Free MCP Servers for Claude Desktop: Control Your Homelab with Natural Language

> **SEO Target Keywords**: MCP servers Claude Desktop, Model Context Protocol homelab, Claude Code tools, free MCP servers 2025, AI homelab automation
> **Word Count**: ~2000 | **Reading Time**: 8 min | **Published**: 2026-02-25
> **Author**: AI-Engineering.at

---

## Introduction

Imagine telling your AI assistant "show me which Docker services are down" and instantly getting a live dashboard — no copy-pasting, no clicking through UIs. That's exactly what **Model Context Protocol (MCP)** makes possible with Claude Desktop.

MCP is Anthropic's open standard for connecting AI models to external tools and data sources. With the right MCP servers, Claude becomes a genuine ops engineer for your homelab. And the best part? Most MCP servers are completely free.

In this guide, I'll show you **8 free MCP servers** I'm running in my own homelab — and how you can do the same.

---

## What is MCP and Why Does It Matter?

The **Model Context Protocol** (MCP) lets Claude Desktop connect to external services through a standardized interface. Instead of just answering questions based on training data, Claude can:

- **Read** live data from your infrastructure
- **Execute** commands on your behalf
- **Manage** files, services, and databases in real time

Think of MCP servers as "plugins" that supercharge Claude's capabilities beyond conversation.

---

## The 8 Free MCP Servers for Your Homelab

### 1. Filesystem MCP — Read & Write Local Files

**What it does**: Gives Claude direct access to your local filesystem — read configs, write scripts, analyze logs.

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user"]
    }
  }
}
```

**Use case**: "Read my nginx.conf and tell me what's wrong with the SSL configuration."

---

### 2. GitHub MCP — Manage Repositories via Chat

**What it does**: Browse repos, create issues, review PRs — all through natural language.

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "your_token_here" }
    }
  }
}
```

**Use case**: "Create a GitHub issue for the failing health check workflow and assign it to me."

---

### 3. Brave Search MCP — Real-Time Web Research

**What it does**: Live web search directly inside Claude conversations — no hallucinated outdated info.

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": { "BRAVE_API_KEY": "your_key_here" }
    }
  }
}
```

**Use case**: "Search for the latest Proxmox VE security patches released this week."

---

### 4. PostgreSQL MCP — Query Databases Conversationally

**What it does**: Connect Claude directly to your Postgres databases. Query, analyze, even modify data via natural language.

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres",
               "postgresql://user:pass@localhost/db"]
    }
  }
}
```

**Use case**: "How many newsletter subscribers signed up this week? Show me the breakdown by day."

---

### 5. Puppeteer MCP — Browser Automation

**What it does**: Full browser automation — screenshots, form fills, web scraping — all via Claude commands.

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    }
  }
}
```

**Use case**: "Take a screenshot of my Grafana dashboard and save it to the reports folder."

---

### 6. Portainer MCP — Docker Swarm Control

**What it does**: Manage Docker Swarm services, stacks, and containers through Claude. Perfect for homelab orchestration.

This is a community-built MCP server (available via Portainer agent) that exposes:
- `services_list` — all running Swarm services with status
- `service_logs` — live logs from any service
- `stacks_list` — deployed stacks
- `nodes_list` — Swarm node health
- `containers_list` — per-node containers

**Use case**: "Which Docker services have less than the desired replica count right now?"

---

### 7. Prometheus MCP — Infrastructure Metrics via Chat

**What it does**: Query Prometheus metrics using natural language instead of PromQL.

```json
{
  "mcpServers": {
    "prometheus": {
      "command": "node",
      "args": ["path/to/prometheus-mcp/server.js"],
      "env": { "PROMETHEUS_URL": "http://10.40.10.80:9090" }
    }
  }
}
```

**Use case**: "Which server had the highest CPU usage in the last 24 hours and why?"

---

### 8. n8n MCP — Trigger Automation Workflows

**What it does**: Execute n8n workflows directly from Claude conversations. Bridge the gap between AI reasoning and automated actions.

With the n8n MCP integration you can:
- Trigger webhooks programmatically
- Chain AI reasoning with automation
- Get workflow execution results back in the conversation

**Use case**: "Run the Rapidmail newsletter campaign workflow for the new blog post."

---

## Setting Up MCP Servers: Step-by-Step

### Step 1: Install Claude Desktop

Download from [claude.ai/download](https://claude.ai/download). MCP support is available in the desktop app (not the web version).

### Step 2: Locate Your Config File

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

### Step 3: Add MCP Servers

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "ghp_yourtoken" }
    }
  }
}
```

### Step 4: Restart Claude Desktop

After editing the config, fully restart Claude Desktop. You'll see a tools icon (🔧) in the chat interface when MCP servers are active.

---

## Real-World Homelab Workflow Example

Here's a typical morning workflow I run with Claude + MCP:

1. **"Check overnight alerts"** → Prometheus MCP queries alert history
2. **"Show me which services restarted"** → Portainer MCP lists container restart counts
3. **"Create a summary issue"** → GitHub MCP creates a tracking issue
4. **"Send the report to Slack"** → n8n MCP triggers the notification workflow

What used to take 20 minutes of tab-switching takes 2 minutes of conversation.

---

## Performance & Security Considerations

**Performance**: MCP calls add ~50-200ms latency per tool invocation. For homelab use, this is negligible.

**Security**: MCP servers run locally on your machine. Be careful with:
- Filesystem access — limit to specific directories, not `/`
- Database access — use read-only credentials where possible
- Token storage — use environment variables, never hardcode in config

**Rate limits**: Most free MCP servers have no rate limits. Cloud-based ones (Brave Search, GitHub) use your API quotas.

---

## The AI-Engineering.at MCP Bundle

Want all 8 MCP servers pre-configured for homelab use? Our **[AI Agent Team Blueprint](https://ai-engineering.at/products)** includes:

- Pre-built MCP configurations for Proxmox, Docker Swarm, Prometheus, n8n
- Ready-to-use prompt templates for infrastructure management
- Step-by-step setup guide for DACH homelab environments

---

## Conclusion

MCP servers transform Claude from a conversational AI into an active infrastructure operator. With 8 free servers, you can control your entire homelab through natural language — from querying databases to triggering automation workflows.

The barrier to entry is low: install Claude Desktop, edit one JSON config file, and you're talking to your infrastructure.

**Start with the Filesystem and GitHub MCP servers** — they're zero-config and immediately useful. Then add Portainer and Prometheus as you get comfortable.

Your homelab deserves an AI operator. MCP makes it possible.

---

*AI-Engineering.at — KI-Automation für deutschsprachige Homelab-Enthusiasten und DevOps-Teams.*

*Follow us on [LinkedIn](https://linkedin.com/company/ai-engineering-at) | [GitHub](https://github.com/AI-Engineerings-at)*

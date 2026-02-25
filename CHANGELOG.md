# Changelog — Homelab MCP Bundle

All notable changes to the MCP Bundle are documented here.

Format: [Version] - Date | Author

---

## [v1.0.0] - 2026-02-25

**Initial release — 6 MCP Servers, 28 Tools**

### Added

#### mattermost-mcp (5 tools)
- `channels_list` — List channels with pagination (up to 200/page)
- `posts_read` — Read posts from channel (newest first, paginated)
- `posts_create` — Create post with optional thread reply support
- `users_list` — List team members with filter by team
- `posts_search` — Full-text search across team (AND/OR mode)

#### n8n-mcp (5 tools)
- `workflows_list` — List workflows with active filter and cursor pagination
- `workflows_get` — Get workflow with nodes and connection graph
- `workflows_execute` — Trigger workflow via webhook with custom payload
- `executions_list` — List executions filtered by status, workflow, limit
- `executions_get` — Get execution details including error info

#### proxmox-mcp (6 tools)
- `nodes_list` — Cluster nodes with CPU/RAM/disk usage percentages
- `vms_list` — All VMs and LXCs across nodes (optional node filter)
- `vm_status` — Live status with network/disk I/O stats
- `vm_start` — Start VM/LXC, returns UPID task ID
- `vm_stop` — Graceful ACPI shutdown or force stop
- `vm_resources` — Top CPU/RAM consumers + cluster totals

#### uptime-kuma-mcp (3 tools)
- `monitors_list` — All monitors from status page with group info
- `monitors_status` — Current UP/DOWN status with latency, sorted by state
- `status_overview` — Full dashboard with uptime % from heartbeat history

#### ollama-mcp (4 tools)
- `models_list` — Available models with size, family, quantization
- `generate` — Single-shot generation with system prompt + temperature
- `chat` — Multi-turn chat with message history
- `pull` — Download model from Ollama registry

#### portainer-mcp (5 tools)
- `services_list` — All Swarm services with replica counts and image
- `service_logs` — Stream log lines from any service (configurable tail)
- `stacks_list` — Stacks via Docker service label inspection (com.docker.stack.namespace)
- `nodes_list` — Swarm nodes with leader, reachability, engine version
- `containers_list` — Containers with ports (running or all)

### Infrastructure
- Pure Python implementation (stdlib only, no external HTTP libraries)
- Single dependency per server: `mcp[cli]>=1.0.0`
- Environment variable configuration (no hardcoded credentials)
- Bundle-level `.gitignore` (excludes `__pycache__`, `*.pyc`, `.env`)
- 6 individual READMEs + bundle overview README
- All servers live-tested against real homelab hardware

### Known Limitations
- Portainer `/api/stacks` only returns Portainer-managed stacks; CLI-deployed stacks are detected via service labels
- Uptime Kuma MCP uses public status-page API (requires public status page)
- Proxmox MCP uses ticket-based auth (auto-refreshed per request)

---

## [Unreleased] — v2.0.0 (Planned)

### Planned Additions
- **adguard-mcp** — DNS stats, query log, blocklist management
- **grafana-mcp** — Dashboard list, alert rules, datasource health
- **neo4j-mcp** — Cypher queries for knowledge graph access

---

*Homelab MCP Bundle | https://github.com/AI-Engineerings-at/Playbook01/tree/main/mcp-servers*

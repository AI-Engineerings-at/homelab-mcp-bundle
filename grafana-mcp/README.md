# Grafana MCP Server

Model Context Protocol Server for Grafana — enables AI agents to query dashboards, run PromQL, and monitor alerts via natural language.

> **Market gap**: No Grafana MCP Server exists (as of 2026-02)

## Features

| Tool | Description |
|------|-------------|
| `dashboards_list` | List all dashboards with folder, UID, tags (searchable) |
| `dashboard_get` | Get dashboard details + panel list by UID |
| `datasources_list` | List all configured datasources (Prometheus, Loki, etc.) |
| `alerts_list` | List all alert rules with current state (firing/normal) |
| `query_prometheus` | Run an instant PromQL query and get results |
| `annotations_list` | Get recent events, alert state changes, deployments |

**6 Tools — stdlib only, no extra dependencies**

## Installation

```bash
pip install mcp
```

## Configuration

```bash
export GRAFANA_URL=http://localhost:3000      # Grafana URL
export GRAFANA_USER=admin                     # Username (default: admin)
export GRAFANA_PASSWORD=yourpassword          # Password OR use API token:
export GRAFANA_TOKEN=glsa_xxxxx               # Service account token (preferred)
```

## Claude Desktop Configuration

`~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "grafana": {
      "command": "python3",
      "args": ["/path/to/grafana-mcp/server.py"],
      "env": {
        "GRAFANA_URL": "http://10.40.10.80:3000",
        "GRAFANA_USER": "admin",
        "GRAFANA_PASSWORD": "<your-password>"
      }
    }
  }
}
```

## Examples

```
# List all dashboards
dashboards_list()
→ 12 dashboards across 5 folders

# Search for specific dashboard
dashboards_list(query="docker")
→ Docker monitoring, Docker Swarm

# Get dashboard details
dashboard_get(uid="prometheus-stats")
→ Title: Docker monitoring | 8 panels | Prometheus datasource

# Check active alerts
alerts_list()
→ 6 rules total | 0 currently firing

# Run a PromQL query
query_prometheus(expr="node_memory_MemAvailable_bytes/node_memory_MemTotal_bytes*100")
→ docker-swarm: 42.3% | docker-swarm2: 38.7% | docker-swarm3: 51.2%

query_prometheus(expr="up")
→ 13 targets | all returning 1 (UP)

# Check recent annotations/events
annotations_list(limit=10)
→ Last deployment, alert state changes
```

## PromQL Examples for Homelab

```python
# Memory available %
query_prometheus(expr="node_memory_MemAvailable_bytes/node_memory_MemTotal_bytes*100")

# CPU usage per node
query_prometheus(expr="100 - (avg by(instance)(irate(node_cpu_seconds_total{mode='idle'}[5m]))*100)")

# Disk usage per mount
query_prometheus(expr="(1 - node_filesystem_free_bytes/node_filesystem_size_bytes)*100")

# Services UP/DOWN
query_prometheus(expr="up")

# Network traffic (bytes/s)
query_prometheus(expr="irate(node_network_receive_bytes_total{device='eth0'}[1m])")
```

## Requirements

- Grafana v9+
- Python 3.10+
- `mcp[cli]>=1.0.0`
- For `query_prometheus`: Prometheus datasource configured in Grafana

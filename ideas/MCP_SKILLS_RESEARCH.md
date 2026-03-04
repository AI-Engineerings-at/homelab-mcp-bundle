# MCP & Claude Code Research — Top-200 Shortlist
## Repo-Analyse: awesome-mcp-servers, claude-code-showcase, anthropics/skills
> Stand: 2026-02-25 | Fokus: DevOps / Docker / n8n / AI-Agents

---

## SOFORT-AKTIONSPLAN (Top 10)

| Prio | Action | Quelle |
|------|--------|--------|
| 1 | **Grafana MCP** zu `.mcp.json` hinzufuegen — Dashboards direkt abfragen | awesome-mcp-servers |
| 2 | **GitHub MCP** zu `.mcp.json` — PR Reviews, Issue Management | awesome-mcp-servers |
| 3 | `PreToolUse` Hook: Edits auf `main` Branch blockieren | claude-code-showcase |
| 4 | `docker-swarm-ops` SKILL.md fuer unseren Cluster bauen | anthropics/skills |
| 5 | `n8n-workflows` SKILL.md mit unseren Workflow-Patterns | anthropics/skills |
| 6 | **Alertmanager MCP** — Claude fragt Prometheus Alerts direkt ab | awesome-mcp-servers |
| 7 | `/deploy` Slash-Command fuer standardisierte Deployments | claude-code-showcase |
| 8 | `infrastructure-reviewer` Sub-Agent erstellen | claude-code-showcase |
| 9 | skill-eval Auto-Aktivierung fuer Docker/n8n/Prometheus Keywords | claude-code-showcase |
| 10 | `mcp-builder` Skill nutzen um Custom Portainer MCP Server zu bauen | anthropics/skills |

---

## TEIL 1: github.com/wong2/awesome-mcp-servers

> Kuratierte Liste von MCP Servern. Submissions gehen jetzt an mcpservers.org.
> Hunderte Server — von Anthropic Reference Implementations bis Corporate Integrations.

### Tier 1 — Reference Servers (ZUERST installieren)

Offizielle Anthropic/MCP Reference Implementations (`modelcontextprotocol/servers`):

| Server | Pfad | Use Case |
|--------|------|----------|
| **Git** | `.../src/git` | Git Repos aus Claude lesen, suchen, manipulieren |
| **Filesystem** | `.../src/filesystem` | Sichere File-Ops mit konfigurierbaren Access Controls |
| **Fetch** | `.../src/fetch` | Web Content fetchen und fuer LLM konvertieren |
| **Memory** | `.../src/memory` | Knowledge Graph persistentes Memory — perfekt fuer AIOps |
| **Sequential Thinking** | `.../src/sequentialthinking` | Strukturiertes Multi-Step Reasoning fuer Incident-Analyse |

### Tier 2 — Infrastructure & CI/CD

| Server | GitHub | Beschreibung |
|--------|--------|--------------|
| **Docker** | community | Docker Container, Compose, Logs via Claude verwalten |
| **Kubernetes** | community | K8s Cluster: Pods, Deployments, Services managen |
| **Harness** | `harness/mcp-server` | Pipelines, Repos, Logs, Artifact Registries |
| **CircleCI** | `CircleCI-Public/mcp-server-circleci` | AI Agents reparieren CI Build-Fehler automatisch |
| **GitHub** | `github/github-mcp-server` | OFFIZIELL: PRs, Issues, Repos, Actions |
| **GitKraken** | `gitkraken/gk-cli` | Wraps GitKraken, Jira, GitHub, GitLab in einem MCP |
| **Cloudflare** | `cloudflare/mcp-server-cloudflare` | Workers deployen, KV/R2/D1 konfigurieren |

### Tier 3 — Observability & Monitoring (DIREKT relevant fuer unser Stack!)

| Server | GitHub | Beschreibung |
|--------|--------|--------------|
| **Grafana** | `grafana/mcp-grafana` | Dashboards suchen, Incidents untersuchen, Datasources abfragen |
| **Alertmanager** | community | AI direkt mit Prometheus Alertmanager verbinden |
| **Axiom** | `axiomhq/mcp-server-axiom` | Logs und Traces in natuerlicher Sprache abfragen |
| **Dash0** | `dash0hq/mcp-dash0` | OpenTelemetry — Metrics, Logs, Traces |
| **Comet Opik** | `comet-ml/opik-mcp` | LLM Logs, Traces, Prompts abfragen — gut fuer Ollama Monitoring |

### Tier 4 — Databases

| Server | GitHub | Beschreibung |
|--------|--------|--------------|
| **Neo4j** | community | Graph DB Schema + Read/Write Cypher — **direkt fuer AIOps Neo4j** |
| **Chroma** | `chroma-core/chroma-mcp` | Vector Search, Embeddings, Document Storage — fuer AI/RAG |
| **Aiven** | `Aiven-Open/mcp-aiven` | PostgreSQL, Kafka, ClickHouse, OpenSearch |

### Tier 5 — Messaging & Notifications

| Server | GitHub | Beschreibung |
|--------|--------|--------------|
| **Ntfy** | community | ntfy Notifications senden/empfangen (self-hosted) |

### Tier 6 — Security & Networking

| Server | GitHub | Beschreibung |
|--------|--------|--------------|
| **Globalping** | `jsdelivr/globalping-mcp-server` | Ping, Traceroute, MTR, DNS Resolve — fuer Netzwerk-Diagnose |
| **E2B** | `e2b-dev/mcp-server` | Code in sicheren Sandboxes ausfuehren |
| **Cycode** | `cycodehq/cycode-cli` | SAST, SCA, Secrets & IaC Scanning |

### Tier 7 — AI-Agent Orchestration

| Server | GitHub | Beschreibung |
|--------|--------|--------------|
| **1mcpserver** | `particlefuture/1mcpserver` | MCP of MCPs — automatische Discovery anderer MCP Server |
| **AgentRPC** | `agentrpc/agentrpc` | Funktionen ueber Netzwerk-Grenzen verbinden — gut fuer Multi-Agent |

### .mcp.json Snippet — Sofort nutzbar

```json
{
  "mcpServers": {
    "grafana": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@grafana/mcp-grafana"],
      "env": {
        "GRAFANA_URL": "http://10.40.10.80:3000",
        "GRAFANA_API_KEY": "${GRAFANA_API_KEY}"
      }
    },
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@github/mcp-server"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "memory": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/joe"]
    }
  }
}
```

---

## TEIL 2: github.com/ChrisWiles/claude-code-showcase

> Production-Grade Reference Implementation fuer Claude Code in einem Engineering-Team.
> Zeigt echte Patterns aus einem funktionierenden React/TypeScript Codebase.

### Directory-Struktur Pattern

```
project-root/
├── CLAUDE.md                    # Projekt-Memory — laedt automatisch beim Start
├── .mcp.json                    # MCP Server Config (git-committed, team-shared)
├── .claude/
│   ├── settings.json            # Hooks, Env Vars, Permissions
│   ├── settings.local.json      # Persoenliche Overrides (gitignored)
│   ├── agents/                  # Spezialisierte Sub-Agents
│   │   └── code-reviewer.md     # Proaktiver Code-Review Agent
│   ├── commands/                # Slash Commands (/command-name)
│   │   ├── ticket.md            # End-to-End JIRA/Linear Ticket Workflow
│   │   ├── pr-review.md         # PR Review Workflow
│   │   └── onboard.md           # Deep Task Exploration
│   ├── hooks/                   # Hook Scripts
│   │   ├── skill-eval.sh        # Matcht Skills zu Prompts
│   │   ├── skill-eval.js        # Node.js Skill-Matching Engine
│   │   └── skill-rules.json     # Pattern-Matching Config
│   └── skills/                  # Domain Knowledge Docs
│       ├── testing-patterns/SKILL.md
│       ├── graphql-schema/SKILL.md
│       └── core-components/SKILL.md
```

### Pattern 1: Hook System fuer automatische Quality Gates

```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [{
          "type": "command",
          "command": "[ \"$(git branch --show-current)\" != \"main\" ] || { echo '{\"block\": true, \"message\": \"Cannot edit on main branch.\"}' >&2; exit 2; }",
          "timeout": 5
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [{
          "type": "command",
          "command": "if [[ \"$CLAUDE_TOOL_INPUT_FILE_PATH\" =~ \\.test\\.(js|ts)$ ]]; then npm test -- --findRelatedTests \"${CLAUDE_TOOL_INPUT_FILE_PATH}\" 2>&1; fi",
          "timeout": 90
        }]
      }
    ]
  }
}
```

**Hook Events:**

| Event | Wann | DevOps Use Case |
|-------|------|-----------------|
| `PreToolUse` | Vor Tool-Ausfuehrung | Edits auf main blockieren, gefaehrliche Commands validieren |
| `PostToolUse` | Nach Tool-Ausfuehrung | Auto-Lint, Tests, Type-Check |
| `UserPromptSubmit` | Bei Prompt-Submit | Context injizieren, Skills vorschlagen |
| `Stop` | Agent fertig | Mattermost Notification, Downstream Trigger |

Exit Codes: `0` = OK, `2` = Blocking Error (nur PreToolUse), andere = Non-blocking

### Pattern 2: Skill Auto-Aktivierung (skill-eval System)

```json
// skill-rules.json — DevOps Adaptation
{
  "skills": {
    "docker-swarm-ops": {
      "priority": 9,
      "triggers": {
        "keywords": ["docker", "compose", "swarm", "container", "stack"],
        "keywordPatterns": ["\\bdocker\\b", "\\bswarm\\b", "\\bcontainer\\b"],
        "pathPatterns": ["**/docker-compose*.yml", "**/Dockerfile*", "**/*.stack.yml"],
        "intentPatterns": [
          "(?:deploy|scale|restart).*(?:service|container)",
          "(?:docker|swarm).*(?:stack|service)"
        ]
      }
    },
    "n8n-workflows": {
      "priority": 8,
      "triggers": {
        "keywords": ["n8n", "workflow", "automation", "webhook"],
        "keywordPatterns": ["\\bn8n\\b", "\\bworkflow\\b"],
        "pathPatterns": ["**/*.workflow.json", "**/n8n/**"]
      }
    },
    "prometheus-monitoring": {
      "priority": 7,
      "triggers": {
        "keywords": ["prometheus", "grafana", "alert", "metric", "alertmanager"],
        "pathPatterns": ["**/*-rules.yml", "**/prometheus.yml", "**/alert*.yml"]
      }
    }
  }
}
```

### Pattern 3: Proaktiver Infrastructure-Reviewer Agent

```markdown
---
name: infrastructure-reviewer
description: PROAKTIV nach Infrastruktur-Aenderungen (Dockerfiles, Compose, n8n Workflows, Terraform)
model: sonnet
---

Review Infrastruktur-Aenderungen auf:
- Security: exponierte Ports, fehlende Resource Limits, hardcoded Secrets
- Docker: Resource Limits, Health Checks, non-root User, gepinnte Images
- n8n: Error-Handler auf jedem Produktions-Workflow, keine hardcoded Credentials
- Netzwerk: unnoetige Port-Exposures, fehlende Firewall Rules
```

### Pattern 4: Slash Commands fuer Workflow-Automation

```markdown
# .claude/commands/deploy.md
---
description: Service zu Docker Swarm deployen
allowed-tools: Bash(docker:*), Bash(ssh:*), Bash(git:*)
---

Deploy $ARGUMENTS nach Production:
1. Verifiziere Branch ist nicht main, pruefe CI Status
2. SSH zu docker-swarm3, inspiziere aktuellen Service-State
3. Pulle neues Image, update Service mit Rollback-Plan
4. Monitoring 60s, pruefe Health Endpoints
5. Poste Deployment-Summary in Mattermost #echo_log
```

### Pattern 5: GitHub Actions Scheduled Maintenance

```yaml
# .github/workflows/weekly-infra-audit.yml
on:
  schedule:
    - cron: '0 9 * * 1'  # Jeder Montag 09:00

jobs:
  infra-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: claude -p "Review Docker images fuer veraltete Base Images und erstelle Report"
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**DevOps Zeitplan:**
- Woechentlich: Docker Images auf veraltete Base Images pruefen
- Monatlich: n8n Workflow-Dokumentation aktualisieren
- Zweiwoechtlich: Prometheus Alert Rules auf veraltete/ungenutzte Alerts pruefen

---

## TEIL 3: github.com/anthropics/skills

> Anthropic's offizielles Skill Repository — Skills sind Verzeichnisse mit Instructions + Scripts.
> Funktionieren in Claude Code (via `/plugin`), Claude.ai und Claude API.

### Skill-Struktur — Das kanonische Format

Jeder Skill ist ein Verzeichnis mit `SKILL.md`:

```markdown
---
name: mein-skill-name
description: >
  Klare Beschreibung was dieser Skill macht und wann er genutzt wird.
  Keywords einschliessen die Claude mit Aktivierung assoziiert.
  Beispiel: "Nutzen beim Deployen von Docker Services, Verwalten von Docker Swarm Stacks,
  oder Arbeiten mit docker-compose Dateien. Auch aktivieren fuer: swarm, docker service."
license: Apache-2.0
---

# Skill Titel

[Instructions die Claude befolgt wenn dieser Skill aktiv ist]

## Uebersicht
## Nutzung (mit Beispielen)
## Guidelines
```

**Kritische Felder:**
- `name` — lowercase, Bindestriche statt Leerzeichen, eindeutig
- `description` — entscheidend fuer Aktivierung; Claude nutzt dies um zu entscheiden

### Skills im Anthropics Repo

| Skill | DevOps Relevanz |
|-------|-----------------|
| **mcp-builder** | HOCH — Custom MCP Server in TypeScript/Python bauen |
| **webapp-testing** | MITTEL — Playwright fuer n8n, Grafana, Portainer UIs |
| **skill-creator** | META — Neue Skills schnell bootstrappen |
| **internal-comms** | MITTEL — Mattermost Posts, Runbooks |

### mcp-builder — Wichtigste Best Practices

```typescript
// TypeScript MCP Server Pattern (empfohlen)
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({ name: "docker-swarm", version: "1.0.0" });

server.registerTool("docker_list_services", {
  description: "List all Docker Swarm services with their status",
  inputSchema: z.object({
    stack: z.string().optional().describe("Filter by stack name"),
  }),
  handler: async ({ stack }) => {
    // implementation
  }
});
```

**Quality Checklist:**
- Actionable Error Messages mit konkreten naechsten Schritten
- Pagination fuer grosse Result Sets
- Focused, relevante Daten — keine vollen API Dumps
- Tool Descriptions muessen LLM-lesbar sein
- 10 Q&A Paare schreiben die verifizieren dass MCP funktioniert

### Custom DevOps Skill Template — Komplett

```markdown
---
name: docker-swarm-ops
description: >
  Expert guide fuer Docker Swarm Clusters, Stacks und Services.
  Nutzen beim Deployen, Troubleshooting, Skalieren, Log-Checks.
  Keywords: swarm, docker service, docker stack, container restart.
---

# Docker Swarm Operations

## Cluster Info
- Leader: docker-swarm3 @ 10.40.10.83
- Manager: docker-swarm @ .80, docker-swarm2 @ .82
- SSH: ssh root@<ip>

## Haeufige Commands

### Service Management
```bash
# Alle Services auflisten
ssh root@10.40.10.80 "docker service ls"

# Service skalieren
ssh root@10.40.10.83 "docker service scale <service>=<replicas>"

# Update mit Rollback-Plan
ssh root@10.40.10.83 "docker service update --image <new-image> --rollback-on-failure <service>"

# Service Logs (letzte 50 Zeilen)
ssh root@10.40.10.80 "docker service logs --tail 50 <service>"
```

## Safety Rules
- NIEMALS docker prune ohne explizite Bestaetigung
- IMMER aktuelle Replica-Anzahl pruefen vor Scale-Down
- IMMER Health Endpoints nach Deployment verifizieren
- Fuer Prod-Aenderungen: vorher/nachher in #echo_log posten
```

### webapp-testing Skill — Reconnaissance Pattern

```python
# Playwright Pattern aus dem webapp-testing Skill
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Immer headless
    page = browser.new_page()
    page.goto('http://10.40.10.80:3000')         # Grafana
    page.wait_for_load_state('networkidle')      # KRITISCH fuer dynamische Apps
    page.screenshot(path='/tmp/grafana-check.png', full_page=True)
    browser.close()
```

**Reconnaissance-Then-Action Pattern:** Screenshot und DOM inspizieren BEVOR gehandelt wird.

### Skills installieren in Claude Code

```bash
# Anthropics Skill Marketplace hinzufuegen
/plugin marketplace add anthropics/skills

# Spezifische Skill Sets installieren
/plugin install document-skills@anthropic-agent-skills

# Oder lokale Skills nutzen — einfach in .claude/skills/ ablegen
```

---

## KEY RESOURCES

| Ressource | URL |
|-----------|-----|
| Awesome MCP Servers | https://github.com/wong2/awesome-mcp-servers |
| MCP Server Discovery | https://mcpservers.org |
| Claude Code Showcase | https://github.com/ChrisWiles/claude-code-showcase |
| Anthropics Skills | https://github.com/anthropics/skills |
| MCP Spec | https://modelcontextprotocol.io |
| Grafana MCP | https://github.com/grafana/mcp-grafana |
| GitHub MCP | https://github.com/github/github-mcp-server |

---

## NAECHSTE SCHRITTE (konkret)

### Woche 1
- [ ] Grafana MCP zu `.mcp.json` hinzufuegen und testen
- [ ] `docker-swarm-ops` SKILL.md in `.claude/skills/` erstellen
- [ ] `PreToolUse` Hook fuer main-Branch-Schutz einrichten

### Woche 2
- [ ] `n8n-workflows` SKILL.md mit unseren Patterns bauen
- [ ] `infrastructure-reviewer` Sub-Agent erstellen
- [ ] skill-eval System mit Docker/n8n/Prometheus Keywords konfigurieren

### Woche 3
- [ ] Custom Portainer MCP Server mit `mcp-builder` Skill bauen
- [ ] `/deploy` Slash-Command fuer standardisierte Deployments
- [ ] Neo4j MCP evaluieren fuer AIOps Knowledge Graph Abfragen

---
*Erstellt: 2026-02-25 | Autor: @lisa01 | Quelle: GitHub Research*

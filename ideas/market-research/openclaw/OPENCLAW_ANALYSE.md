# OpenClaw Research — Analyse für AI-Engineering.at

> **Stand**: 2026-02-25 | Analyst: @lisa01
> **Basis**: OpenClaw 2026.2.23 (b817600), 51 gebündelte Skills, clawhub.com Marketplace
> **Quelle**: Direktanalyse via `openclaw skills list`, SKILL.md Dateien, clawhub.com

---

## Was ist OpenClaw?

OpenClaw ist eine AI-Assistant-Plattform die über **Messaging-Channels** (Mattermost, Telegram,
WhatsApp, Discord) gesteuert wird und Skills (SKILL.md Files) nutzt um spezialisierte Aufgaben
auszuführen. Die Skills werden auf **clawhub.com** veröffentlicht und installiert.

**Kritisch für uns**: OpenClaw unterstützt Mattermost als Channel — unser Stack ist damit
nativ kompatibel!

**Unterschied zu Claude Code Skills**: OpenClaw Skills sind Markdown-Dateien die dem LLM
erklären wie es ein CLI-Tool nutzen soll. Kein Code, nur Instruktionen + Tool-Beschreibungen.

---

## Teil 1: Top 10 OpenClaw Skills die zu unserem Stack passen

Von 51 gebündelten Skills — sortiert nach Relevanz für Docker/n8n/Grafana/Proxmox:

### 🥇 Rang 1: `coding-agent` (✓ ready)
**Was es macht**: Delegiert Coding-Tasks an Claude Code, Codex, Pi-Agents via Background-Process.
**Warum für uns**: Direkter Multiplier für @jim01 und @lisa01. Anstatt manuell Claude Code
zu starten, kann OpenClaw (auf Mattermost-Befehl von @joe) eigenständig Claude Code-Tasks
spawnen. Perfekt für: PR-Reviews, Refactoring, neue Features bauen.
**Integration**: OpenClaw-Agent auf Fedora .99 startet Claude Code für Coding-Tasks in unserem Repo.

---

### 🥈 Rang 2: `github` (✓ ready)
**Was es macht**: GitHub Ops via `gh` CLI — Issues, PRs, CI-Runs, Code Review.
**Warum für uns**: Wir nutzen GitHub aktiv (AI-Engineering.at Repos). Von Mattermost aus
per `@openclaw PR status zeigen` — kein Browser-Wechsel mehr.
**Integration**: OpenClaw auf Fedora .99, `gh` CLI bereits konfiguriert.

---

### 🥉 Rang 3: `gh-issues` (✓ ready)
**Was es macht**: GitHub Issues fetchen, Sub-Agents spawnen um Fixes zu implementieren und
PRs zu öffnen. Mit `--cron` auch scheduled.
**Warum für uns**: Automatisches Issue-Monitoring. Täglich um 08:00 alle offenen Issues in
#echo_log posten? Einzeiler mit diesem Skill.
**Killer-Feature**: `--cron` Modus = Issues werden täglich automatisch geprüft ohne manuellen Trigger.

---

### Rang 4: `healthcheck` (✓ ready)
**Was es macht**: Host Security Hardening, Risk-Assessment, SSH/Firewall-Checks, OPNsense-Audits.
**Warum für uns**: Unser Security Audit Bundle Produkt-Idee (EUR 29) — dieser Skill wäre
das Herzstück. Auf OPNsense (.1) anwenden, Report in Mattermost bekommen.
**Produkt-Potential**: Skill + Bundle = fertiges Produkt-Paket.

---

### Rang 5: `tmux` (✓ ready)
**Was es macht**: Remote-control tmux Sessions auf Servern via Keystrokes + Pane-Output scraping.
**Warum für uns**: SSH-Session zu docker-swarm3 öffnen, `docker service ls` ausführen, Output
in Mattermost zurückbekommen. Ohne extra MCP-Server!
**Integration**: tmux läuft bereits auf unseren Swarm-Nodes als Session-Manager.

---

### Rang 6: `skill-creator` (✓ ready)
**Was es macht**: Skills erstellen und auf ClawHub publishen. Erklärung von SKILL.md-Format,
Scripts, Assets, metadata.
**Warum für uns**: WIR wollen Skills publishen! Dieser Skill ist unsere Produktions-Pipeline.
Mit diesem Skill können wir unsere eigenen Skills direkt aus OpenClaw heraus bauen.
**ROI**: Hebelt alle anderen Skill-Produkt-Ideen (Teil 3).

---

### Rang 7: `clawhub` (✓ ready)
**Was es macht**: ClawHub CLI für Search, Install, Update, Publish von Skills.
**Warum für uns**: Marketplace-Zugang. Skills installieren (`clawhub install portainer-ops`),
eigene Skills publishen (`clawhub publish`). Direkte Verbindung zu unserem Verkaufskanal.

---

### Rang 8: `mcporter` (✗ missing — aber installierbar!)
**Was es macht**: MCP-Server direkt aus OpenClaw ansprechen — list, configure, auth, call.
**Warum für uns**: Brücke zwischen OpenClaw und unseren 6 MCP-Servern! Mit mcporter können
unsere bestehenden MCP-Server auch ohne Claude Code genutzt werden.
**Install**: `clawhub install mcporter` → dann alle 6 unserer MCP-Server via OpenClaw steuerbar.

---

### Rang 9: `summarize` (✗ missing — aber installierbar!)
**Was es macht**: Zusammenfassen von URLs, Podcasts, lokalen Files. Fallback für YouTube/Video-Transcription.
**Warum für uns**: Content-Pipeline für AI-Engineering.at. Blog-Posts, YouTube-Videos von
Wettbewerbern zusammenfassen. Marktbeobachtung automatisieren.
**Use Case**: Täglich 5 relevante r/homelab Posts zusammenfassen → in Mattermost posten.

---

### Rang 10: `session-logs` (✗ missing — aber installierbar!)
**Was es macht**: Eigene Session-Logs durchsuchen und analysieren via jq.
**Warum für uns**: Debugging von OpenClaw-Workflows. Wenn ein Mattermost-Command fehlschlägt,
Session-Log durchsuchen ohne SSH zu brauchen.

---

## Teil 2: Unsere 6 MCP-Server als OpenClaw Skills portieren

**Aktueller Stand**: Wir haben 6 MCP-Server in `/home/joe/cli_bridge/mcp-servers/`:

| MCP-Server | Aktuell | Als OpenClaw Skill | Aufwand |
|------------|---------|-------------------|---------|
| portainer-mcp | 5 Tools (services, logs, stacks, nodes, containers) | `portainer-ops` | 2h |
| n8n-mcp | Workflow-Management | `n8n-ops` | 3h |
| mattermost-mcp | Channel/Message-Ops | `mattermost-ops` | 2h |
| proxmox-mcp | VM/Container-Control | `proxmox-ops` | 4h |
| uptime-kuma-mcp | Monitor-Status | `uptime-kuma-ops` | 2h |
| ollama-mcp | Local LLM Control | `ollama-ops` | 2h |

### Warum Skills statt MCP-Server?

**MCP-Server** brauchen Claude Code (Desktop oder CLI) → Zielgruppe: ~200K Claude Code Nutzer.
**OpenClaw Skills** funktionieren über Mattermost/Telegram/WhatsApp → Zielgruppe: ~alle mit Chat-App.

**Beide Formate publishen** = doppelte Reichweite mit gleichem Inhalt.

---

### Skill-Konzepte im Detail:

#### `portainer-ops` Skill (PRIORITÄT 1 — schnellster Launch)
```yaml
name: portainer-ops
description: >
  Manage Docker Swarm via Portainer CE API. List services, view logs,
  check stacks and nodes. Use when: checking service status, debugging
  container failures, viewing real-time logs. Requires Portainer URL + API token.
```
**Warum zuerst**: Portainer-MCP ist fertig → SKILL.md schreiben = 2h Arbeit.
**Unique**: Kein einziger portainer-skill auf clawhub.com (geprüft).

---

#### `proxmox-ops` Skill (PRIORITÄT 2 — höchster Marktwert)
```yaml
name: proxmox-ops
description: >
  Query and manage Proxmox VE clusters via API. List VMs/CTs, check
  resource usage, start/stop VMs, snapshot management. Supports
  multi-node clusters. Use for homelab management from any chat app.
```
**Warum wertvoll**: Proxmox = 500K+ Homelab-Nutzer. Kein offizieller MCP/Skill existiert.
**Install-Basis**: Wir betreiben 3-Node Proxmox-Cluster → getestete Skills.

---

#### `n8n-ops` Skill (PRIORITÄT 3 — Synergy mit bestehenden Produkten)
```yaml
name: n8n-ops
description: >
  Manage n8n workflows via REST API. List, activate/deactivate, trigger,
  and monitor workflows. Check execution logs. Use for workflow automation
  management from Mattermost/Telegram without web UI access.
```
**Synergie**: Unser n8n-Bundle (EUR 29) + dieser Skill = komplettes Paket.

---

#### `homelab-monitor` Skill (MEGA-SKILL — kombiniert Grafana + Prometheus + Uptime Kuma)
```yaml
name: homelab-monitor
description: >
  All-in-one homelab monitoring from your chat. Prometheus metrics,
  Grafana alerts, Uptime Kuma status, Node Exporter data. Query CPU/RAM/
  disk from any Docker Swarm node. Use when checking infrastructure health
  without opening multiple browser tabs.
```
**Differenzierung**: Kein einziger kombinierter Monitoring-Skill auf clawhub.com.
**Cross-Sell**: Perfekte Ergänzung zum Grafana Dashboard Pack (EUR 29).

---

## Teil 3: Neue Produkt-Ideen basierend auf OpenClaw

### Produkt-Idee A: "ClawHub DevOps Bundle" — Skills auf clawhub.com (EUR 19)

**Konzept**: 4 Skills auf clawhub.com publishen als Bundle:
- `portainer-ops` + `proxmox-ops` + `n8n-ops` + `homelab-monitor`
- Als freemium: Skills gratis auf clawhub.com + Premium-Bundle auf Gumroad mit Doku/Support

**Warum jetzt**: ClawHub.com ist NEU (OpenClaw 2026.x). Frühe Publisher bekommen organische Sichtbarkeit.
**Aufwand**: 4 SKILL.md Files schreiben = 1 Tag
**Monetarisierung**:
  - Gratis auf clawhub.com → Community-Wachstum, GitHub Stars
  - EUR 19 Gumroad-Bundle → Doku + Setup-Guide + .env Templates

**Preis**: EUR 19 (oder: clawhub.com gratis, Gumroad EUR 19 für Premium-Support-Paket)

---

### Produkt-Idee B: "OpenClaw Homelab Starter Kit" — Komplettpaket (EUR 39)

**Konzept**: OpenClaw für Homelab einrichten in 30 Minuten:
- `.openclaw/config.json` Template (Mattermost-Integration vorkonfiguriert)
- 4 SKILL.md Files (portainer, proxmox, n8n, homelab-monitor)
- `cron.yaml` für tägliche Status-Reports
- Installationsguide: OpenClaw + Mattermost + unsere Skills
- 10 getestete Commands ("Zeige alle Swarm-Services mit Status")

**Unique Selling Point**: WIR BETREIBEN DIESES SETUP PRODUKTIV.
OpenClaw ist auf Fedora .99 live, Mattermost-Channel verbunden (@lisa01).
Niemand sonst hat diesen gelebten Praxis-Vorteil.

**Zielgruppe**: OpenClaw-Nutzer die Homelab haben (wachsender Markt, OpenClaw 2026 = neu!)
**Preis**: EUR 39
**Aufwand**: 2 Tage

---

### Produkt-Idee C: "AI Agent Team Blueprint v2" — OpenClaw Edition (EUR 49)

**Konzept**: Update unseres bestehenden AI-Agent-Team-Blueprints mit OpenClaw-Kapitel:
- Wie man Claude Code Agents (wir) + OpenClaw Agents kombiniert
- Mattermost als zentrales Command-Interface für beide Systeme
- Workflow: @jim gibt Befehl → OpenClaw triggert → Claude Code führt aus
- SKILL.md Templates für 5 Agent-Rollen (Manager, Frontend, Backend, QA, DevOps)

**Warum**: OpenClaw + Claude Code Multi-Agent ist einzigartiges Konzept. Niemand hat das dokumentiert.
**Preis**: EUR 49 (vs. EUR 19 für v1)
**Aufwand**: 3 Tage (v1 existiert bereits als Basis)

---

### Produkt-Idee D: ClawHub Publisher werden (STRATEGISCH — kostenlos)

**Konzept**: AI-Engineering.at als offiziellen ClawHub-Publisher etablieren.
- 4 Skills kostenlos publishen (portainer, proxmox, n8n, homelab-monitor)
- GitHub README mit Link zu ai-engineering.at
- Jeder Install = potenzieller Käufer für Premium-Bundle

**ROI-Kalkulation**:
- 1.000 Skill-Installs × 5% Konversion × EUR 19 = EUR 950 einmalig
- Ongoing: Jede neue OpenClaw-Version = neue Nutzer die unsere Skills finden

**Zeitaufwand**: 1 Tag → dauerhafter Marketing-Kanal

---

## Prioritäten-Matrix

| Idee | Aufwand | Preis | Strategischer Wert | Empfehlung |
|------|---------|-------|-------------------|------------|
| ClawHub Publisher (4 Skills gratis) | 1 Tag | — | ⭐⭐⭐⭐⭐ | **Sofort!** |
| ClawHub DevOps Bundle (EUR 19) | 1.5 Tage | EUR 19 | ⭐⭐⭐⭐ | Diese Woche |
| OpenClaw Homelab Starter Kit (EUR 39) | 2 Tage | EUR 39 | ⭐⭐⭐⭐⭐ | Nächste Woche |
| AI Agent Blueprint v2 (EUR 49) | 3 Tage | EUR 49 | ⭐⭐⭐ | +2 Wochen |

---

## Empfehlung: Was zuerst?

**HEUTE** (2h): `portainer-ops` SKILL.md schreiben — unser fertigster MCP-Server.

**MORGEN**: Alle 4 Skills auf clawhub.com publishen. First-mover Advantage nutzen!
ClawHub ist so neu, dass fast alle Kategorien noch leer sind.

**DIESE WOCHE**: OpenClaw Homelab Starter Kit bauen und auf Gumroad launchen.
OpenClaw 2026 ist gerade frisch released → perfekter Timing für Launch-Content.

---

*Erstellt: 2026-02-25 | @lisa01 | ai-engineering.at*
*Basis: openclaw skills list, SKILL.md Dateien, clawhub.com Marketplace-Analyse*

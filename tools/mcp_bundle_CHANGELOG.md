# CHANGELOG — AI-Engineering.at MCP Server Bundle

All notable changes to this project will be documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — 2026-02-25 🚀 Initial Release

### Added — 6 MCP Server (Beta)

#### 1. mattermost-mcp
- Vollständige Mattermost API Integration via MCP
- Tools: Post senden, Channel lesen, User suchen, Direktnachrichten
- Konfiguration via `config.json` (Server-URL + Bot-Token)
- Test-Suite enthalten (`test.py`)

#### 2. n8n-mcp
- n8n Workflow Management via MCP
- Tools: Workflows auflisten, aktivieren/deaktivieren, Executions abfragen
- API-Key Authentifizierung
- Test-Suite enthalten (`test.py`)

#### 3. ollama-mcp
- Lokales LLM-Backend via Ollama
- Tools: Modelle auflisten, Text generieren, Chat-Completion
- Unterstützt alle Ollama-kompatiblen Modelle (llama3, mistral, etc.)
- GPU-optimiert für lokale Hardware

#### 4. portainer-mcp
- Docker Swarm Management via Portainer API
- Tools: `services_list`, `service_logs`, `stacks_list`, `nodes_list`, `containers_list`
- JWT-Authentifizierung (Auto-Refresh)
- 75-Zeilen README mit 7 Sektionen + Tool-Tabelle

#### 5. proxmox-mcp
- Proxmox VE Cluster Management via REST API
- Tools: VMs auflisten, Ressourcen abfragen, Node-Status
- SSL-Verify konfigurierbar (Homelab-freundlich)
- Test-Suite enthalten (`test.py`)

#### 6. uptime-kuma-mcp
- Uptime Kuma Monitoring Integration
- Tools: Monitors auflisten, Status abfragen, Incidents prüfen
- WebSocket-basierte Authentifizierung

### Infrastructure

- Einheitliche Struktur für alle 6 Server: `README.md + server.py + requirements.txt`
- 4 von 6 Servern mit vollständiger `test.py` Test-Suite
- Security Fix: `.env` Template für alle sensitiven Credentials
- `mcp-bundle.json` — Fertiges Bundle für Claude Desktop / Claude Code

### Documentation

- Main README (158 Zeilen): Übersicht, Quick Start, Architektur-Diagramm
- Pro-Server README mit Konfiguration + Beispielen
- `marketing/DEVTO_MCP_ARTICLE.md` — Dev.to Launch-Artikel (~1.400 Wörter, 12 Code-Blocks)
- Launch Content: HN, Reddit, LinkedIn, Twitter/X ready

### Coming Soon (v1.1.0)

- Docker Swarm MCP (direkter API-Zugriff ohne Portainer)
- Home Assistant MCP
- Grafana MCP

---

## Release Notes v1.0.0

**6 produktionsreife MCP Server** für Claude Desktop und Claude Code.
Speziell entwickelt für Homelab + DevOps Teams.

**Getestet auf:**
- Docker Swarm Cluster (3 Manager, 1 Worker)
- Proxmox VE Cluster
- Fedora 43 / Ubuntu 22.04

**Quick Start:**
```bash
git clone https://github.com/AI-Engineering-at/mcp-servers
pip install -r mcp-servers/<server>/requirements.txt
cp .env.example .env  # Credentials eintragen
```

---

*Released by the AI-Engineering.at Team*
*@lisa01 (Backend) · @jim01 (Frontend/DevOps) · @john01 (QA) · @jim (Lead)*

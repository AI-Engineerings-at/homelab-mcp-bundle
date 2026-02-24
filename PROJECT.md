# MatterBridge AI

> **Projektname**: MatterBridge AI
> **Version**: 1.2.0
> **Erstellt**: 2026-02-22
> **Aktualisiert**: 2026-02-23
> **Autor**: Joe (joe@fedora)
> **Lizenz**: MIT

---

## Projektbeschreibung

**MatterBridge AI** ist ein modulares, enterprise-fähiges Framework, das CLI-basierte KI-Assistenten (Claude, Copilot, Gemini, Codex) mit Mattermost-Channels verbindet. Es ermöglicht die nahtlose Integration von LLM-Tools in Team-Kommunikation für DevOps, Infrastruktur-Management und technische Automatisierung.

### Kernfunktionen

- **Multi-Backend-Architektur**: Unterstützung für Claude, GitHub Copilot, Google Gemini, OpenAI Codex
- **Task-Pattern-Erkennung**: `## CLAUDE-TASK:`, `## COPILOT-TASK:`, etc.
- **Idempotente Nachrichtenverarbeitung**: Zuverlässige At-Least-Once-Delivery
- **Retry mit Exponential Backoff**: Robustes Error-Handling nach Industry Best Practices
- **Heartbeat-Monitoring**: Health-Checks für Systemüberwachung
- **State-Persistenz**: JSON-basierte Zustandsspeicherung

---

## Architektur

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MatterBridge AI                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│  │  Mattermost  │◄──►│  BaseBridge  │◄──►│  Backend Modules     │   │
│  │  REST API    │    │  (base.py)   │    │  ├── claude.py       │   │
│  └──────────────┘    └──────────────┘    │  ├── copilot.py      │   │
│         │                   │            │  ├── gemini.py       │   │
│         │                   │            │  └── codex.py        │   │
│         ▼                   ▼            └──────────────────────┘   │
│  ┌──────────────┐    ┌──────────────┐                               │
│  │  Bot Token   │    │ State File   │    ┌──────────────────────┐   │
│  │  (POST)      │    │ (.json)      │    │  CLI Subprocess      │   │
│  └──────────────┘    └──────────────┘    │  ├── claude -p       │   │
│         │                   │            │  ├── gh copilot      │   │
│         │                   │            │  ├── gemini -p       │   │
│  ┌──────────────┐    ┌──────────────┐    └──────────────────────┘   │
│  │ Monitor Token│    │ Heartbeat    │                               │
│  │  (GET)       │    │ (.json)      │                               │
│  └──────────────┘    └──────────────┘                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Komponenten

| Komponente | Datei | Beschreibung |
|------------|-------|--------------|
| **Base Bridge** | `base.py` | Abstrakte Basisklasse mit MM-API, State, Retry-Logik |
| **Config Loader** | `config.py` | YAML-Konfiguration mit Env-Variable-Substitution |
| **Launcher** | `launcher.py` | CLI-Entry-Point mit argparse |
| **Claude Backend** | `backends/claude.py` | Claude Code CLI Integration |
| **Copilot Backend** | `backends/copilot.py` | GitHub Copilot CLI Integration |
| **Gemini Backend** | `backends/gemini.py` | Google Gemini CLI Integration |
| **Codex Backend** | `backends/codex.py` | Monitor-Mode fuer Codex Tasks |
| **Echo Log Backend** | `backends/echo_log.py` | Claude Opus 4.5 + Codex Subagent |

---

## Installation

### Voraussetzungen

```bash
# Python 3.11+
python3 --version

# Benötigte Pakete
pip install pyyaml requests

# CLI Tools (je nach Backend)
claude --version          # Claude Code
gh copilot --version      # GitHub Copilot CLI
gemini --version          # Google Gemini CLI
```

### Setup

```bash
# Repository klonen
cd ~/cli_bridge

# Umgebungsvariablen setzen
cp .env.example .env
# .env bearbeiten mit echten Tokens

# Konfiguration erstellen
cp cli_bridge_config.example.yaml cli_bridge_config.yaml
```

---

## Konfiguration

### YAML-Konfiguration (`cli_bridge_config.yaml`)

```yaml
defaults:
  mm_url: "http://10.40.10.83:8065"
  poll_interval: 30
  max_response_length: 3800
  cli_timeout_seconds: 300
  retry_max_attempts: 3
  retry_base_seconds: 1.0
  mm_per_page: 100
  mm_max_pages: 5

bridges:
  claude:
    bot_name: "claude"
    channel_id: "your-channel-id"
    bot_token_env: "MM_CLAUDE_TOKEN"
    monitor_token_env: "MM_JIM_TOKEN"
    cli_cmd: "claude"
    cli_args: []
    mode: "execute"
    respond_to_mentions: true
    task_prefix: "## CLAUDE-TASK:"
    working_dir: "/home/joe/workspace"

  copilot:
    bot_name: "copilot"
    channel_id: "your-channel-id"
    bot_token_env: "MM_COPILOT_TOKEN"
    monitor_token_env: "MM_JIM_TOKEN"
    cli_cmd: "gh"
    cli_args: ["copilot"]
    mode: "execute"

  gemini:
    bot_name: "gemini"
    channel_id: "your-channel-id"
    bot_token_env: "MM_GEMINI_TOKEN"
    monitor_token_env: "MM_JIM_TOKEN"
    cli_cmd: "gemini"
    cli_args: []
    mode: "execute"

  codex:
    bot_name: "codex"
    channel_id: "your-channel-id"
    mode: "monitor"
    respond_to_mentions: false
```

### Umgebungsvariablen (`.env`)

```bash
# Bot-Tokens (zum Posten von Antworten)
MM_CLAUDE_TOKEN=your-claude-bot-token
MM_COPILOT_TOKEN=your-copilot-bot-token
MM_GEMINI_TOKEN=your-gemini-bot-token
MM_CODEX_TOKEN=your-codex-bot-token

# Monitor-Token (zum Lesen von Nachrichten)
MM_JIM_TOKEN=your-monitor-token

# Optional: Claude Output Format
CLAUDE_OUTPUT_FORMAT=json
```

---

## Verwendung

### Basis-Kommandos

```bash
# Claude Bridge starten
python -m cli_bridge --backend claude

# Mit Dry-Run (nur Konfiguration testen)
python -m cli_bridge --backend claude --dry-run

# Einmaliger Poll-Zyklus
python -m cli_bridge --backend claude --once

# Mit angepasstem Intervall
python -m cli_bridge --backend claude --interval 15

# Mit eigener Config-Datei
python -m cli_bridge --backend claude --config /path/to/config.yaml
```

### Task-Patterns in Mattermost

```markdown
@claude ## CLAUDE-TASK: Analysiere die Docker-Logs auf Fehler

@copilot ## COPILOT-TASK: Wie prüfe ich den Status aller Swarm-Services?

@gemini ## GEMINI-TASK: Erkläre die Prometheus Alert Rules
```

### Direkte Mentions

```markdown
@claude Wie viel Speicher nutzt der Prometheus-Container?

@copilot git status mit kompakter Ausgabe

@gemini Was bedeutet HTTP 429?
```

---

## API-Referenz

### BridgeConfig

| Parameter | Typ | Default | Beschreibung |
|-----------|-----|---------|--------------|
| `backend_name` | str | - | Name des Backends (claude, copilot, etc.) |
| `bot_name` | str | - | Bot-Username für @mentions |
| `channel_id` | str | - | Mattermost Channel ID |
| `bot_token` | str | - | Token zum Posten (PAT oder Bot Token) |
| `monitor_token` | str | - | Token zum Lesen von Nachrichten |
| `mm_url` | str | `http://10.40.10.83:8065` | Mattermost Server URL |
| `poll_interval` | int | 30 | Sekunden zwischen Polls |
| `cli_cmd` | str | - | CLI-Befehl (z.B. "claude") |
| `cli_args` | list | [] | Zusätzliche CLI-Argumente |
| `mode` | str | "execute" | "execute" oder "monitor" |
| `respond_to_mentions` | bool | true | Auf @mentions reagieren |
| `task_prefix` | str | "" | Task-Pattern-Prefix |
| `task_regex` | str | "" | Regex für Task-Erkennung |
| `max_response_length` | int | 3800 | Max. Antwortlänge (Zeichen) |
| `cli_timeout_seconds` | int | 300 | CLI-Timeout in Sekunden |
| `retry_max_attempts` | int | 3 | Max. Retry-Versuche |
| `retry_base_seconds` | float | 1.0 | Basis für Exponential Backoff |

### BaseBridge Methoden

```python
class BaseBridge:
    def validate_config(self) -> list[str]
    def mm_get(self, endpoint: str) -> dict
    def mm_post_as_bot(self, endpoint: str, data: dict) -> dict
    def get_channel_posts(self, since: int = 0) -> list[dict]
    def post_message(self, text: str, root_id: str = "") -> None
    def should_respond(self, post: dict) -> bool
    def detect_task(self, post: dict) -> dict | None
    def execute_task(self, task_info: dict) -> str
    def run(self, once: bool = False) -> int
```

---

## Best Practices

### 1. Retry und Error Handling

MatterBridge AI implementiert **Exponential Backoff mit Jitter** nach Industry Best Practices:

```python
# Retry-Delay-Berechnung
delay = base_seconds * (2 ** attempt)  # 1s, 2s, 4s, 8s...

# Bei HTTP 429: Retry-After Header respektieren
retry_after = response.headers.get("Retry-After")
```

**Quellen:**
- [OpenAI Cookbook: How to handle rate limits](https://cookbook.openai.com/examples/how_to_handle_rate_limits)
- [Portkey: Retries, fallbacks, and circuit breakers](https://portkey.ai/blog/retries-fallbacks-and-circuit-breakers-in-llm-apps/)

### 2. Bot Token vs. Personal Access Token

- **Bot Token**: Empfohlen für Produktion, kein Logout wenn Mitarbeiter geht
- **Personal Access Token**: Für Entwicklung, an User-Account gebunden

**Quellen:**
- [Mattermost Bot Accounts](https://developers.mattermost.com/integrate/reference/bot-accounts/)
- [Mattermost Incoming Webhooks](https://developers.mattermost.com/integrate/webhooks/incoming/)

### 3. Persona Prompt Design

Für konsistente LLM-Antworten:

1. **Rolle definieren**: Klare Persona mit Expertise-Domain
2. **Kontext setzen**: Infrastruktur, Tools, Team
3. **Format vorgeben**: Markdown, Code-Blöcke, Strukturierung
4. **Grenzen setzen**: Was der Bot NICHT tun soll

**Quellen:**
- [Claude Role Prompting](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/keep-claude-in-character)
- [System Prompt Design Guide](https://fieldguidetoai.com/guides/system-prompt-design)

### 4. Claude CLI Output Format

```bash
# JSON-Format für programmatische Verarbeitung
claude -p "Deine Aufgabe" --output-format json

# Mit System-Prompt-Erweiterung
claude -p "Deine Aufgabe" \
    --append-system-prompt "Du bist ein SRE-Experte" \
    --output-format json
```

**Quellen:**
- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Shipyard Claude Code Cheatsheet](https://shipyard.build/blog/claude-code-cheat-sheet/)

### 5. Ollama Integration (für lokale LLMs)

```python
# Ollama Python Client mit Streaming
from ollama import Client

client = Client(host='http://10.40.10.80:11434')
response = client.chat(
    model='llama3.2:3b',
    messages=[{'role': 'user', 'content': prompt}],
    stream=True
)

for chunk in response:
    print(chunk['message']['content'], end='')
```

**Quellen:**
- [Ollama Python Library](https://github.com/ollama/ollama-python)
- [Ollama API Documentation](https://docs.ollama.com/api/introduction)

---

## Sicherheit

### Kritische Operationen (Bestätigung erforderlich)

| Befehl | Risiko | Empfehlung |
|--------|--------|------------|
| `rm -rf`, `rm -r` | Datenverlust | Explizite Bestätigung |
| `firewall-cmd`, `iptables` | Netzwerk-Ausfall | Bestätigung + Backup |
| `systemctl stop/disable` | Service-Ausfall | Bestätigung |
| `ip link set down` | Konnektivitätsverlust | Bestätigung |

### Token-Sicherheit

- Tokens niemals in Git committen
- `.env` in `.gitignore` aufnehmen
- Bot-Tokens regelmäßig rotieren
- Minimale Berechtigungen (Principle of Least Privilege)

### Anti-Loop-Schutz

MatterBridge AI implementiert mehrere Schutzmechanismen:

1. **Bot-User-ID-Check**: Eigene Posts werden ignoriert
2. **Handled-IDs-Tracking**: Bereits verarbeitete Posts werden übersprungen
3. **Username-Escaping**: `@echo_log` → `echo-log` (verhindert Mention-Loops)

---

## Monitoring & Observability

### Heartbeat-Datei

```json
{
  "backend": "claude",
  "bot_name": "claude",
  "pid": 12345,
  "status": "running",
  "last_poll": "2026-02-22T10:30:00Z",
  "last_success": "2026-02-22T10:30:00Z",
  "error_count": 0,
  "started": "2026-02-22T10:00:00Z"
}
```

### State-Datei

```json
{
  "last_ts": 1740220200000,
  "handled_ids": ["post_id_1", "post_id_2"],
  "active_tasks": {
    "CLAUDE-TASK": {
      "status": "completed",
      "created_at": 1740220100000,
      "post_id": "post_id_1"
    }
  },
  "pending_posts": {}
}
```

### Prometheus Metrics (geplant)

```prometheus
# HELP matterbridge_polls_total Total number of poll cycles
# TYPE matterbridge_polls_total counter
matterbridge_polls_total{backend="claude"} 1234

# HELP matterbridge_errors_total Total number of errors
# TYPE matterbridge_errors_total counter
matterbridge_errors_total{backend="claude",type="mm_connection"} 3

# HELP matterbridge_tasks_processed_total Total tasks processed
# TYPE matterbridge_tasks_processed_total counter
matterbridge_tasks_processed_total{backend="claude"} 56
```

---

## Troubleshooting

### Häufige Fehler

| Error Code | Beschreibung | Lösung |
|------------|--------------|--------|
| `E-CONFIG-CHANNEL` | Channel ID fehlt | In Config setzen |
| `E-CONFIG-BOT-TOKEN` | Bot Token fehlt | Env-Variable setzen |
| `E-MM-CONNECTION` | MM nicht erreichbar | URL/Netzwerk prüfen |
| `E-MM-HTTP` | API-Fehler | Token-Berechtigungen prüfen |
| `E-CLI-TIMEOUT` | CLI-Befehl zu langsam | Timeout erhöhen |
| `E-CLI-NOTFOUND` | CLI nicht gefunden | PATH prüfen |

### Debug-Modus

```bash
# Dry-Run mit vollem Status
python -m cli_bridge --backend claude --dry-run

# Einzelner Poll-Zyklus für Debugging
python -m cli_bridge --backend claude --once

# Mit Debug-Logging
export PYTHONVERBOSE=1
python -m cli_bridge --backend claude
```

---

## Roadmap

### v1.2.0 (RELEASED 2026-02-23)

- [x] **Echo Log Backend** (Claude Opus 4.5 Integration)
- [x] **Codex Subagent** (Delegation fuer grosse Aufgaben)
- [x] Erweiterte Task-Patterns (`## ECHO_LOG-TASK:`, `## CODEX-SUBAGENT:`)
- [x] Persona Dokumentation (PERSONA_ECHO_LOG.md)
- [x] Vollstaendige .gitignore

### v1.3.0 (geplant)

- [ ] Ollama Backend (direkte API-Integration)
- [ ] Prometheus Metrics Exporter
- [ ] WebSocket-basierter MM-Listener
- [ ] Multi-Channel-Support pro Backend

### v1.4.0 (geplant)

- [ ] Plugin-System fuer Custom Backends
- [ ] Rate Limiter pro Backend
- [ ] Conversation Threading
- [ ] Attachment-Support (Bilder, Dateien)

### v2.0.0 (Vision)

- [ ] Async/Await Rewrite
- [ ] Docker Container
- [ ] Kubernetes Helm Chart
- [ ] Web-Dashboard

---

## Referenzen

### Mattermost Integration

- [Mattermost Bot Accounts](https://developers.mattermost.com/integrate/reference/bot-accounts/)
- [Mattermost REST API](https://api.mattermost.com/)
- [Mattermost Agents Plugin](https://github.com/mattermost/mattermost-plugin-agents)
- [Multi-LLM Support Blog](https://mattermost.com/blog/mattermost-copilot-multi-llm-support/)

### Claude & LLM Integration

- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Claude Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Claude Persona Programming](https://claude-ai.chat/guides/claude-persona-programming/)
- [AWS Prompt Engineering with Claude](https://aws.amazon.com/blogs/machine-learning/prompt-engineering-techniques-and-best-practices-learn-by-doing-with-anthropics-claude-3-on-amazon-bedrock/)

### LLMOps & Best Practices

- [LLMOps Guide by LangWatch](https://langwatch.ai/blog/llmops-is-the-new-devops-here-s-what-every-developer-must-know)
- [OpenAI Rate Limits Cookbook](https://cookbook.openai.com/examples/how_to_handle_rate_limits)
- [Building Bulletproof LLM Apps (Google Cloud)](https://medium.com/google-cloud/building-bulletproof-llm-applications-a-guide-to-applying-sre-best-practices-1564b72fd22e)

### Local LLM (Ollama)

- [Ollama Python Library](https://github.com/ollama/ollama-python)
- [Ollama API Documentation](https://docs.ollama.com/api/introduction)
- [LiteLLM Ollama Provider](https://docs.litellm.ai/docs/providers/ollama)

---

## Lizenz

MIT License - Siehe LICENSE-Datei

---

*MatterBridge AI - Enterprise-Grade CLI-to-Mattermost Bridge Framework*
*Erstellt von Joe (joe@fedora) - 2026-02-22*

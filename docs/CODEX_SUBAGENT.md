# Codex Subagent - Dokumentation

> **Version**: 1.0.0
> **Stand**: 2026-02-23
> **Integration**: echo_log Backend

---

## Uebersicht

Der **Codex Subagent** ist eine Erweiterung des echo_log Backends, die grosse und komplexe Aufgaben an OpenAI's Codex CLI delegiert. Dies ermoeglicht:

- **Autonome Code-Generierung** fuer Multi-File-Projekte
- **Langlaeufer-Tasks** mit bis zu 10 Minuten Timeout
- **Full-Auto-Modus** fuer selbststaendige Ausfuehrung

---

## Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                    Echo Log Bridge                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Standard Task:                                              │
│  @echo_log ## ECHO_LOG-TASK: → Claude CLI → Antwort         │
│                                                              │
│  Codex Delegation:                                           │
│  @echo_log ## CODEX-SUBAGENT: → Codex CLI → Antwort         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Verwendung

### Task-Pattern

```markdown
@echo_log ## CODEX-SUBAGENT: [Deine komplexe Aufgabe hier]
```

### Beispiele

**Multi-File Refactoring:**
```markdown
@echo_log ## CODEX-SUBAGENT: Refaktoriere alle Python-Dateien
im cli_bridge/backends/ Verzeichnis um vollstaendige Type Hints
hinzuzufuegen und PEP 484 zu erfuellen.
```

**Codebase-Analyse:**
```markdown
@echo_log ## CODEX-SUBAGENT: Analysiere die gesamte cli_bridge
Codebasis und erstelle einen detaillierten Architektur-Report
mit UML-Diagrammen.
```

**Automatisierungs-Script:**
```markdown
@echo_log ## CODEX-SUBAGENT: Erstelle ein Bash-Script das:
1. Alle Docker Swarm Services prueft
2. Prometheus Alerts abruft
3. Einen Status-Report generiert
4. Den Report nach Mattermost sendet
```

---

## Konfiguration

### Umgebungsvariablen

| Variable | Default | Beschreibung |
|----------|---------|--------------|
| `CODEX_CLI_CMD` | `codex` | Pfad zum Codex CLI |
| `CODEX_APPROVAL_MODE` | `auto-edit` | Approval-Modus |
| `CODEX_TIMEOUT_SECONDS` | `600` | Timeout in Sekunden |

### .env Beispiel

```bash
# Codex Subagent Konfiguration
CODEX_CLI_CMD=codex
CODEX_APPROVAL_MODE=auto-edit
CODEX_TIMEOUT_SECONDS=600
```

### Approval-Modi

| Modus | Beschreibung |
|-------|--------------|
| `suggest` | Nur Vorschlaege, keine Ausfuehrung |
| `auto-edit` | Automatische Edits, fragt bei Commands |
| `full-auto` | Vollstaendig autonom |

---

## Wann Codex nutzen?

### Geeignete Aufgaben

| Kategorie | Beispiele |
|-----------|-----------|
| **Code-Generierung** | Neue Module, Klassen, Tests |
| **Refactoring** | Type Hints, Code-Modernisierung |
| **Analyse** | Codebase-Reviews, Architektur-Docs |
| **Automatisierung** | Komplexe Scripts, Pipelines |
| **Migration** | API-Upgrades, Framework-Wechsel |

### Nicht geeignet

| Kategorie | Grund |
|-----------|-------|
| **Einfache Fragen** | Overkill, nutze Standard-Task |
| **Status-Abfragen** | Besser mit Quick Commands |
| **Destruktive Ops** | Benoetigt manuelle Bestaetigung |

---

## Antwort-Format

Codex-Antworten werden mit einem Prefix markiert:

```markdown
**[Codex Subagent]**

[Generierter Code oder Analyse hier]

**Hinweise**: Task wurde an Codex delegiert
```

---

## Fehlerbehandlung

### Timeout
```
[E-CLI-TIMEOUT] CLI command timed out
```
**Loesung**: `CODEX_TIMEOUT_SECONDS` erhoehen

### CLI nicht gefunden
```
[E-CLI-NOTFOUND] CLI not found: codex
```
**Loesung**: Codex CLI installieren oder `CODEX_CLI_CMD` anpassen

### Exit-Code != 0
```
[E-CLI-EXIT] command exited with code X: [Details]
```
**Loesung**: Codex-Ausgabe analysieren, Task vereinfachen

---

## Integration mit Claude Subagenten

Der Codex Subagent ist kompatibel mit den Claude Code Subagenten:

| Claude Subagent | Codex Aequivalent |
|-----------------|-------------------|
| `network-admin` | Infrastruktur-Analyse |
| `docker-admin` | Container-Scripts |
| `documentation-writer` | Docs-Generierung |
| `aiops-specialist` | Monitoring-Automation |

### Beispiel: Kombination

```markdown
@echo_log ## CODEX-SUBAGENT: Erstelle einen neuen Claude Code
Subagenten fuer Backup-Management mit folgenden Features:
- Proxmox VM Backup Orchestrierung
- NFS/Samba Backup-Rotation
- Prometheus Metriken Export
```

---

## Sicherheitshinweise

1. **Sandbox**: Codex laeuft im Working Directory (`/home/joe/cli_bridge`)
2. **Keine Secrets**: Niemals Credentials im Task-Prompt
3. **Review**: Bei `full-auto` Modus Output sorgfaeltig pruefen
4. **Logs**: Alle Codex-Aufrufe werden geloggt

---

## Monitoring

### Heartbeat-Datei
```json
{
  "backend": "echo_log",
  "bot_name": "echo_log",
  "status": "running",
  "last_poll": "2026-02-23T10:30:00Z",
  "codex_tasks_processed": 5
}
```

### State-Datei
```json
{
  "active_tasks": {
    "CODEX-SUBAGENT": {
      "status": "completed",
      "duration_seconds": 45
    }
  }
}
```

---

*Codex Subagent - Enterprise-Grade Task Delegation*
*Erstellt: 2026-02-23*

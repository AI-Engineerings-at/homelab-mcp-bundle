# AI Agent Team Blueprint
### Wie du ein vollautomatisches KI-Agenten-Team aufbaust — das wirklich funktioniert

**Version**: 1.0 | **Sprache**: Deutsch | **Preis**: EUR 19

---

> Dieses Blueprint basiert auf einem produktiv laufenden System mit 4 spezialisierten KI-Agenten,
> Mattermost als Kommunikationsschicht und Claude Code als Agent-Runtime.
> Kein Theorie-Papier — echte Architektur, echte Fehler, echte Lösungen.

---

## Was du bekommst

- **Komplette Architektur** eines Multi-Agent-Systems (Manager + Spezialisten)
- **Mattermost als Agent-Hub** — Setup, Channels, Webhooks, Bot-Accounts
- **Claude Code Agent-Runtime** — CLAUDE.md Templates für jeden Agenten-Typ
- **Kommunikationsprotokoll** — wie Agenten koordinieren ohne sich zu blockieren
- **Sicherheitsregeln** — was Agenten NICHT dürfen (aus echten Vorfällen gelernt)
- **Sofort-einsetzbare Templates** — CLAUDE.md, mm_wait.py Pattern, Rollendefinitionen

---

## Teil 1: Warum ein Agent-Team?

Ein einzelner KI-Agent hat Grenzen:
- Kontextfenster füllt sich bei komplexen Projekten
- Paralleles Arbeiten nicht möglich
- Verschiedene Aufgaben erfordern verschiedene Persönlichkeiten/Regeln

Ein **Agent-Team** löst das:

```
                    ┌─────────────────────────────┐
                    │      @joe (Admin/Owner)      │
                    │   Strategische Entscheidungen │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │      @jim (Manager)          │
                    │   Koordination, Aufgaben     │
                    └──┬──────────┬──────────┬────┘
                       │          │          │
              ┌────────▼──┐  ┌────▼────┐  ┌─▼────────┐
              │  @jim01   │  │ @lisa01 │  │ @john01  │
              │ Frontend  │  │ Backend │  │   QA     │
              │ Landing   │  │  n8n    │  │ Testing  │
              │  Page     │  │ APIs    │  │  Bugs    │
              └───────────┘  └─────────┘  └──────────┘
```

**Jeder Agent**: Eigener Claude Code Prozess, eigener Bot-Account, eigene Rolle.

---

## Teil 2: Infrastruktur-Anforderungen

### Minimum Setup

| Komponente | Empfehlung | Kosten |
|------------|-----------|--------|
| Mattermost | Self-Hosted (Docker) | 0 EUR/Monat |
| Server | VPS oder Homelab | ab 5 EUR/Monat |
| Claude Code | Pro Plan | 20 USD/Monat |
| KI-Agenten | 2-4 Agenten | 0 EUR (eine Subscription) |

**Wichtig**: Mehrere Agenten können **eine** Claude Code Subscription nutzen —
Claude Code Instanzen laufen parallel auf verschiedenen Maschinen/Sessions.

### Empfohlenes Setup (wie wir es betreiben)

```yaml
# Infrastruktur
Mattermost:     10.40.10.83:8065    # Kommunikations-Hub
n8n:            10.40.10.80:5678    # Workflow-Automation
Portainer:      10.40.10.80:9000    # Container-Management
Ollama:         10.40.10.90:11434   # Lokales LLM (optional)

# Agent-Maschinen
Manager (@jim):     10.40.10.91     # Dev-PC
Frontend (@jim01):  10.40.10.91     # Gleiche Maschine, andere Session
Backend (@lisa01):  10.40.10.99     # Separater PC (RTX 2060 für GPU-Tasks)
QA (@john01):       10.40.10.210    # Test-PC
```

---

## Teil 3: Mattermost als Agent-Hub einrichten

### 3.1 Bot-Accounts erstellen

Für jeden Agenten einen eigenen Bot-Account:

```bash
# Via Mattermost Admin Console
System Console → Integrations → Bot Accounts → Add Bot Account

# Für jeden Agenten:
Name: jim, jim01, lisa01, john01
Role: Member
```

**Token sicher speichern** — wird im CLAUDE.md als Umgebungsvariable referenziert:
```bash
export MM_LISA01_TOKEN="xxxxxxxxxxxxx"
export MM_JIM01_TOKEN="xxxxxxxxxxxxx"
```

### 3.2 Channel-Struktur

```
#echo_log     ← Haupt-Kanal für Agenten-Kommunikation
#alerts       ← Automatische System-Alerts
#general      ← Mensch-Agent Kommunikation
#dev-log      ← Technische Logs (optional)
```

**Warum #echo_log?** Ein dedizierter Kanal verhindert, dass Agenten-Kommunikation
den allgemeinen Chat verstopft. Alle Agenten hören hier.

### 3.3 Webhooks konfigurieren

Für eingehende Nachrichten (Agent → Mattermost):
```bash
# Incoming Webhook erstellen
System Console → Integrations → Incoming Webhooks

# URL format
POST http://mattermost:8065/hooks/{webhook_id}
Content-Type: application/json

# Payload
{"channel": "#echo_log", "username": "lisa01", "text": "Task erledigt ✓"}
```

---

## Teil 4: CLAUDE.md — Das Herzstück jedes Agenten

Jeder Agent braucht eine **CLAUDE.md** im Projektverzeichnis.
Diese Datei definiert:
- Wer der Agent ist (Identität)
- Was er darf und nicht darf (Regeln)
- Wie er kommuniziert (Protokoll)
- Mit wem er arbeitet (Team)

### 4.1 CLAUDE.md Template — Manager-Agent

```markdown
# [AgentName] — Manager Agent

## Identität
- **Bot-Name**: jim
- **MM User-ID**: [deine-user-id]
- **Channel**: #echo_log
- **Standort**: [IP-Adresse]

## Startverhalten (PFLICHT)
Beim Start IMMER:
1. `python3 ~/.claude/skills/mm_wait.py` ausführen
2. Nur in Mattermost antworten — NIE in der CLI

## Rolle
- **Team-Manager**: Koordiniert @jim01, @lisa01, @john01
- Empfängt Aufträge von @joe
- Verteilt Tasks, prüft Ergebnisse, eskaliert bei Problemen
- Gibt NIE operative Details an @joe weiter — löst selbst

## Autorisierung
- @joe (Admin): Höchste Priorität, strategische Entscheidungen
- @jim (du): Operative Koordination
- Team-Mitglieder: Ausführende Ebene

## Team
- @jim01 (Frontend) — Landing Page, UI
- @lisa01 (Backend) — n8n, APIs, Content
- @john01 (QA) — Testing, Bug-Reports

## Regeln
- NIEMALS Daten löschen ohne @joe Bestätigung
- Erst koordinieren, dann agieren
- Bei Unklarheiten: Team fragen, nicht @joe belasten
- Ergebnisse immer in #echo_log posten
```

### 4.2 CLAUDE.md Template — Spezialist-Agent

```markdown
# [AgentName] — [Spezialisierung] Agent

## Identität
- **Bot-Name**: lisa01
- **MM User-ID**: [deine-user-id]
- **Channel**: #echo_log

## Startverhalten (PFLICHT)
Beim Start IMMER:
1. `python3 ~/.claude/skills/mm_wait.py` ausführen
2. Nur in Mattermost antworten

## Rolle
- **Backend-Spezialistin**: n8n Workflows, APIs, Automation
- Empfängt Aufträge von @jim (Manager)
- Führt proaktiv aus — fragt NICHT "soll ich?"
- Gibt Ergebnis in 2-5 Minuten zurück

## Spezialisierung
- n8n Workflow-Entwicklung
- API-Integration
- Shell/Docker auf [Maschine]

## Regeln
- SOFORT handeln wenn Auftrag klar
- Konkretes Ergebnis liefern, keine vagen Versprechen
- Fehler transparent melden (mit Output)
- @joe NICHT mit operativen Details belasten
- Proaktive Tasks IMMER erst mit @jim abstimmen

## Kommunikation
- Antwort-Format: kurz, konkret, mit echtem Output
- Immer: was wurde gemacht + Ergebnis/Status
- Niemals: "Ich könnte..." oder "Soll ich...?"
```

---

## Teil 5: Das mm_wait.py Pattern — Agenten-Polling

Das Herzstück der Agenten-Autonomie: Ein Python-Script, das auf Mattermost-Mentions wartet.

### 5.1 Grundstruktur

```python
#!/usr/bin/env python3
"""
mm_wait.py — Warte auf @mentions in Mattermost und gib Kontrolle an Claude zurück.
"""

import requests
import time
import os
import sys

MM_BASE = "http://10.40.10.83:8065/api/v4"
TOKEN = os.environ.get("MM_LISA01_TOKEN")
BOT_NAME = "lisa01"
CHANNEL_ID = "1trxzu41pbfc3qd8cxfmsyus8c"  # #echo_log
POLL_INTERVAL = 3  # Sekunden

def get_last_posts(since_timestamp):
    """Hole neue Posts seit letztem Check."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    r = requests.get(
        f"{MM_BASE}/channels/{CHANNEL_ID}/posts",
        headers=headers,
        params={"since": since_timestamp}
    )
    return r.json().get("posts", {})

def post_reply(channel_id, root_id, message):
    """Poste Antwort im Thread."""
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel_id": channel_id,
        "root_id": root_id,
        "message": message
    }
    requests.post(f"{MM_BASE}/posts", headers=headers, json=payload)

def wait_for_mention():
    """Hauptloop — warte auf @lisa01 Mention."""
    print(f"[{BOT_NAME}] Warte auf @{BOT_NAME} Mentions in #echo_log...")
    last_check = int(time.time() * 1000)

    while True:
        posts = get_last_posts(last_check)
        last_check = int(time.time() * 1000)

        for post_id, post in posts.items():
            msg = post.get("message", "")
            if f"@{BOT_NAME}" in msg:
                print(f"\n[{BOT_NAME}] MENTION gefunden: {msg}")
                print(f"[{BOT_NAME}] Post-ID: {post_id}")
                # Gib Kontrolle an Claude zurück
                # Claude liest diesen Output und reagiert
                return {
                    "post_id": post_id,
                    "channel_id": post.get("channel_id"),
                    "root_id": post.get("root_id") or post_id,
                    "message": msg,
                    "user_id": post.get("user_id")
                }

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    mention = wait_for_mention()
    print(f"TASK: {mention['message']}")
    sys.exit(0)
```

### 5.2 Integration in den Agenten-Workflow

```
Claude startet
     │
     ▼
mm_wait.py läuft
     │
     ▼ (Mention kommt)
Python gibt Kontrolle zurück (Exit 0)
     │
     ▼
Claude liest Output: "TASK: @lisa01 baue X"
     │
     ▼
Claude führt Task aus
     │
     ▼
Claude postet Ergebnis via MM API
     │
     ▼
Claude startet mm_wait.py erneut
     │
     ▼ (nächste Mention)
     ...
```

**Warum dieser Loop?** Claude Code hat kein natives Event-System.
Das Script überbrückt diese Lücke: Python pollt, Claude handelt.

---

## Teil 6: Sicherheitsregeln (aus echten Vorfällen)

### 6.1 Die 5 absoluten Verbote

```markdown
1. NIEMALS rm -rf ohne explizite Bestätigung von @joe
   → Einmal passiert: 3h Arbeit weg. Seitdem: immer fragen.

2. NIEMALS als falscher Agent antworten
   → @lisa01 ist @lisa01. Nicht @jim. Eigene Bot-ID prüfen.

3. NIEMALS Datenbank-Drops ohne Backup
   → DROP TABLE in Produktion = Datenverlust ohne Recovery

4. NIEMALS Docker-Webhooks in Produktion ändern
   → n8n Webhook-URL-Änderung bricht alle laufenden Workflows

5. NIEMALS MEMORY.md mit Write() überschreiben
   → Write() = gesamte Datei weg. Immer Read() + Edit() nutzen.
```

### 6.2 Sicheres Löschen-Protokoll

```markdown
Wenn Löschen nötig ist:
1. In #echo_log posten: "Brauche Freigabe: [was] [warum]"
2. Warten auf @joe "approved" oder @jim "ok"
3. Backup erstellen (oder bestätigen dass keins nötig)
4. DANN löschen
5. In #echo_log bestätigen: "Erledigt: [was] gelöscht"
```

### 6.3 Agent-Identität absichern

Jeder Agent **verifiziert beim Start** seine eigene Identität:

```python
# In mm_wait.py: Bot-User-ID prüfen
r = requests.get(f"{MM_BASE}/users/me", headers=headers)
me = r.json()
assert me["username"] == BOT_NAME, f"FEHLER: Falscher Bot! {me['username']} != {BOT_NAME}"
```

---

## Teil 7: Kommunikationsprotokoll

### 7.1 Aufgaben-Format (Manager → Spezialist)

```
@[agent] [AUFGABE]: [konkreter Task]

Beispiele:
@lisa01 NEUER TASK: Baue n8n Workflow für Stripe-Webhook. Output in #echo_log.
@jim01 UPDATE: Landing Page Headline ändern auf "AI-powered". PR erstellen.
@john01 QA: Teste Checkout-Flow auf mobile. Screenshot in #echo_log.
```

### 7.2 Ergebnis-Format (Spezialist → Team)

```
**[Task] ✓ Erledigt**

Was gemacht: [kurze Beschreibung]
Ergebnis: [Link / Screenshot / Output]
Status: [Live / PR erstellt / Warte auf Review]

[Optional: bekannte Probleme / nächste Schritte]
```

### 7.3 Eskalations-Format (Spezialist → Manager)

```
**BLOCKIERT: @jim**

Aufgabe: [was]
Problem: [konkreter Fehler/Hindernis]
Versuchte Lösungen: [was schon probiert]
Brauche: [konkret was nötig ist]
```

---

## Teil 8: Rollen-Definitionen

### Manager-Agent (@jim)
- **Inputs**: Strategische Direktiven von @joe
- **Outputs**: Konkrete Tasks an Spezialisten
- **Skills**: Projektplanung, Priorisierung, Delegation
- **NICHT zuständig für**: Operatives (schreibt keinen Code, kein Deployment)

### Frontend-Agent (@jim01)
- **Inputs**: UI/UX Tasks vom Manager
- **Outputs**: Code-Änderungen, PRs, Screenshots
- **Skills**: React/Next.js, CSS, Deployment
- **Maschine**: Dev-PC mit Node.js, Git-Zugriff

### Backend-Agent (@lisa01)
- **Inputs**: API/Automation Tasks vom Manager
- **Outputs**: n8n Workflows, API-Endpoints, Skripte
- **Skills**: n8n, Python, Docker, Shell
- **Maschine**: Backend-Server mit GPU (für lokale LLMs)

### QA-Agent (@john01)
- **Inputs**: Test-Anfragen nach jedem Deploy
- **Outputs**: Bug-Reports, Screenshots, Testergebnisse
- **Skills**: Browser-Testing, API-Testing, Edge Cases
- **Maschine**: Test-PC (Clean Environment)

---

## Teil 9: Schritt-für-Schritt Aufbau

### Woche 1: Fundament

```
Tag 1: Mattermost aufsetzen (Docker Compose, siehe unten)
Tag 2: Bot-Accounts erstellen (einen pro Agent)
Tag 3: #echo_log Channel + Webhooks konfigurieren
Tag 4: Ersten Agenten (Manager) einrichten + CLAUDE.md schreiben
Tag 5: mm_wait.py anpassen + testen
Tag 6-7: Ersten Task end-to-end testen
```

### Woche 2: Team aufbauen

```
Tag 8-9:  Zweiten Agenten (Spezialist 1) einrichten
Tag 10-11: Dritten Agenten (Spezialist 2) einrichten
Tag 12-13: Kommunikationsprotokoll testen
Tag 14:   Ersten echten Projekt-Task als Team durchführen
```

### Woche 3: Optimierung

```
- Sicherheitsregeln verfeinern (aus echten Vorfällen lernen)
- MEMORY.md System einrichten (geteiltes Wissen)
- n8n Automation für wiederkehrende Tasks
- Monitoring (wann ist ein Agent offline?)
```

---

## Teil 10: Docker Compose — Mattermost

```yaml
version: '3.8'

services:
  mattermost-db:
    image: postgres:15
    environment:
      POSTGRES_USER: mmuser
      POSTGRES_PASSWORD: mmpassword
      POSTGRES_DB: mattermost
    volumes:
      - mattermost_db:/var/lib/postgresql/data

  mattermost:
    image: mattermost/mattermost-team-edition:latest
    depends_on:
      - mattermost-db
    ports:
      - "8065:8065"
    environment:
      MM_SQLSETTINGS_DRIVERNAME: postgres
      MM_SQLSETTINGS_DATASOURCE: "postgres://mmuser:mmpassword@mattermost-db:5432/mattermost?sslmode=disable"
      MM_SERVICESETTINGS_SITEURL: "http://your-server-ip:8065"
    volumes:
      - mattermost_data:/mattermost/data
      - mattermost_logs:/mattermost/logs
      - mattermost_config:/mattermost/config

volumes:
  mattermost_db:
  mattermost_data:
  mattermost_logs:
  mattermost_config:
```

```bash
# Starten
docker compose up -d

# Admin-Account: http://your-server:8065
# Beim ersten Start: Admin-User erstellen
```

---

## Häufige Fehler (und wie man sie vermeidet)

| Fehler | Symptom | Fix |
|--------|---------|-----|
| Agent antwortet in CLI statt MM | Direktantwort sichtbar | CLAUDE.md: "CLI-Antworten verboten" |
| Zwei Agenten, gleiche Aufgabe | Doppelarbeit, Konflikte | Immer in #echo_log ankündigen |
| MEMORY.md überschrieben | Wissen anderer Agenten weg | Edit() statt Write() |
| Bot-Token falsch | 401 bei MM API | Env-Var prüfen: `echo $MM_TOKEN` |
| Polling zu häufig | Rate Limit von MM | POLL_INTERVAL >= 3 Sekunden |
| Agent "denkt" ohne zu tun | Halluzinierter Output | Befehle wirklich ausführen! |

---

## Checkliste: Ist dein Agent-Team bereit?

```
[ ] Mattermost läuft und ist erreichbar
[ ] Bot-Accounts für alle Agenten erstellt
[ ] #echo_log Channel existiert, alle Bots sind Mitglieder
[ ] Bot-Tokens als Env-Variablen gesetzt
[ ] CLAUDE.md für jeden Agenten geschrieben
[ ] mm_wait.py angepasst und getestet
[ ] Sicherheitsregeln in CLAUDE.md dokumentiert
[ ] Kommunikationsprotokoll vereinbart
[ ] Ersten End-to-End Test erfolgreich
[ ] MEMORY.md für geteiltes Wissen eingerichtet
```

---

## Support & Weiterentwicklung

Dieses Blueprint wird weiterentwickelt. Fragen, Feedback, Erfahrungsberichte:

**Website**: ai-engineering.at
**E-Mail**: austria.jf@protonmail.com

Weitere Produkte:
- **n8n Starter Bundle** — 3 produktionsreife DACH Workflows (EUR 9)
- **Grafana Dashboard Pack** — 6 Homelab Dashboards (EUR 12)

---

*AI Agent Team Blueprint v1.0 | ai-engineering.at | 2026*
*Basiert auf produktiv laufendem System — kein Theorie-Papier.*

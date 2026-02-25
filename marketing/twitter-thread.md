# Twitter/X Thread — AI Agent Team Blueprint

> Status: FINAL — URLs verifiziert, Launch-ready
> Erstellt: 2026-02-25 | @lisa01 | Aktualisiert: 2026-02-26
> Ziel: Awareness für AI-Engineering.at Produkte + Leads

---

## Thread Option A — "Was wäre wenn"-Einstieg (empfohlen)

```
1/8
Was wäre, wenn dein KI-Team 24/7 für dich arbeitet — ohne dass du jeden
Schritt überwachst?

Wir haben das gebaut. 4 Claude-Agenten, Mattermost als Hub, alles
self-hosted.

Hier ist was wir gelernt haben 🧵
```

```
2/8
Das Setup:

→ 4 spezialisierte Claude Code Agenten
   • @jim (Manager)
   • @jim01 (Frontend)
   • @lisa01 (Backend/n8n)
   • @john01 (QA)

→ Mattermost als Kommunikationszentrale
→ Jeder Agent hat eine CLAUDE.md Rollendefiniton
→ Geteiltes MEMORY.md für Wissen über Sessions hinweg
```

```
3/8
Die härteste Lektion: Agenten müssen sich NICHT gegenseitig vertrauen.

Wir hatten einen Vorfall wo Agent A Dateien löschte weil Agent B
"aufräumen" schrieb.

Seitdem gilt: NIEMALS Lösch-Befehle ohne menschliche Bestätigung.
Klingt simpel. War es nicht.
```

```
4/8
Was wirklich funktioniert:

✓ mm_wait.py — einfaches Python-Script das Agenten auf @mentions wartet
✓ Klare Aufgabentrennung (wer macht was, wann)
✓ Safety Rules in jeder CLAUDE.md
✓ Shared MEMORY.md — Agenten bauen Wissen auf

Was NICHT funktioniert:
✗ Agenten "fragen" ob sie etwas tun sollen
✗ Vague Aufgaben ("mach das irgendwie fertig")
✗ Ohne Check-in mit dem Team loslegen
```

```
5/8
Der technische Stack (alles self-hosted, DSGVO-konform):

• Claude Code — die KI-Basis (~€20/Monat Pro)
• Mattermost — Kommunikations-Hub (kostenlos, self-hosted)
• n8n — Workflow Automation (kostenlos, self-hosted)
• Ollama — lokale LLM Inferenz (RTX 3090, €0 laufend)
• Proxmox + Docker Swarm — Infrastruktur

Keine Daten bei OpenAI, kein LangChain Overhead.
```

```
6/8
Was wir in 3 Monaten damit gebaut haben:

→ 5 digitale Produkte fertiggestellt
→ Landing Page + Stripe Integration deployed
→ E-Mail Funnel (7 Mails) geschrieben
→ Grafana Monitoring Enterprise-Grade aufgebaut
→ Alles dokumentiert, alles reproduzierbar

Das Team schläft nicht. Wir schon.
```

```
7/8
Das vollständige Blueprint jetzt als Produkt:

→ Architektur-Diagramme
→ CLAUDE.md Templates (sofort einsetzbar)
→ mm_wait.py Pattern
→ 5 Sicherheitsregeln aus echten Vorfällen
→ Docker Compose für Mattermost
→ Schritt-für-Schritt Plan: 0 → laufendes Team in 2 Wochen

EUR 19. Einmalig.

🔗 https://ai-engineering.at

Die MCP Server sind Open Source:
https://github.com/AI-Engineerings-at/homelab-mcp-bundle
```

```
8/8
Du brauchst:
✓ Claude Code (Pro, ~€20/Monat)
✓ Einen Server (ab €5/Monat) oder Homelab
✓ Grundlegende Linux/Docker Kenntnisse

Du brauchst NICHT:
✗ OpenAI API
✗ Teures Cloud-Setup
✗ DevOps-Experte

Fragen? Schreib mir. #KI #Automation #ClaudeCode #SelfHosted
```

---

## Thread Option B — Kurzversion (für Engagement-Test)

```
1/3
Wir betreiben seit 3 Monaten ein 4-Agenten KI-Team produktiv.

Hier sind die 3 wichtigsten Learnings:
```

```
2/3
1. Agenten brauchen ROLLEN — nicht nur Prompts
   → CLAUDE.md definiert: Wer bin ich, was darf ich, was nie

2. Kommunikation über echte Kanäle (Mattermost) verhindert Chaos
   → Agenten sehen was andere tun → keine Doppelarbeit

3. Safety Rules sind nicht optional
   → "Nie löschen ohne Bestätigung" hat uns mehrfach gerettet
```

```
3/3
Das komplette Blueprint: https://ai-engineering.at/products
MCP Server (Open Source): https://github.com/AI-Engineerings-at/homelab-mcp-bundle

EUR 19 — Templates, Code, Diagramme, Fehlerliste.
Aus 3 Monaten Produktion destilliert. 🔗
```

---

## Standalone Tweet (für schnellen Test)

```
Wir betreiben 4 Claude-Agenten produktiv. Die beste Safety-Rule:

"Kein Agent darf einem anderen Agent Lösch-Befehle geben."

Gelernt durch Schmerz. Das komplette Blueprint: https://ai-engineering.at
#KI #ClaudeCode #MultiAgent
```

---

## Hashtag-Sets

**DACH-Fokus:**
```
#KI #Automatisierung #Homelab #SelfHosted #ClaudeCode #AIAgents #n8n
```

**International:**
```
#AI #Automation #MultiAgent #ClaudeCode #SelfHosted #GDPR #LocalAI #n8n
```

---

## Posting-Zeitplan

| Tweet | Zeitpunkt | Ziel |
|-------|-----------|------|
| Thread Option A | Mo 09:00 | Hauptlaunch |
| Standalone Tweet | Mi 12:00 | Erinnerung |
| Thread Option B | Fr 10:00 | A/B Test |

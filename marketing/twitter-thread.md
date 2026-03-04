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
Das komplette Blueprint: https://ai-engineering.at
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

---

---

# 🇬🇧 ENGLISH VERSIONS

---

## Thread Option A — "What if" hook (recommended)

```
1/8
What if your AI team worked 24/7 — without you supervising every step?

We built that. 4 Claude agents, Mattermost as the hub, fully self-hosted.

Here's what we learned 🧵
```

```
2/8
The setup:

→ 4 specialized Claude Code agents
   • @jim (Manager)
   • @jim01 (Frontend)
   • @lisa01 (Backend/n8n)
   • @john01 (QA)

→ Mattermost as the communication hub
→ Each agent has a CLAUDE.md role definition
→ Shared MEMORY.md for knowledge across sessions
```

```
3/8
The hardest lesson: agents must NOT blindly trust each other.

We had an incident where Agent A deleted files because Agent B
wrote "clean up" in a shared channel.

Since then: NEVER delete data without human confirmation.
Sounds obvious. It wasn't.
```

```
4/8
What actually works:

✓ mm_wait.py — simple Python script that lets agents listen for @mentions
✓ Clear role separation (who does what, when)
✓ Safety rules in every CLAUDE.md
✓ Shared MEMORY.md — agents build knowledge over time

What does NOT work:
✗ Agents asking "should I do this?"
✗ Vague tasks ("finish this somehow")
✗ Starting work without checking in with the team
```

```
5/8
The tech stack (all self-hosted, GDPR-compliant):

• Claude Code — the AI foundation (~€20/month Pro)
• Mattermost — communication hub (free, self-hosted)
• n8n — workflow automation (free, self-hosted)
• Ollama — local LLM inference (RTX 3090, €0 running cost)
• Proxmox + Docker Swarm — infrastructure

No data at OpenAI, no LangChain overhead.
```

```
6/8
What we shipped in 3 months with this:

→ 5 digital products completed
→ Landing page + Stripe integration deployed
→ Email funnel (7 emails) written
→ Enterprise-grade Grafana monitoring built
→ Everything documented, everything reproducible

The team doesn't sleep. We do.
```

```
7/8
The complete blueprint — now available as a product:

→ Architecture diagrams
→ CLAUDE.md templates (ready to use)
→ mm_wait.py pattern
→ 5 safety rules from real incidents
→ Docker Compose for Mattermost
→ Step-by-step: 0 → running team in 2 weeks

EUR 19. One-time.

🔗 https://ai-engineering.at

MCP Servers are Open Source:
https://github.com/AI-Engineerings-at/homelab-mcp-bundle
```

```
8/8
You need:
✓ Claude Code (Pro, ~€20/month)
✓ A server (from €5/month) or a homelab
✓ Basic Linux/Docker knowledge

You don't need:
✗ OpenAI API
✗ Expensive cloud setup
✗ A DevOps expert

Questions? DM me. #AI #Automation #ClaudeCode #SelfHosted
```

---

## Thread Option B — Short version (engagement test)

```
1/3
We've been running a 4-agent AI team in production for 3 months.

Here are the 3 most important lessons:
```

```
2/3
1. Agents need ROLES — not just prompts
   → CLAUDE.md defines: who am I, what can I do, what never

2. Communication over real channels (Mattermost) prevents chaos
   → Agents see what others are doing → no duplicate work

3. Safety rules are not optional
   → "Never delete without confirmation" saved us multiple times
```

```
3/3
The complete blueprint: https://ai-engineering.at
MCP Servers (Open Source): https://github.com/AI-Engineerings-at/homelab-mcp-bundle

EUR 19 — templates, code, diagrams, failure list.
Distilled from 3 months of production. 🔗
```

---

## Standalone Tweet (quick test)

```
We run 4 Claude agents in production. The best safety rule:

"No agent can instruct another agent to delete data."

Learned through pain. The complete blueprint: https://ai-engineering.at
#AI #ClaudeCode #MultiAgent
```

---

## Hashtag Sets

**DACH focus:**
```
#KI #Automatisierung #Homelab #SelfHosted #ClaudeCode #AIAgents #n8n
```

**International:**
```
#AI #Automation #MultiAgent #ClaudeCode #SelfHosted #GDPR #LocalAI #n8n
```

# Email 2 — Tag 3: Top 3 MCP Use Cases

**Subject**: Die 3 MCP-Anwendungen, die wirklich Zeit sparen
**From**: AI Engineering <hello@ai-engineering.at>
**To**: {{ subscriber.email }}
**Segment**: Engaged (opened Email 1) + All

---

Hey {{ subscriber.first_name | default: "du" }},

vor 3 Tagen hast du dir den MCP Starter Kit heruntergeladen.

Heute zeige ich dir die 3 Use Cases, bei denen MCP-Server in der Praxis wirklich etwas bringen — nicht in Theorie, sondern aus unserem eigenen Betrieb.

---

## Use Case #1: Docker Swarm über natürliche Sprache steuern

Statt `docker service ls && docker service ps agents_service-monitor` zu tippen:

> *"Zeig mir alle Services die nicht 1/1 laufen"*

Ein MCP-Server, der direkt die Docker API anspricht, liefert die Antwort in Sekunden — formatiert, gefiltert, mit Timestamp.

**Was du brauchst:** Portainer MCP Server (im Starter Kit enthalten), Claude Desktop

**Zeitersparnis:** ~40 Min/Woche für 5-Node Cluster

---

## Use Case #2: Prometheus Alerts automatisch erklären

Wenn `HighMemory` auf docker-swarm2 feuert, will ich nicht selbst in Grafana nachschauen:

> *"Warum hat docker-swarm2 gerade hohe Memory-Last?"*

Ein MCP-Server, der Prometheus direkt abfragt, kann die letzten 30 Minuten Memory-Trend analysieren, Top-5 Prozesse ausgeben und eine Erklärung formulieren — alles in einem Zug.

**Was du brauchst:** Prometheus MCP Server, Ollama lokal oder Anthropic API

**Zeitersparnis:** Keine Nachtschichten mehr für False-Positive Alerts

---

## Use Case #3: n8n Workflow-Dokumentation auf Knopfdruck

Du hast 17 Workflows in n8n und keine Ahnung mehr, was Workflow #12 macht?

> *"Erkläre mir Workflow 'Stripe Download Delivery' Schritt für Schritt"*

Ein MCP-Server mit n8n API-Zugriff liest den Workflow-JSON, analysiert die Nodes und erstellt eine verständliche Dokumentation — auf Deutsch, mit Risiko-Hinweisen.

**Was du brauchst:** n8n MCP Server (Custom), n8n API Key

**Zeitersparnis:** 2+ Stunden bei jedem Onboarding neuer Entwickler

---

## Was haben diese 3 gemeinsam?

Alle drei nutzen das gleiche Muster:

```
Claude (LLM) ←→ MCP Server ←→ Deine Infra
```

Kein Custom-Code. Keine komplizierte Integration. Nur ein MCP-Server, der deine vorhandene API exposed.

Das ist die Stärke des Model Context Protocol — und warum ich glaube, dass es 2025 das wichtigste Konzept in der AI-Toolchain wird.

---

**In 4 Tagen** zeige ich dir, wie unser Team seinen ersten vollständigen AI Agent in unter einem Tag deployed hat — inklusive Monitoring und DSGVO-Compliance.

Bis nächste Woche,

Joe

---

*P.S. Hast du den Starter Kit schon ausprobiert? Antworte auf diese Mail und sag mir, welcher Use Case für dich am relevantesten ist.*

---

*[Abmelden]({{ unsubscribe_url }}) | [Datenschutz](https://www.ai-engineering.at/datenschutz)*

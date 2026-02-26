---
subject: "Die 3 MCP Server, die dein Homelab wirklich braucht"
day: 3
goal: "Deliver value, show practical use cases, soft CTA to free bundle"
from: "Joe"
---

# Email 2: Die Top 3 MCP Use Cases für dein Homelab

Hallo [NAME],

Du hast das MCP Quickstart Playbook gelesen. Jetzt die Frage: Wie setzt man MCP wirklich ein?

Hier sind die **3 Use Cases**, die ich selbst täglich nutze und die dir den größten sofortigen Mehrwert bringen:

---

## Use Case 1: Portainer MCP – Deine Docker Swarm über AI steuern

**Das Problem:** Du willst mit einer Frage wie „Welche Services laufen gerade auf docker-swarm3?" antworten bekommen, ohne manuell in die CLI zu wechseln.

**Die Lösung:** Der Portainer MCP Server verbindet deine AI mit deinem Docker Swarm Cluster. Dein Agent kann jetzt live Logs abrufen, Service-Status checken und sogar Services neustarten – auf Anfrage.

**Echtes Beispiel:** Statt `ssh root@docker-swarm "docker service logs"` schreibst du nur noch dem Agent „Zeig mir die letzten 50 Logs von Grafana" und erhältst sofort die Antwort.

---

## Use Case 2: n8n MCP – Deine Workflows mit natürlicher Sprache auslösen

**Das Problem:** n8n Workflows sind mächtig, aber Nicht-Techniker können sie nicht auslösen, und selbst Techniker müssen dafür immer in die UI klicken.

**Die Lösung:** Mit dem n8n MCP Server wird jeder Workflow zu einem natürlichen Sprachbefehl. „Starten Sie den Onboarding-Workflow für [email]" und es passiert automatisch.

**Echtes Beispiel:** Marketing-Mails, Lead-Scoring, automatische Report-Generierung – alles über einen Chatbot gesteuert.

---

## Use Case 3: Monitoring MCP (Grafana + Prometheus) – Alerts verstehen, nicht nur sehen

**Das Problem:** Du bekommst einen Prometheus Alert „High CPU on pve3". Aber _warum_? Was läuft da gerade? Brauchst du handeln?

**Die Lösung:** Der Monitoring MCP gibt deinem Agent direkt Zugriff auf Prometheus Queries und Grafana Dashboards. Er kann live sehen, dass der Laster durch einen neuen Container-Spawn kam und sagt dir „Das ist normal und wird sich in 5 Minuten beruhigen".

**Echtes Beispiel:** Keine Mitternacht-Paniken mehr. Der Agent analysiert den Alert, gibt dir Kontext, schlägt Lösungen vor.

---

## Nächster Schritt: Das Homelab MCP Bundle

Alle diese MCP Server (Portainer, n8n, Monitoring, + 2 weitere) sind bereits fertig konfiguriert in unserem **kostenlosen Homelab MCP Bundle**.

Dazu gibt es:
- Komplette Installationsanleitung (docker-compose ready)
- Konfigurationsbeispiele für alle 5 MCP Server
- Integration mit Claude, Ollama, DeepSeek
- Echte Workflow-Beispiele

**Hole dir das Bundle hier:** [GUMROAD_LINK]

Keine versteckten Kosten, keine Abo – einfach öffnen, deployen, profitieren.

Bis bald,
**Joe**

P.S. Die nächste Email (in 4 Tagen) zeigt dir das komplette Playbook für einen lokalen AI-Stack mit Ollama + n8n. Das ist das Pro-Level Material.

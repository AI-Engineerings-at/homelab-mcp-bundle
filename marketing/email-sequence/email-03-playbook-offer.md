# Email 3 — Tag 7: Soft-Sell Playbook EUR 49

**Subject**: Wie wir einen AI Agent in <1 Tag in Produktion gebracht haben
**From**: AI Engineering <hello@ai-engineering.at>
**To**: {{ subscriber.email }}
**Segment**: All subscribers (day 7)

---

Hey {{ subscriber.first_name | default: "du" }},

letzte Woche habe ich dir die 3 besten MCP Use Cases gezeigt.

Heute erzähle ich dir, wie wir das alles zusammengebaut haben — und wie du dasselbe in weniger als einem Tag schaffst.

---

## Die ehrliche Geschichte

Im November letzten Jahres hatten wir ein Problem: Prometheus hat Alerts gefeuert, die Alertmanager hat sie geschluckt, und wir haben erst beim morgendlichen Check gemerkt, dass ein Service seit 6 Stunden tot war.

Die klassische Lösung: mehr Monitoring. Mehr Dashboards. Mehr Alerts.

Unsere Lösung: ein AI Agent, der Alerts in natürlicher Sprache erklärt, Kontext aus der History zieht und proaktiv in Mattermost postet — bevor wir morgens aufwachen.

Gebaut an einem Nachmittag. In Produktion seit 3 Monaten. Kein Ausfall.

---

## Die Architektur in 3 Schichten

**Schicht 1 — Detection**
Prometheus scrapt jeden Node alle 15 Sekunden. Alertmanager routet kritische Alerts an einen Webhook-Endpoint.

**Schicht 2 — Analysis**
Ein Python-Service (Service Monitor Agent) empfängt den Webhook, zieht Kontext aus Neo4j (welche Services laufen auf diesem Node? welche Dependencies?) und schickt alles an Ollama.

**Schicht 3 — Communication**
Ollama (llama3.1:8b auf GPU) formuliert eine Erklärung auf Deutsch. Der Agent postet ins Mattermost-Team.

Fertig. Kein LangChain. Kein kompliziertes Framework.

---

## Die Zahl, die mich überrascht hat

Seit Deployment haben wir **73% weniger "was ist das?"-Slack-Nachrichten** im Team.

Nicht weil wir weniger Incidents haben. Sondern weil der Agent den Kontext liefert, bevor die erste Person aufmacht.

---

## Willst du dasselbe aufbauen?

Wir haben die komplette Architektur — Prometheus Config, Alertmanager Rules, Agent-Code, n8n Workflows, Grafana Dashboards — in einem Playbook dokumentiert.

**Das AI Agent Team Playbook** (EUR 49) enthält:

- Schritt-für-Schritt Aufbau des Service Monitor Agents
- Alle Docker Compose / Swarm Files
- n8n Workflow-Templates (Import-fertig)
- DSGVO-Compliance Checklist für EU-Teams
- Troubleshooting Guide aus 3 Monaten Betrieb

**[→ Playbook ansehen — EUR 49](https://www.ai-engineering.at/#products)**

---

Kein Abo. Einmalzahlung. Lebenslanger Zugriff auf Updates.

Falls du Fragen hast bevor du kaufst, antworte einfach auf diese Mail. Ich beantworte sie persönlich.

Joe

---

*P.S. Wenn EUR 49 gerade nicht passt: Der MCP Starter Kit (kostenlos) und die Blog-Artikel auf ai-engineering.at sind ein guter Start. Kein Druck.*

---

*[Abmelden]({{ unsubscribe_url }}) | [Datenschutz](https://www.ai-engineering.at/datenschutz)*

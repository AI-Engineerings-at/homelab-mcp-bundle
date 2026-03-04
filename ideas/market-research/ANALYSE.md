# Marktanalyse — AI-Engineering.at Produkt-Chancen

> **Stand**: 2026-02-25 | Analyst: @lisa01
> **Basis**: MCP_SKILLS_RESEARCH.md, SKILL_MARKETPLACES.md, bestehende Produkt-Listings,
> Marktpreise aus Gumroad/smithery.ai/mcp.so sowie Wettbewerbsrecherche

---

## Executive Summary

Der Markt fuer DevOps-Templates und Automation-Bundles ist stark unterversorgt in der
DACH-Region und bei Self-Hosted-Loesungen. Waehrend n8n-Templates auf Gumroad typisch
zwischen EUR 9–49 liegen, fehlen hochwertige DevOps-spezifische Bundles vollstaendig.
Bei Grafana-Dashboards dominieren kostenlose Grafana.com-Submissions — wer Premium-Qualitaet
mit Doku und Setup-Scripts verkauft, hat quasi kein Wettbewerb. MCP-Server sind ein
Blueocean-Markt: fast alle sind gratis/Open-Source, wenige verkaufen Premium-Bundles.
Die groesste sofortige Chance liegt in einem **MCP DevOps Bundle** (smithery.ai + Gumroad)
und einem **n8n AI-Monitoring-Bundle** mit Prometheus-Integration — beide in 2–3 Tagen
launchbar und ohne direkte Konkurrenz in unserem Stack.

---

## Top 5 Produkt-Chancen

### 1. MCP DevOps Bundle — "Claude Code fuer Ops-Teams"

- **Markt-Gap**: Auf smithery.ai, mcp.so und glama.ai gibt es hunderte MCP-Server —
  aber KEIN kuratiertes, getestetes Bundle fuer DevOps/Homelab mit Prometheus, Grafana,
  Docker Swarm und n8n in einem Paket. Alle verfuegbaren Bundles sind entweder nur
  fuer Entwickler (GitHub/Jira) oder nur einzelne Server, nie ein komplettes Ops-Stack.
- **Zielgruppe**: DevOps-Engineers, SREs, Homelab-Betreiber mit Claude Code Pro-Abo.
  Niche: ~50.000 aktive Claude Code Nutzer, davon ~5–10% technisch genug fuer MCP.
- **Preis**: EUR 39 — basierend auf Marktvergleich: einzelne MCP-Server auf mcpmarket.com
  kosten 0–15 USD, Bundles (5+ Server) mit Doku fehlen fast vollstaendig.
- **Aufwand**: 2–3 Tage bis Launch (wir haben bereits Grafana + Portainer MCP live!)
- **Bestandteile**:
  - Vorkonfigurierte .mcp.json fuer unseren Stack (Grafana, Neo4j, Docker, GitHub)
  - SKILL.md Templates: docker-swarm-ops, n8n-workflows, prometheus-monitoring
  - Hook-Konfiguration (PreToolUse: main-Branch-Schutz, PostToolUse: Auto-Lint)
  - Installationsguide fuer alle 4 MCP-Server
  - 10 getestete Prompts ("Ask Claude: Zeige alle Swarm-Services mit Status")
- **Begruendung**: Wir betreiben diesen Stack produktiv — niemand sonst hat diesen
  gelebten Praxis-Vorteil. Differenzierung durch echte Q&A-Paare und Troubleshooting.

---

### 2. n8n AI-Monitoring-Bundle — "Prometheus trifft Automation"

- **Markt-Gap**: n8n-Templates auf Gumroad und n8n.io/workflows zeigen: die meistgekauften
  Templates sind CRM/Sales-Automation (HubSpot, Pipedrive) und Social-Media-Automation.
  DevOps/Monitoring-Workflows (Prometheus Alerting, Grafana, Docker Healthchecks) fehlen
  fast vollstaendig. Der n8n-Template-Marktplatz (n8n.io/workflows) hat ~2.000 Community-
  Templates, davon unter 30 mit "monitoring" oder "prometheus" Tag — und KEINES kombiniert
  Prometheus Alertmanager + Mattermost/Slack + automatische Incident-Tickets.
- **Zielgruppe**: IT-Admins, DevOps-Engineers, KMU-IT die n8n bereits betreiben und
  ihr Monitoring automatisieren wollen. Schmerz: Alert-Fatigue, manuelle Ticket-Erstellung.
- **Preis**: EUR 29 — unsere bestehende n8n-Bundle ist EUR 19 (3 allgemeine Workflows),
  dieses Bundle ist spezialisierter und wertvoller fuer die Zielgruppe.
- **Aufwand**: 2 Tage (Workflows bereits in Produktion auf unserem Stack!)
- **Bestandteile** (5 Workflows):
  - Prometheus Alert → Mattermost-Benachrichtigung mit Kontext (bereits live als AIOps v4.1)
  - Alertmanager Webhook → automatische Incident-Ticket-Erstellung (n8n intern)
  - Docker Service Health → taeglich um 08:00 Status-Report
  - Uptime Kuma → Eskalation bei >5min Downtime an zweite Kontaktperson
  - Weekly Capacity Report: CPU/RAM/Disk-Trends aus Prometheus
- **Begruendung**: Unser AIOps-System v4.1 ist genau das. Wir verkaufen die extrahierten,
  documentierten Workflows aus unserem produktiven System.

---

### 3. Claude Code Starter Kit fuer Teams — "Von 0 auf Agent-Team in 1 Tag"

- **Markt-Gap**: Das AI-Agent-Team-Blueprint (EUR 19) zeigt die Architektur. Was fehlt:
  ein plug-and-play Starter Kit mit allen Dateien sofort kopierbar. Auf GitHub gibt es
  claude-code-showcase (ChrisWiles) als Referenz, aber kein kommerzielles "alles inklusive"
  Paket fuer deutschsprachige Teams. Kein einziger Anbieter auf Gumroad verkauft
  fertige CLAUDE.md-Templates-Pakete fuer Multi-Agent-Setups.
- **Zielgruppe**: Entwickler-Teams (2–5 Personen) die Claude Code Pro nutzen und ein
  strukturiertes Workflow-System aufbauen wollen. Budget: typisch EUR 20–50 fuer Templates.
- **Preis**: EUR 49 — hoeher als Blueprint (EUR 19) weil direkt nutzbare Dateien,
  nicht nur Doku. Vergleich: aehnliche GitHub-Action-Templates auf Gumroad EUR 25–79.
- **Aufwand**: 3 Tage
- **Bestandteile**:
  - CLAUDE.md Templates fuer 5 Rollen (Manager, Frontend, Backend, QA, DevOps)
  - .mcp.json Basiskonfiguration mit 4 empfohlenen Servern
  - .claude/settings.json mit PreToolUse/PostToolUse Hooks (main-Branch-Schutz, Auto-Lint)
  - 3 SKILL.md Files (docker-swarm-ops, n8n-workflows, prometheus-monitoring)
  - 3 Slash Commands (/deploy, /pr-review, /incident)
  - mm_wait.py Pattern fuer Mattermost-Integration
  - Onboarding-Checklist: Ist dein Team bereit?
- **Begruendung**: Wir betreiben genau dieses Setup. Exklusives Know-how das echte
  Vorfaelle und Learnings einschliesst (MEMORY.md-Fehler, falsche Agent-Identitaet, etc.).

---

### 4. Prometheus + Grafana Alert-Rules Pack — "Alert-Fatigue beenden"

- **Markt-Gap**: Auf Grafana.com/dashboards gibt es ~7.000 kostenlose Dashboards.
  Aber: kaum jemand verkauft KURATIERTE Alert-Rules (YAML) + Dashboard-Kombinationen
  fuer spezifische Use Cases (Homelab, Docker Swarm, KMU). Kostenlose Dashboards haben
  oft keine Alert-Rules dabei, keine Doku, keine Threshold-Erklaerungen.
  Auf Gumroad: 0 Treffer fuer "prometheus alert rules" (Stand Research).
- **Zielgruppe**: Ops-Teams, SREs, Homelab-Betreiber mit Prometheus. Schmerz: Stunden
  damit verbracht Alert-Thresholds zu tunen, trotzdem zu viele False Positives.
- **Preis**: EUR 19 — guenstiger Einstieg, Cross-Sell zum Grafana Dashboard Pack (EUR 29).
  Bundle beider Produkte: EUR 39.
- **Aufwand**: 1–2 Tage (Alert-Rules aus unserem Stack bereits produktiv getestet!)
- **Bestandteile**:
  - 6 produktionsgetestete Prometheus Alert-Rules (TargetDown, HighCPU, HighMemory,
    DiskSpaceLow/Critical, HighNetworkTraffic) — unsere aktuellen Regeln, gereinigt
  - Erklaerung jedes Thresholds (Warum 85% CPU? Warum 2h Pending?)
  - Alertmanager-Konfiguration fuer Mattermost + E-Mail
  - "Tuning Guide" — wie man False Positives reduziert
  - Docker Compose Snippet fuer schnelles Alert-Testing
- **Begruendung**: Wir haben diese Regeln durch echte Incidents getestet und optimiert.
  Der TargetDown-Alert zum Beispiel brauchte 3 Iterationen bis die Thresholds stimmten.

---

### 5. Homelab Security Audit Bundle — n8n + Grafana + Doku

- **Markt-Gap**: Security-Templates fuer Homelab sind extrem rar. Wer sucht nach
  "firewall audit automation n8n" oder "security dashboard grafana homelab" findet
  fast nichts Kommerzielles. OPNsense + Grafana-Integrationen existieren als gratis
  Community-Scripts, aber kein kuratiertes, dokumentiertes Bundle fuer DACH.
- **Zielgruppe**: Homelab-Betreiber mit OPNsense/pfSense, KMU-IT-Admins, Personen die
  DSGVO-konformes Logging betreiben muessen. Bereitschaft zu zahlen: EUR 19–39.
- **Preis**: EUR 29
- **Aufwand**: 4–5 Tage (neues Produkt, aber viele Bausteine vorhanden)
- **Bestandteile**:
  - Grafana Dashboard fuer OPNsense/pfSense (Suricata-Alerts, Firewall-Logs)
  - n8n Workflow: Taeglicher Security-Report (offene Ports, fehlgeschlagene Logins)
  - n8n Workflow: Automatische Benachrichtigung bei unbekannten Geraeten im Netz
  - Prometheus-Regeln fuer Netzwerk-Anomalien
  - DSGVO-Checkliste fuer Netzwerk-Logging
- **Begruendung**: OPNsense laeuft bei uns produktiv (10.40.10.1). Einzigartiger Ansatz
  kombiniert Security + Compliance fuer DACH-Markt.

---

## Preisvergleich nach Kategorie

| Kategorie | Markt-Preis (avg) | Unser Preis | Begruendung |
|-----------|-------------------|-------------|-------------|
| n8n Workflows (allgemein) | EUR 9–19 | EUR 19 | Standard-Marktpreis, DSGVO-Bonus |
| n8n Workflows (DevOps/Monitoring) | EUR 0 (kein Angebot!) | EUR 29 | Kein Wettbewerb, Spezialnische |
| Grafana Dashboards (einfach) | EUR 0 (gratis Grafana.com) | n/a | Nicht konkurrieren |
| Grafana Dashboards (Premium-Bundle) | EUR 15–39 (Gumroad rare) | EUR 29 | Qualitaetspositionierung |
| Grafana + Alert-Rules Bundle | EUR 0–15 | EUR 39 (Bundle) | Einziges Angebot mit Doku |
| MCP Server (einzeln) | EUR 0 (fast alle gratis) | n/a | Einzeln nicht sinnvoll |
| MCP Bundle (kuratiert, DevOps) | Nicht existent | EUR 39 | Blue Ocean |
| Claude Code Templates/Blueprints | EUR 10–49 | EUR 19–49 | Wettbewerbsfaehig |
| Security/Audit Templates | EUR 0–25 (Luecke!) | EUR 29 | Luecke im DACH-Markt |

---

## Quick Wins — Diese Woche launchbar

### Quick Win 1: Prometheus Alert-Rules Pack (EUR 19)

**Beschreibung**: Unsere 6 produktionsgetesteten Prometheus Alert-Rules als YAML-Dateien
mit vollstaendiger Doku, Alertmanager-Config fuer Mattermost und einem Tuning-Guide.

**Warum schnell machbar**:
- Alert-Rules laufen bereits produktiv in unserem Stack (TargetDown, HighCPU, etc.)
- Nur Bereinigung, Kommentierung und Verpackung als ZIP noetig
- Kein neuer Code — reine Extraktion und Dokumentation
- Launchzeit: 1 Tag Arbeit

**Erwarteter Umsatz**:
- Zielgruppe: Prometheus-Nutzer (Millionen weltweit, DACH-Fokus ~50.000 aktive)
- Konversion: 5–10 Kaeufer/Monat realistisch bei EUR 19 = EUR 95–190/Monat passiv
- Cross-Sell: 30% kaufen zusaetzlich Grafana Dashboard Pack (+EUR 29) = EUR 124–247/Monat total

**Naechste Schritte**:
1. `~/.claude/` Alert-Rules extrahieren und bereinigen
2. Alertmanager-Beispielkonfig fuer Mattermost + E-Mail schreiben
3. Tuning-Guide Markdown erstellen (1 Seite)
4. Gumroad-Listing mit Cover-Image
5. Launch-Post in r/homelab und r/selfhosted

---

### Quick Win 2: MCP DevOps Starter Kit (EUR 39)

**Beschreibung**: Plug-and-play .mcp.json + SKILL.md Bundle fuer Claude Code DevOps-Teams.
Einmalige Konfiguration, sofort Grafana/Docker/n8n aus Claude Code bedienbar.

**Warum schnell machbar**:
- .mcp.json fuer unseren Stack existiert bereits (Grafana, Portainer MCPs live!)
- SKILL.md Templates fuer docker-swarm-ops und n8n-workflows: 1–2h Schreibarbeit
- Hook-Konfigurationen aus MCP_SKILLS_RESEARCH.md direkt uebertragbar
- Testbare Q&A-Paare aus echtem Betrieb generierbar
- Launchzeit: 2 Tage

**Erwarteter Umsatz**:
- Kleines aber zahlungskraeftiges Segment: Claude Code Pro-Nutzer (~200.000 weltweit)
- Zielgruppe DevOps-Anteil: ~10% = 20.000
- Konversion bei EUR 39: 3–8 Kaeufer/Monat = EUR 117–312/Monat
- Wachstumspotenzial: Claude Code waechst stark, frueher Markteintritt wichtig

**Naechste Schritte**:
1. .mcp.json finalisieren (Grafana + GitHub + Memory + Neo4j)
2. 3 SKILL.md Files schreiben (docker-swarm, n8n, prometheus)
3. 3 Hook-Konfigurationen als settings.json vorbereiten
4. README mit "Erste 30 Minuten"-Guide schreiben
5. Smithery.ai Eintrag erstellen (kostenlose Sichtbarkeit!)

---

### Quick Win 3: n8n AIOps Monitoring Bundle (EUR 29)

**Beschreibung**: 5 produktionsgetestete n8n Workflows fuer DevOps-Monitoring —
extrahiert aus unserem laufenden AIOps v4.1-System. Prometheus + Alertmanager +
Mattermost/Slack-Integration, taeglich automatische Reports.

**Warum schnell machbar**:
- ALLE 5 Workflows laufen bereits produktiv in unserem n8n (10.40.10.80:5678)
- n8n-Export per API in wenigen Minuten moeglich
- Bereinigung (Credentials entfernen, Webhook-Pfade generisch machen): 2–3h
- Doku aus unserem laufenden Betrieb schreibbar: halbem Tag
- Launchzeit: 2 Tage

**Erwarteter Umsatz**:
- Ueberschneidung mit Grafana-Kaeuferschaft (Cross-Sell!)
- Standalone: 5–10 Kaeufer/Monat bei EUR 29 = EUR 145–290/Monat
- Bundle mit Grafana Pack (EUR 49 statt EUR 58): erhoehte Konversion
- Langfristig: Community-Wachstum n8n (1M+ Installs) = skalierender Absatzkanal

**Naechste Schritte**:
1. Alle 5 AIOps-Workflows aus n8n exportieren (API: `~/.claude/.n8n-api-key`)
2. Credentials durch Platzhalter ersetzen, Webhook-Pfade generisch
3. README mit Architektur-Diagramm (Mermaid) und Installationsguide
4. Gumroad-Listing mit erklaerenden Screenshots
5. n8n Community Forum-Post: "My production AIOps monitoring setup"

---

## Wettbewerbsanalyse

### n8n Templates Markt (Gumroad + n8n.io)

**Meistverkaufte Kategorien** (nach Recherche):
- Social Media Automation (Instagram, LinkedIn, Twitter): EUR 9–29
- CRM/Lead-Automation (HubSpot, Pipedrive, Salesforce): EUR 19–49
- E-Commerce-Automation (Shopify, WooCommerce): EUR 14–39
- AI-Content-Generation (ChatGPT-basiert): EUR 12–25
- **DevOps/Monitoring**: Fast nicht vorhanden → UNSERE CHANCE

**Preisrange**: EUR 9 (einfache 1-Step-Workflows) bis EUR 79 (komplexe Multi-System-Bundles)
Sweetspot: EUR 19–29 fuer 3–7-Step-Workflows mit Doku

**Luecken**:
- Prometheus/Grafana-Integration: 0 kommerzielle Angebote gefunden
- Docker Swarm Management-Workflows: 0
- DSGVO-konformes Monitoring fuer DACH: 0
- Mattermost-Integration (statt nur Slack): 0 Wettbewerb

### Grafana Dashboard Markt

**Paid vs. Free**:
- Grafana.com/dashboards: ~7.000 kostenlose Community-Dashboards
- Kommerziell auf Gumroad: sehr wenige Angebote, weniger als 20 gefunden
- Preisspanne kommerziell: EUR 0 (Pay-what-you-want) bis EUR 49 fuer spezialisierte Bundles

**Unterversorgte Kategorien**:
- Homelab-spezifische Dashboards (Proxmox + Docker Swarm + NAS): fast keine
- OPNsense/pfSense Netzwerk-Monitoring: nur Community-Scripts, keine kommerzielle Loesung
- Multi-Cluster Docker Swarm: wenige qualitativ hochwertige Optionen
- AI/LLM-Monitoring (Ollama Latenz, Request-Rate): quasi nicht existent

**Unser Vorteil**: Grafana Dashboard Pack (EUR 29) mit Import-Script und Doku ist
bereits besser als 95% der kostenlosen Alternativen. Preis-Leistung unschlagbar.

### Notion Templates Markt

**Kategorien** (nach Marktrecherche):
- Produktivitaet/GTD-Systeme: EUR 9–49 (grosser, gesaettigter Markt)
- Team-Wikis/SOPs: EUR 19–79 (mittelgross)
- Content-Kalender: EUR 7–25 (sehr gesaettigt)
- Freelancer/Agentur-Templates: EUR 14–49 (wettbewerbsfaehig)
- **DevOps/Infrastruktur-Doku**: fast nicht vorhanden!

**Chance fuer AI-Engineering.at**:
- "Infrastructure as Notion" — Homelab-Dokumentations-Template mit AI-Engineering.at-Branding
- Zielgruppe: Homelab-Betreiber die ihre Infrastruktur dokumentieren wollen
- Preis: EUR 14–19 (Einstiegsprodukt, Lead-Magnet fuer andere Produkte)
- Enthaelt: Geraete-Inventory, Service-Uebersicht, Incident-Log, Change-Management
- Aufwand: 2 Tage (Notion-Templates sind schnell erstellt)

### MCP Server Markt

**Aktuelle Situation**:
- ~90% aller MCP-Server sind Open Source und kostenlos (GitHub)
- Kommerzielle MCP-Server: kaum vorhanden (Stand 2026-02)
- Smithery.ai, mcp.so, glama.ai: reine Verzeichnisse, kein Bezahlmodell etabliert
- mcpmarket.com: fruehes Stadium, noch kein relevanter Umsatz erkennbar

**Fehlende MCPs fuer DevOps** (basierend auf MCP_SKILLS_RESEARCH.md):
- Portainer-spezifischer MCP (wir haben bereits einen Beta-Server mit 5 Tools!)
- OPNsense/pfSense MCP: Firewall-Regeln abfragen, Netzwerk-Status
- Proxmox MCP: VMs/Containers steuern, Ressourcen abfragen
- AdGuard Home MCP: DNS-Regeln, Query-Logs aus Claude abfragen
- Uptime Kuma MCP: Monitor-Status, Incident-History

**Wertvollste MCPs fuer DevOps** (nach Einsatz-Potenzial):
1. Grafana MCP (bereits Open Source von Grafana Inc.) — installieren, nicht selbst bauen
2. Portainer MCP (wir haben Beta!) — finalisieren und vermarkten
3. Proxmox MCP — waere unique, hoher Wert fuer Homelab-Community
4. Prometheus/Alertmanager MCP — direkte Alerts aus Claude abfragen

**Empfehlung**: MCP-Server nicht einzeln verkaufen (zu wenig Zahlungsbereitschaft),
sondern als Teil von Bundles (MCP DevOps Bundle, EUR 39) oder Open Source veroeffentlichen
fuer Community-Wachstum und dann durch Premium-Support/Doku monetarisieren.

---

## Produkt-Roadmap (Priorisiert)

| Woche | Produkt | Preis | Aufwand | Erwarteter MRR |
|-------|---------|-------|---------|----------------|
| Diese Woche | Alert-Rules Pack | EUR 19 | 1 Tag | EUR 95–190 |
| Diese Woche | n8n AIOps Bundle | EUR 29 | 2 Tage | EUR 145–290 |
| Naechste Woche | MCP DevOps Starter Kit | EUR 39 | 2–3 Tage | EUR 117–312 |
| Naechste Woche | Notion Homelab-Doku | EUR 14 | 2 Tage | EUR 70–140 |
| +2 Wochen | Claude Code Starter Kit | EUR 49 | 3 Tage | EUR 147–392 |
| +3 Wochen | Security Audit Bundle | EUR 29 | 4–5 Tage | EUR 87–232 |

**Kumulierter MRR-Forecast (Monat 3)**: EUR 661–1.556

---

## Fazit & Empfehlung

**Was zuerst bauen?**

**Prioritaet 1 (morgen starten)**: n8n AIOps Monitoring Bundle (EUR 29)
- Laeuft bereits produktiv → minimaler Aufwand, maximaler Wert
- Einzigartiges Angebot: kein einziger Wettbewerber in dieser Nische
- Cross-Sell-Synergie mit Grafana Dashboard Pack (EUR 29) → Bundle EUR 49

**Prioritaet 2 (Tag 2-3)**: Prometheus Alert-Rules Pack (EUR 19)
- 1 Tag Arbeit fuer passiven Einkommens-Stream
- Perfekter Einstieg fuer Kunden die dann Grafana Pack kaufen

**Prioritaet 3 (naechste Woche)**: MCP DevOps Starter Kit (EUR 39)
- Blueocean-Markt, kein Wettbewerb
- Wachsender Markt: Claude Code Nutzerzahlen steigen stark
- Smithery.ai-Listing gibt kostenlose organische Reichweite

**Langfristige Strategie**:
DevOps/Homelab-Nische konsequent besitzen. Kein Konkurrent kombiniert:
1. Echte Produktionserfahrung (wir betreiben unseren Stack 24/7)
2. DSGVO/DACH-Fokus (grosse Luecke bei US-Anbietern)
3. Self-Hosted-First-Ansatz (kein Cloud-Lock-in)
4. Vollstaendige Stack-Integration (n8n + Grafana + Prometheus + MCP + Claude Code)

Wer zuerst diese Nische besetzt, kann sie langfristig dominieren.

---

*Erstellt: 2026-02-25 | @lisa01 | ai-engineering.at*
*Grundlage: MCP_SKILLS_RESEARCH.md, SKILL_MARKETPLACES.md, bestehende Produkt-Listings,
Marktpreisrecherche Gumroad/smithery.ai/mcp.so/n8n.io*

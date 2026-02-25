# Gumroad Listing — Grafana Dashboard Pack

## Produkt-Details

| Feld | Wert |
|------|------|
| **Titel (DE)** | Grafana Dashboard Pack — 6 DACH Homelab & DevOps Dashboards |
| **Titel (EN)** | Grafana Dashboard Pack — 6 Production-Ready Monitoring Dashboards |
| **Preis** | EUR 29 |
| **Kategorie** | Templates & Tools / Monitoring |
| **Tags** | grafana, prometheus, homelab, devops, monitoring, docker, node-exporter, DSGVO |

---

## Listing-Text (Deutsch)

### Headline
**6 produktionsreife Grafana Dashboards — sofort einsatzbereit für Homelab & KMU**

### Beschreibung

Stundenlang Grafana Dashboards konfigurieren? Nicht mehr.

Dieses Pack enthält **6 sofort importierbare JSON-Dashboards** — battle-tested in einem echten Docker Swarm Cluster mit Prometheus, Node Exporter und cAdvisor.

---

**Dashboard 1: Infrastructure Overview**
Der perfekte Einstieg — alles auf einen Blick.
- CPU, RAM, Disk aller Nodes simultan
- Uptime-Indikatoren, kritische Schwellenwerte voreingestellt
- Für: Server, VMs, Bare-Metal

**Dashboard 2: Docker Swarm Cluster**
Container-Infrastruktur professionell monitoren.
- Services, Tasks, Replicas in Echtzeit
- Stack-Übersichten, Container-Status
- Für: Docker Swarm, Container-Hosts

**Dashboard 3: Node Exporter Full**
Deep-Dive in System-Metriken.
- Detaillierte CPU-Auslastung per Core
- Memory-Breakdown, Swap, Buffers/Cache
- Disk I/O, Netzwerk-Throughput
- Für: Performance-Analyse, Kapazitätsplanung

**Dashboard 4: Network Overview**
Netzwerk-Traffic im Griff.
- Bandwidth per Interface, Pakete/s
- Fehler-Raten, Kollisionen
- Für: Router, Firewalls, Switches mit SNMP

**Dashboard 5: Services Status**
Alle HTTP-Endpoints auf einen Blick.
- Uptime-Übersicht für alle Services
- Response-Time Trends
- Für: Webserver, APIs, interne Services

**Dashboard 6: Alerts Overview**
Alerts professionell verwalten.
- Aktive Prometheus Alerts gesammelt
- Alert-History und Häufigkeit
- Für: On-Call Teams, SRE, Operations

---

### Was du bekommst
- ✅ 6 JSON-Dateien — sofort in Grafana importierbar
- ✅ Detaillierte Install Guide (Markdown, DE)
- ✅ Import-Script (Bash) für alle 6 Dashboards via API
- ✅ Voraussetzungen: Grafana >= 9.0, Prometheus + Node Exporter
- ✅ Optional: cAdvisor für Docker-Metriken

### Für wen ist das?
- **Homelab-Betreiber**: Proxmox, Docker, Synology, Pi
- **KMU IT-Admins**: Monitoring ohne Enterprise-Kosten
- **DevOps Engineers**: Schneller Einstieg, dann selbst anpassen
- **DSGVO-Bewusste**: 100% lokal, keine Cloud-Abhängigkeit

---

## Listing-Text (Englisch)

### Headline
**6 Production-Ready Grafana Dashboards — Import & Monitor in Minutes**

### Beschreibung

Stop spending hours configuring Grafana dashboards from scratch.

This pack includes **6 battle-tested JSON dashboards** — running in production on a real Docker Swarm cluster with Prometheus, Node Exporter, and cAdvisor.

**Included:**
- Infrastructure Overview (CPU/RAM/Disk all nodes)
- Docker Swarm Cluster (Services, Tasks, Replicas)
- Node Exporter Full (Deep system metrics)
- Network Overview (Traffic, errors, bandwidth)
- Services Status (HTTP endpoints, uptime)
- Alerts Overview (Active Prometheus alerts)

**You get:**
- ✅ 6 JSON files — import directly into Grafana
- ✅ Install guide with bash import script
- ✅ Requirements: Grafana >= 9.0, Prometheus + Node Exporter

---

## Preispositionierung

| Produkt | Preis | Begründung |
|---------|-------|------------|
| n8n Starter Bundle | EUR 19 | 3 Workflows — Einstiegspreis |
| **Grafana Dashboard Pack** | **EUR 29** | 6 Dashboards — mehr Inhalt, DevOps-Zielgruppe zahlt mehr |
| Bundle (beides) | EUR 39 | ~EUR 9 Rabatt |

---

## Gumroad Setup Checkliste

- [ ] Produkt erstellen auf Gumroad
- [ ] ZIP-Datei erstellen: `grafana-dashboard-pack-v1.zip`
  - 6 JSON-Dateien
  - `INSTALL_GUIDE.md`
  - `README.md`
  - `import-all.sh` (Bash-Script)
- [ ] Cover-Bild erstellen (1280x720px)
- [ ] Preis: EUR 29 setzen
- [ ] Kategorien: Templates, Tools, Monitoring
- [ ] Tags setzen
- [ ] Stripe Webhook verknüpfen (http://10.40.10.80:5678/webhook/stripe-payment-completed)
- [ ] Test-Kauf durchführen

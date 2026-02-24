# Grafana Dashboard Pack — DACH Homelab Monitoring

**6 produktionsreife Dashboards | Sofort importierbar | Docker Swarm & Node Exporter ready**

---

## Enthaltene Dashboards

| # | Dashboard | Datei | Beschreibung |
|---|-----------|-------|--------------|
| 1 | Infrastructure Overview | `01_infrastructure-overview.json` | CPU, RAM, Disk aller Nodes |
| 2 | Docker Swarm Cluster | `02_docker-swarm-cluster.json` | Services, Tasks, Replicas |
| 3 | Node Exporter Full | `03_node-exporter-full.json` | Detaillierte System-Metriken |
| 4 | Network Overview | `04_network-overview.json` | Traffic, Pakete, Fehler |
| 5 | Services Status | `05_services-status.json` | HTTP-Endpoints, Uptime |
| 6 | Alerts Overview | `06_alerts-overview.json` | Aktive Alerts, History |

---

## Installation

### Voraussetzungen
- Grafana >= 9.0
- Prometheus mit Node Exporter
- (Optional) cAdvisor für Docker-Metriken

### Import
1. Grafana → Dashboards → Import
2. JSON-Datei hochladen oder Inhalt einfügen
3. Datasource auf dein Prometheus zeigen
4. Importieren

### Anpassung
- Alle Dashboards nutzen `${datasource}` Variable → automatische Datasource-Erkennung
- Variablen anpassen unter Dashboard Settings → Variables

---

## Screenshot-Preview

Die Dashboards sind optimiert für:
- **1920x1080** (Desktop)
- **Dark Mode** (Grafana default)
- **5-Minuten Refresh**

---

## Support

Bei Fragen: Öffne ein Issue oder schreibe uns auf Discord.

---

*Erstellt von AI-Engineerings | DACH-optimiert | Getestet auf Grafana 10.x | 2026*

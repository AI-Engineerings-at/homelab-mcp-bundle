# Install Guide — Grafana Dashboard Pack

## Voraussetzungen

| Komponente | Mindestversion | Zweck |
|------------|----------------|-------|
| Grafana | >= 9.0 | Dashboard-Server |
| Prometheus | >= 2.30 | Metriken-Backend |
| Node Exporter | >= 1.3 | System-Metriken (CPU, RAM, Disk) |
| cAdvisor | >= 0.47 | Docker-Metriken (optional) |

---

## Schritt 1 — Prometheus Datasource prüfen

1. Grafana öffnen → **Configuration → Data Sources**
2. Prometheus-Datasource vorhanden? → weiter mit Schritt 2
3. Falls nicht: **Add data source → Prometheus**
   - URL: `http://localhost:9090` (oder deine Prometheus-URL)
   - **Save & Test** → "Data source is working"

---

## Schritt 2 — Dashboards importieren

### Methode A: Einzelner Import (empfohlen)

1. Grafana → **Dashboards → Import**
2. **Upload JSON file** klicken
3. Gewünschte Datei auswählen (z.B. `01_infrastructure-overview.json`)
4. **Datasource** auf dein Prometheus setzen
5. **Import** klicken

### Methode B: Alle 6 Dashboards auf einmal (via API)

```bash
# Grafana URL und Credentials anpassen
GRAFANA_URL="http://localhost:3000"
GRAFANA_USER="admin"
GRAFANA_PASS="admin"

for f in *.json; do
  echo "Importiere: $f"
  curl -s -X POST \
    -H "Content-Type: application/json" \
    -u "$GRAFANA_USER:$GRAFANA_PASS" \
    -d "{\"dashboard\": $(cat $f), \"overwrite\": true, \"folderId\": 0}" \
    "$GRAFANA_URL/api/dashboards/import"
  echo ""
done
```

---

## Schritt 3 — Variablen konfigurieren

Alle Dashboards nutzen diese Variablen (automatisch erkannt):

| Variable | Beschreibung | Beispielwert |
|----------|--------------|--------------|
| `$datasource` | Prometheus Datasource | Prometheus |
| `$node` | Server/Node auswählen | docker-swarm |
| `$job` | Prometheus Job | node |

**Anpassen**: Dashboard → ⚙️ Settings → Variables

---

## Schritt 4 — Empfohlene Einstellungen

```
Refresh-Intervall:  5 Minuten (Standard)
Zeitraum:           Letzte 24 Stunden
Theme:              Dark (optimiert)
Auflösung:          1920x1080
```

---

## Troubleshooting

### "No data" in Panels
- Prometheus läuft? → `curl http://localhost:9090/-/healthy`
- Node Exporter läuft? → `curl http://localhost:9100/metrics | head`
- Datasource-URL korrekt? → Grafana → Data Sources → Test

### Docker-Panels leer
- cAdvisor installieren und in Prometheus scrapen:
```yaml
# prometheus.yml
- job_name: 'cadvisor'
  static_configs:
    - targets: ['cadvisor:8080']
```

### Alerts-Dashboard zeigt nichts
- Alertmanager muss konfiguriert sein
- Prometheus Alerting-Rules vorhanden?

---

## Node Exporter — Schnellstart (Docker)

```bash
docker run -d \
  --name node-exporter \
  --pid="host" \
  -v "/:/host:ro,rslave" \
  -p 9100:9100 \
  prom/node-exporter:latest \
  --path.rootfs=/host
```

---

## Support & Community

- **Issues**: GitHub Repository
- **Docs**: [Grafana Dokumentation](https://grafana.com/docs/)
- **Node Exporter Metriken**: [Prometheus Docs](https://prometheus.io/docs/guides/node-exporter/)

---

*AI-Engineerings | DACH-optimiert | Getestet auf Grafana 10.x | 2026*

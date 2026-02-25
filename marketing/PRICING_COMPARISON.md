# Pricing Vergleich — Self-Hosted AI vs. Cloud-Alternativen

> **Ziel**: Zeigen warum unsere Produkte günstiger sind als Cloud-Alternativen.
> **Stand**: 2026-02-25 | ai-engineering.at

---

## Cloud AI Kosten vs. Self-Hosted (Monatlich)

| Lösung | Cloud-Anbieter | Monatliche Kosten | Self-Hosted | Ersparnis/Jahr |
|--------|---------------|-------------------|-------------|----------------|
| **KI-Analyse / LLM** | OpenAI GPT-4o | ~50–200 USD | Ollama lokal: 0 EUR | bis zu 2.400 USD |
| **Automation** | Zapier Pro | 73 USD | n8n Self-Hosted: 0 EUR | 876 USD |
| **Monitoring** | Datadog Essentials | 23 USD/Host × 3 | Grafana + Prometheus: 0 EUR | 828 USD |
| **Uptime Monitoring** | Better Uptime Team | 24 USD | Uptime Kuma: 0 EUR | 288 USD |
| **Compliance Tools** | OneTrust Basic | ab 500 USD | n8n DSGVO-Workflow: einmalig | ~6.000 USD |
| **Team-Kommunikation** | Slack Pro | 7,25 USD/User × 5 | Mattermost Self-Hosted: 0 EUR | 435 USD |

**Gesamt Cloud-Kosten**: ~700–1.000 USD/Monat
**Gesamt Self-Hosted**: ~10–20 EUR/Monat (nur Strom + Server)
**Ersparnis**: **bis zu 11.000 USD/Jahr**

---

## Unsere Produkte — Einmalkosten statt Abo

### Was du einmalig zahlst — und nie wieder

| Produkt | Preis | Ersetzt | Cloud-Kosten/Jahr |
|---------|-------|---------|-------------------|
| **n8n Starter Bundle** | EUR 19 | Zapier Pro (3 Workflows) | ~876 USD |
| **Grafana Dashboard Pack** | EUR 29 | Datadog Essentials (3 Hosts) | ~828 USD |
| **AI Agent Team Blueprint** | EUR 19 | Consulting + Setup-Zeit (10h) | ~500–2.000 USD |

### ROI-Rechnung (Beispiel: Kleines Team)

```
Cloud-Alternative monatlich:
  Zapier Pro:          73 USD
  Datadog 3 Hosts:     69 USD
  OpenAI API:         ~80 USD
  Slack 5 User:        36 USD
  ──────────────────────────
  Gesamt:            258 USD/Monat = 3.096 USD/Jahr

Unsere Lösung:
  n8n Starter Bundle:     19 EUR (einmalig)
  Grafana Dashboard Pack: 29 EUR (einmalig)
  Server (VPS o. Homelab):~10 EUR/Monat
  ──────────────────────────────────────
  Jahr 1:    168 EUR
  Jahr 2+:   120 EUR/Jahr

Ersparnis Jahr 1:  ~2.750 USD
Ersparnis Jahr 2+: ~2.850 USD/Jahr
```

---

## Feature-Vergleich: n8n vs. Zapier

| Feature | Zapier Pro (73 USD/mo) | n8n Self-Hosted (0 EUR) |
|---------|------------------------|--------------------------|
| Workflows | 20 Zaps | Unbegrenzt |
| Task-Limit | 2.000/Monat | Unbegrenzt |
| DSGVO-Konformität | ⚠️ US-Server | ✅ eigener Server |
| KI-Integration | Nur OpenAI | ✅ Ollama, Claude, etc. |
| Anpassbarkeit | Gering | ✅ Vollständig |
| Vendor Lock-in | Hoch | ✅ Keine |
| **Kosten/Jahr** | **876 USD** | **0 EUR** |

---

## Feature-Vergleich: Grafana Stack vs. Datadog

| Feature | Datadog (23 USD/Host) | Grafana + Prometheus (0 EUR) |
|---------|----------------------|-------------------------------|
| Hosts inklusive | 1 (dann +23 USD/Host) | Unbegrenzt |
| Daten-Retention | 15 Tage | Beliebig konfigurierbar |
| Custom Dashboards | Begrenzt | ✅ Unbegrenzt |
| Alerting | ✅ | ✅ |
| DSGVO | ⚠️ US-Anbieter | ✅ 100% lokal |
| **3 Hosts / Jahr** | **828 USD** | **0 EUR** |

---

## Feature-Vergleich: Self-Hosted LLM vs. OpenAI API

| Feature | OpenAI GPT-4o API | Ollama lokal (llama3.1:8b) |
|---------|-------------------|---------------------------|
| Kosten | ~0,005 USD/1k Token | 0 EUR |
| Datenschutz | ⚠️ Daten an US-Server | ✅ Bleibt lokal |
| DSGVO-konform | ⚠️ Problematisch | ✅ Ja |
| Geschwindigkeit | Gut | Gut (GPU empfohlen) |
| Offline-Betrieb | ❌ | ✅ |
| **100k Anfragen/Monat** | **~50–200 USD** | **0 EUR** |

---

## Warum Self-Hosted für DACH-Unternehmen?

### DSGVO-Risiko mit Cloud-Tools

| Risiko | Cloud (US-Anbieter) | Self-Hosted |
|--------|---------------------|-------------|
| Datentransfer in USA | ⚠️ Standard | ✅ Kein Transfer |
| Auskunftspflicht Art.15 | ⚠️ Schwierig | ✅ Vollständige Kontrolle |
| Recht auf Löschung Art.17 | ⚠️ Abhängig vom Anbieter | ✅ Sofort möglich |
| Verarbeitungsverzeichnis Art.30 | ⚠️ Aufwändig | ✅ Automatisiert (n8n) |
| DSGVO-Bußgeld-Risiko | Hoch | Minimal |

---

## Unsere Preisphilosophie

> **Einmal zahlen. Für immer nutzen. Keine Überraschungen.**

Wir glauben: Gute Tools sollten erschwinglich und transparent sein.

- **Kein Abo-Modell** — du kaufst einmal, du nutzt es dauerhaft
- **Kein Vendor Lock-in** — offene Formate (JSON, Markdown, Bash)
- **Kein Datenschutz-Kompromiss** — alles läuft auf deinem Server
- **Echter ROI** — unsere Produkte amortisieren sich in wenigen Wochen

---

## Schnellstart-Rechner

**Wie viel sparst du?**

```
Wenn du aktuell zahlst für:
  □ Zapier / Make.com        → n8n Starter Bundle spart dir: ~800+ USD/Jahr
  □ Datadog / New Relic      → Grafana Pack spart dir:       ~800+ USD/Jahr
  □ OpenAI API               → Ollama Blueprint spart dir:   ~600+ USD/Jahr
  □ Consulting für KI-Setup  → Blueprint spart dir:          ~500+ USD (einmalig)

Gesamtpaket (alle 3 Produkte): EUR 67
Ersparnis Jahr 1:              2.000–5.000 USD
```

---

*ai-engineering.at | Self-Hosted AI für DACH | 2026*

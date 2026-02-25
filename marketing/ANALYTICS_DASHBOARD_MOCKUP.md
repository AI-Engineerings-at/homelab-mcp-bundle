# Analytics Dashboard Mockup — Post-Launch KPIs
## AI-Engineering.at

**Stand**: 2026-02-25
**Verantwortlich**: @lisa01

---

## Dashboard-Struktur (4 Bereiche)

```
┌─────────────────────────────────────────────────────────────────┐
│  AI-Engineering.at — Sales Dashboard                           │
│  Zeitraum: [Heute] [7 Tage] [30 Tage] [Gesamt]               │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│  REVENUE     │  TRAFFIC     │  CONVERSION  │  PRODUCTS         │
│  €0 heute    │  0 Besucher  │  0%          │  0 Verkäufe       │
└──────────────┴──────────────┴──────────────┴───────────────────┘
```

---

## KPI-Block 1: Revenue (Umsatz)

| KPI | Beschreibung | Quelle | Ziel (Monat 1) |
|-----|-------------|--------|---------------|
| **Tagesumsatz** | Revenue heute | Gumroad API | €50/Tag |
| **Monatsumsatz** | MTD Revenue | Gumroad | €500 |
| **Durchschn. Bestellwert** | AOV (Avg Order Value) | Gumroad | €35 |
| **Refund-Rate** | % Rückerstattungen | Gumroad | <5% |
| **Revenue by Product** | Umsatz pro Produkt | Gumroad | - |
| **Affiliate Revenue** | Über Affiliates | Gumroad | 20% des Total |

---

## KPI-Block 2: Traffic (Website)

| KPI | Beschreibung | Quelle | Ziel (Monat 1) |
|-----|-------------|--------|---------------|
| **Unique Visitors** | Eindeutige Besucher | Plausible/GA | 1.000/Monat |
| **Page Views** | Gesamt-Seitenaufrufe | Plausible | 3.000/Monat |
| **Bounce Rate** | Absprungrate Landing | Plausible | <60% |
| **Avg. Session Duration** | Verweildauer | Plausible | >2 Min |
| **Traffic Sources** | Organisch/Social/Direct | Plausible | - |
| **Top Pages** | Meistbesuchte Seiten | Plausible | - |

---

## KPI-Block 3: Conversion

| KPI | Beschreibung | Formel | Ziel |
|-----|-------------|--------|------|
| **Landing → Gumroad** | Click-through zu Produkt | Klicks / Besucher | >10% |
| **Gumroad → Kauf** | Kaufabschluss-Rate | Käufe / Gumroad-Besucher | >5% |
| **Email → Kauf** | Email-to-Sale | Käufe / Email-Klicks | >2% |
| **Overall CVR** | Gesamt-Conversion | Käufe / Unique Visitors | >1% |

---

## KPI-Block 4: Email / Newsletter

| KPI | Beschreibung | Quelle | Ziel |
|-----|-------------|--------|------|
| **Subscriber Growth** | Neue Abonnenten/Tag | Rapidmail | +10/Tag |
| **Gesamtliste** | Total Subscribers | Rapidmail | 500 nach Monat 1 |
| **Open Rate** | Email-Öffnungsrate | Rapidmail | >40% |
| **Click Rate** | Link-Klicks in Emails | Rapidmail | >5% |
| **Unsubscribe Rate** | Abmelderate | Rapidmail | <1% |

---

## KPI-Block 5: Social / Community

| KPI | Beschreibung | Quelle | Ziel |
|-----|-------------|--------|------|
| **GitHub Stars** | Repo Stars | GitHub API | +50/Monat |
| **Twitter Impressions** | Tweet-Reichweite | Twitter Analytics | 10k/Monat |
| **LinkedIn Reach** | Post-Reichweite | LinkedIn | 5k/Monat |
| **Reddit Upvotes** | Karma bei Posts | Reddit | >100 pro Post |
| **HN Points** | Hacker News Show HN | HN | >50 |

---

## Tool-Empfehlung (Self-Hosted = passend zum Brand)

### Option A: Plausible Analytics (EMPFOHLEN)
- **Self-Hosted** auf eigenem Server (Docker)
- DSGVO-konform by default (kein Cookie-Banner nötig!)
- Leichtgewichtig, schön, Open Source
- Kosten: €0 (self-hosted) oder €9/Monat (Cloud)
- **USP**: Passt perfekt zum "Self-Hosted AI"-Brand!

```bash
# Docker Deploy
docker run -d --name plausible \
  -p 8000:8000 \
  ghcr.io/plausible/community-edition:latest
```

### Option B: Grafana (bereits vorhanden!)
- Nutze bestehenden Grafana Stack (.80:3000)
- Datenquellen: Gumroad Webhook → n8n → InfluxDB/PostgreSQL → Grafana
- Vorteil: Kein neues Tool, alles integriert
- Custom Dashboard "Sales Overview" erstellen

### Option C: Google Analytics 4 (nicht empfohlen)
- Datenschutz-Problem (US-Server)
- Widerspricht DSGVO-USP
- Cookie-Banner nötig

---

## n8n Integration für Sales Dashboard

```
Gumroad Webhook
    ↓
n8n Workflow "Sales Tracker"
    ↓
PostgreSQL (bestehend auf .80)
    ↓
Grafana Dashboard "Sales Overview"
    ↓
Täglicher Report → Mattermost #echo_log
```

### n8n Workflow (Konzept)
1. **Trigger**: Gumroad Webhook bei Kauf
2. **Parse**: Produkt, Preis, Land, Affiliate extrahieren
3. **Speichern**: INSERT in PostgreSQL `sales` Tabelle
4. **Aggregat**: Daily/Weekly Summary berechnen
5. **Report**: Täglich 08:00 → Mattermost Nachricht

---

## Weekly Review Template (Mattermost Report)

```
📊 **Weekly Sales Report — KW XX**

💰 Revenue: €XX (Ziel: €125/Woche)
🛒 Verkäufe: X (n8n: X | Grafana: X | Blueprint: X)
👥 Traffic: X Visitors (↑/↓ X% vs. Vorwoche)
📬 Email-Liste: XXX Subscriber (+X diese Woche)
⭐ GitHub Stars: XX (+X)

Top-Kanal: [Organisch/Twitter/Reddit/HN]
Best Seller: [Produktname]

🎯 Fokus nächste Woche: [Action Item]
```

---

## Implementierungs-Priorität

| Priorität | KPI | Tool | Aufwand |
|-----------|-----|------|---------|
| 🔴 Sofort | Revenue, Verkäufe | Gumroad Dashboard | 0h (bereits vorhanden) |
| 🟡 Woche 1 | Website Traffic | Plausible self-hosted | 2h |
| 🟡 Woche 1 | Email KPIs | Rapidmail Dashboard | 0h |
| 🟢 Woche 2 | Sales → Grafana | n8n + PostgreSQL | 4h |
| 🟢 Monat 1 | Affiliate Tracking | Gumroad built-in | 1h |
| 🔵 Optional | Social Media | Manuelle Weekly | 0.5h/Woche |

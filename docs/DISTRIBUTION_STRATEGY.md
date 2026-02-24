# Vertriebsstrategie — Digitale Produkte (Templates, n8n Workflows)

**Erstellt**: 2026-02-24 | **@lisa01** | Research-basiert

---

## Wo wir verkaufen sollten

### Sofort starten (0 Setup, geringste Reibung)

| Plattform | Gebühr | Stärken | Best für |
|-----------|--------|---------|----------|
| **Gumroad** | 10% | Sofort live, EU VAT inkl., Discovery | Alle Produkte |
| **Payhip** | 5% | Beste Marge für EU, Sofort-Auszahlung | DACH-Fokus |
| **Lemon Squeezy** | 5% + $0.50 | EU VAT, SaaS-freundlich | n8n Bundles |

### Nischen-Marktplätze (für Reichweite)

| Plattform | Produkt | URL |
|-----------|---------|-----|
| **n8nmarket.com** | n8n Workflows | Premium-Marktplatz für Automation |
| **managen8n.com** | n8n Workflows | Detaillierte Metriken, Community |
| **haveworkflow.com** | n8n Workflows | Globales Publikum |
| **Notion Template Gallery** | Notion Templates | Organischer Traffic, kostenlos |

### Eigener Shop (maximale Kontrolle, 0% Plattform-Gebühr)

**WooCommerce** läuft bereits auf unserem Stack!  
→ `pkC1dFF3qVf3xusI` (WooCommerce ↔ Odoo Bestands-Sync) — bereits aktiv  
→ Stripe Payment → n8n → Download-Link (bereits gebaut: `nPvIiIoVrL3uoxDu`)

**Empfehlung**: WooCommerce als Haupt-Shop (0% externe Gebühr), Gumroad/Payhip als Discovery-Kanal.

---

## Empfohlene Multi-Channel Strategie

```
Kunden finden uns über:           → Kaufen bei:          → Automation via n8n:
─────────────────────────────────────────────────────────────────────────
Reddit, Discord, Dev.to           → Gumroad (Discovery)  → Webhook → E-Mail
Notion Template Gallery           → Payhip (EU-fokus)    → Webhook → E-Mail
n8nmarket.com, managen8n.com      → n8nmarket.com        → direkt
Eigene Landing Page (Playbook01)  → WooCommerce (0%)     → Stripe → n8n
```

---

## Automation mit n8n (bereits vorhanden!)

| Workflow | ID | Status |
|----------|----|--------|
| Stripe Payment → Download-Link → Email | nPvIiIoVrL3uoxDu | ✅ AKTIV |
| Stripe Payment → Resend Email | e4ZkJk7Ii6nFbYF9 | ✅ AKTIV |
| Rapidmail DOI → Download-Link | sULflCy4Y6x2ZoxM | ✅ AKTIV |

**Was noch fehlt**:
- Gumroad Webhook → n8n → Download-Link (10 Min Aufwand)
- Payhip Webhook → n8n → Download-Link (ähnlich)

---

## Neue Shop-Seite für Templates?

### Option A: Subdomain auf Playbook01
`templates.playbook01.de` — eigene Landing Page, WooCommerce Checkout

### Option B: Eigenständiger Shop
Payhip Store (kostenlos, 5% Gebühr) — sofort live, kein eigener Server

### Option C: Gumroad Profile Page
Alle Produkte unter einem Gumroad-Profil — Discovery inklusive

**Empfehlung @joe**: Option B (Payhip) sofort starten, parallel Option A aufbauen.

---

## Preisgestaltung (Research-basiert)

| Produkt | Marktpreis | Unser Preis |
|---------|------------|-------------|
| n8n Starter Bundle (3 Workflows) | EUR 19-49 | **EUR 29** |
| Grafana Dashboard Pack (6) | EUR 9-19 | **EUR 12** |
| DSGVO Art.30 Notion Template | EUR 9-19 | **EUR 12** |
| n8n DACH AI Bundle (premium) | EUR 49-99 | **EUR 49** |

**Integration-Templates** (n8n + Notion zusammen) erzielen EUR 75-150.

---

## Nächste Schritte für @joe (priorisiert)

1. **Payhip Account erstellen** (payhip.com, 5 Min) — sofortiger EU-konformer Shop
2. **Gumroad Account** (als Discovery-Kanal, 10% Gebühr)  
3. Produkte hochladen (PDFs + ZIP-Dateien)
4. n8n Webhook für Payhip/Gumroad anpassen (ich mache das)

---

*Quellen: n8nmarket.com, managen8n.com, Payhip/Gumroad Vergleiche 2026*

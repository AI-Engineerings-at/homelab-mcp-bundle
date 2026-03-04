# Joe-Blocker: 5 Schritte zum fertigen AI-Engineering Store
## Jeder Schritt max. 3 Minuten — Gesamtzeit: ~15 Min

---

## Warum dieser 1-Pager?

Die Infrastruktur ist FERTIG. Download-Service läuft. Stripe ist konfiguriert.
**Nur @joe kann diese 5 Dinge tun** — kein Agent hat Zugriff.

---

## Schritt 1: Gumroad Produkte hochladen (3 Min)

**URL**: https://app.gumroad.com/products/new

Für jedes Produkt einmal:
1. Cover-Image wählen (Pfad: `/home/joe/cli_bridge/products/cover-templates/`)
   - AI Blueprint → `cover-ai-agent-blueprint-sq.png`
   - n8n Bundle → `cover-n8n-starter-bundle-sq.png`
   - Grafana Pack → `cover-grafana-dashboard-pack-sq.png`
   - DSGVO Bundle → `cover-dsgvo-art30-bundle-sq.png`
   - MCP Bundle → `cover-homelab-mcp-bundle-sq.png` (FREE)
2. ZIP-Datei hochladen (liegt in `/home/joe/cli_bridge/tools/download-issuer/files/`)
3. Preis setzen (laut Memory: Blueprint €19, n8n €29, Grafana €39, DSGVO €79, MCP FREE)
4. Publish

**@jim02 macht das** — du musst nur freigeben / Credentials übergeben

---

## Schritt 2: Stripe Webhook HTTPS umstellen (2 Min)

Aktuell läuft der Download-Service nur intern (`:3002`).
Nach Cloudflare Tunnel Setup (Anleitung: `docs/cloudflare-tunnel-setup.md`):

1. Stripe Dashboard → **Developers → Webhooks**
2. Endpoint URL ändern:
   - ALT: `http://10.40.10.99:3002/webhook/stripe`
   - NEU: `https://download.ai-engineering.at/webhook/stripe`
3. Save

**Erst nach Cloudflare Tunnel Setup!** (Anleitung dauert 15 Min, einmalig)

---

## Schritt 3: Rapidmail Account aktivieren (3 Min)

Für automatische Email-Sequenzen (Double-Opt-In, Newsletter):

1. https://www.rapidmail.de → Account erstellen/einloggen
2. **API Key** generieren: Einstellungen → API → Neuen Key erstellen
3. API Key in n8n speichern:
   - n8n → Credentials → New → HTTP Header Auth
   - Name: `Rapidmail API`
   - Header: `Authorization`, Value: `Basic YOUR_API_KEY`
4. Workflow `Rapidmail: Double-Opt-In` aktivieren (ist schon vorbereitet)

---

## Schritt 4: Cloudflare Tunnel einrichten (15 Min einmalig)

Anleitung: `/home/joe/cli_bridge/docs/cloudflare-tunnel-setup.md`

Schritte (Copy-Paste bereit):
1. Cloudflare Dashboard → Tunnel erstellen → Token kopieren
2. DNS Routen konfigurieren (n8n, download, api)
3. Docker Stack deployen (ein Befehl)
4. Testen

**Danach funktioniert**: Stripe Webhooks, öffentliche Download-URLs, externe n8n Trigger

---

## Schritt 5: n8n Community Templates einreichen (3 Min pro Template)

4 Templates sind fertig und submission-ready:
- `~/.claude/n8n-workflows/community-templates/template_01_stripe_delivery.json`
- `~/.claude/n8n-workflows/community-templates/template_02_social_media_ai.json`
- `~/.claude/n8n-workflows/community-templates/template_03_lead_magnet_delivery.json`
- `~/.claude/n8n-workflows/community-templates/template_04_mattermost_ollama_bot.json`

Alle Texte (Titel, Beschreibung, Tags) fertig in:
`~/.claude/n8n-workflows/community-templates/SUBMISSION_GUIDE.md`

**Einreichen**:
1. https://n8n.io/sign-up (Account erstellen)
2. https://n8n.io/workflows/submit
3. JSON + Texte aus Guide einfügen → Submit

**Wert**: 4x Backlinks von n8n.io (Domain Authority ~70) + gratis Traffic

---

## Status-Übersicht

| Schritt | Was | Wer | Status |
|---------|-----|-----|--------|
| 1 | Gumroad Produkte | @jim02 + @joe Freigabe | ⏳ Warten |
| 2 | Stripe HTTPS | @joe | ⏳ Nach CF Tunnel |
| 3 | Rapidmail API | @joe (5 Min) | ⏳ |
| 4 | Cloudflare Tunnel | @joe (15 Min) | ⏳ |
| 5 | n8n Templates | @joe oder @lisa01 | ✅ Bereit |

---

## Was FERTIG ist (kein Blocker):

- ✅ Download-Service auf .99:3002 (alle 6 Produkte)
- ✅ Stripe Checkout Links (5 Produkte)
- ✅ n8n Workflow: Stripe → Download Email
- ✅ n8n Workflow: Lead Magnet Delivery
- ✅ n8n Templates (4 Stück, submission-ready)
- ✅ Cover-Images für alle Produkte
- ✅ Landing Page mit Stripe Checkout
- ✅ Cloudflare Tunnel Anleitung (Copy-Paste)

**Der Store ist zu 90% fertig. Du entsperrst die letzten 10% in ~15 Minuten.**

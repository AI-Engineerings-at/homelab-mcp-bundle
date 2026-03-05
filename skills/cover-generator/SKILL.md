# Skill: cover-generator (v12 — CANONICAL)

> **DER** Standard-Generator für alle Produkt-Thumbnails. Immer v12, kein anderer.

## Zweck
800×800 Produkt-Thumbnails für Gumroad/Stripe — exakt dieses Design, immer konsistent.

## Layout v12 (heilig — nicht abweichen!)
```
┌──────────────────────────────────────────────┐
│  [BADGE: Most Popular]           top-15px    │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │  Produkt-Screenshot (echt)           │   │  0–336px (42%)
│  │  ODER CSS-Mockup: Emoji + Features   │   │
│  │  Gradient-Blend nach unten           │   │
│  └──────────────────────────────────────┘   │
│  ─ ─ ─ ─ Separator-Line ─ ─ ─ ─ ─ ─ ─ ─    │
│  EYEBROW · CATEGORY TEXT                     │  Content: 42–89%
│  Product <em>Title</em>                      │
│  [Feature 1] [Feature 2] [Feature 3]         │
│  [Feature 4]                                 │
│  ────────────────────────────────────        │
│  180+    42      15+          [EUR 49]        │
│  Pages   Diag.   Services                    │
├──────────────────────────────────────────────┤
│  🦅 AI Engineering          ai-engineering.at│  Brand Strip: 32px
└──────────────────────────────────────────────┘

Eagle Watermark: center top:38%, 580×580px, opacity 0.22
→ Schriftzug sichtbar bei ~60% (Übergang Screenshot/Content)
Left Accent Line: 3px, full height, gradient in Accent-Farbe
Orb Glows: top-right + bottom-left, subtle radial in Accent
Grid Overlay: 46×46px, Accent-Farbe 7% opacity
```

## Usage

```bash
# Alle 7 Thumbnails generieren (Standard)
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py

# Einzelne Produkte
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py n8n-starter-bundle
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py grafana-dashboard-pack dsgvo-art30-bundle

# Status / Liste
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py --list

# Debug (HTML ohne Screenshot)
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py --dry-run

# Custom Output
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py --out /tmp/test
```

**Output**: `products/covers/thumbnail-{id}.png`

## Produkte (7 Produkte, stabil)

| ID | Titel | Preis | Accent | Screenshot |
|----|-------|-------|--------|------------|
| `localai-playbook` | Local AI Stack Playbook | EUR 49 | `#10B981` Emerald | — mockup |
| `n8n-starter-bundle` | n8n Starter Bundle | EUR 29 | `#FB923C` Orange | `n8n-workflows-dark.png` |
| `grafana-dashboard-pack` | Grafana Dashboard Pack | EUR 39 | `#60A5FA` Blue | `grafana-infra-overview.png` |
| `dsgvo-art30-bundle` | DSGVO Art.30 Bundle | EUR 79 | `#C084FC` Purple | — mockup |
| `homelab-mcp-bundle` | Homelab MCP Bundle | FREE | `#22D3EE` Cyan | — mockup |
| `ai-agent-blueprint` | AI Agent Team Blueprint | EUR 19 | `#4ADE80` Green | — mockup |
| `komplett-bundle` | AI Engineering Komplett Bundle | EUR 149 | `#F59E0B` Amber | — mockup |

## Farben (unveränderlich!)

| Produkt | Accent | Dark | Gradient |
|---------|--------|------|----------|
| localai-playbook | `#10B981` | `#059669` | `175deg,#020817,#041a10,#020d14` |
| n8n-starter-bundle | `#FB923C` | `#EA580C` | `175deg,#0c0800,#1a1000,#0c0800` |
| grafana-dashboard-pack | `#60A5FA` | `#2563EB` | `175deg,#020817,#0a1220,#020817` |
| dsgvo-art30-bundle | `#C084FC` | `#9333EA` | `175deg,#080010,#120020,#080010` |
| homelab-mcp-bundle | `#22D3EE` | `#0891B2` | `175deg,#020b0d,#031520,#020b0d` |
| ai-agent-blueprint | `#4ADE80` | `#16A34A` | `175deg,#010d02,#021508,#010d02` |
| komplett-bundle | `#F59E0B` | `#D97706` | `175deg,#0d0800,#1a1000,#0d0800` |

## Neues Produkt hinzufügen

1. Eintrag in `SCREENSHOTS` dict in `gen_thumbnails_v12.py`:
```python
"mein-produkt": BASE / "screenshot.png",  # oder None für Mockup
```
2. Eintrag in `PRODUCTS` Liste:
```python
{"id": "mein-produkt",
 "accent": "#FF6B6B", "accent_dark": "#CC0000",
 "gradient": "linear-gradient(175deg,#0d0000 0%,#1a0000 55%,#0d0000 100%)",
 "badge": "New Release", "eyebrow": "Kategorie · Subcategory",
 "title": "Mein <em>Produkt</em> Name",
 "features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4"],
 "stats": [("10+", "Items"), ("Free", "Tier"), ("1-Click", "Setup")],
 "price": "EUR 99", "icon": "🔥"},
```
3. Generator laufen lassen, fertig.

## Dateipfade (kanonisch)

| Datei | Pfad |
|-------|------|
| **Generator** (THE script) | `tools/cover-generator/gen_thumbnails_v12.py` |
| **Output** | `products/covers/thumbnail-{id}.png` |
| **Temp HTML** | `/tmp/thumb_v12_{id}.html` |
| **Eagle** | `/home/joe/Playbook01/landing-page/public/eagle-logo-inverted.png` |
| **Alte Scripts** | `tools/cover-generator/_archive/` |
| **Alte Covers** | `products/cover-templates/_archive/` |

## Screenshots hinzufügen

```python
# In gen_thumbnails_v12.py → SCREENSHOTS dict:
SCREENSHOTS = {
    ...
    "localai-playbook": BASE / "localai-playbook-screenshot.png",  # real screenshot
}
```
Screenshot ablegen als: `/home/joe/cli_bridge/<name>.png` (800px+ breit, 16:9 oder ähnlich)

## Abhängigkeiten

```bash
pip install playwright
playwright install chromium
# Google Fonts werden live geladen (Internet erforderlich!)
```

## Regeln (ABSOLUT!)

- **NIEMALS** einen anderen Generator verwenden (v1-v11, v2-v5, electric, diagonal — alle archiviert)
- **NIEMALS** HTML-Templates manuell in `products/cover-templates/` anlegen (nur _archive dort)
- **IMMER** `gen_thumbnails_v12.py` → Output nach `products/covers/`
- **Farben** nicht eigenmächtig ändern — nur nach Joe-Freigabe
- Nach Änderung: alle 7 neu rendern und in Repo committen

## Version History

| Version | Datum | Änderung |
|---------|-------|----------|
| v12 | 2026-03-05 | CANONICAL. Eagle@38%, Produktbild-Slot oben, Separator, Brand Strip |
| v1-v11 | pre | Archiviert in `_archive/` — nicht verwenden |

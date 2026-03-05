# Skill: thumbnail-generator (v12)

## Zweck
Generiert 800x800 Produkt-Thumbnails die als Produktbild-Cards in den Gumroad/Stripe Covers (gen_covers_v5.py) eingebettet werden.

## Layout v12

```
┌──────────────────────────────────────────────┐
│  [BADGE: Bestseller 2025]                    │  ← Zeile 15px von oben
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │  Produkt-Screenshot (echte Aufnahme) │   │  ← top 0–336px (42%)
│  │  ODER CSS-Mockup mit Icon+Features   │   │
│  │  (Gradient-Blend nach unten)         │   │
│  └──────────────────────────────────────┘   │
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │  ← Separator-Line
│  EYEBROW TEXT                                │  ← Content (42%–89%)
│  Product <em>Title</em>                      │
│  [Feature 1] [Feature 2] [Feature 3]         │
│  ──────────────────────────────────────      │
│  180+    42      15+          [EUR 49]        │
│  Pages   Diag.   Services                    │
├──────────────────────────────────────────────┤
│  🦅 AI Engineering          ai-engineering.at│  ← Brand Strip
└──────────────────────────────────────────────┘

Eagle Watermark: center bei top:38% → 580×580px, opacity 0.22
  → Schriftzug (Logo-Text) sichtbar bei ~60% (zwischen Screenshot und Content)
```

## Usage

```bash
# Alle 6 Produkte generieren
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py

# Einzeln
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py n8n-starter-bundle
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py grafana-dashboard-pack dsgvo-art30-bundle

# Status (Screenshot vorhanden?)
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py --list

# HTML generieren ohne Screenshot (Debug)
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py --dry-run

# Custom Output-Dir
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py --out /tmp/thumbs-test
```

## Produkte

| ID | Titel | Preis | Screenshot |
|----|-------|-------|------------|
| `localai-playbook` | Local AI Stack Playbook | EUR 49 | — mockup |
| `n8n-starter-bundle` | n8n Starter Bundle | EUR 29 | `n8n-workflows-dark.png` |
| `grafana-dashboard-pack` | Grafana Dashboard Pack | EUR 39 | `grafana-infra-overview.png` |
| `dsgvo-art30-bundle` | DSGVO Art.30 Bundle | EUR 79 | — mockup |
| `homelab-mcp-bundle` | Homelab MCP Bundle | FREE | — mockup |
| `ai-agent-blueprint` | AI Agent Team Blueprint | EUR 19 | — mockup |

## Screenshots hinzufuegen

Screenshot-Pfad in `SCREENSHOTS` dict eintragen:
```python
SCREENSHOTS = {
    "localai-playbook": BASE / "localai-playbook-screenshot.png",  # neu
    ...
}
```
Screenshot ablegen als: `/home/joe/cli_bridge/<name>.png`

## Design-Details

- **Renderer**: Playwright Chromium Headless
- **Fonts**: Inter + Space Grotesk (Google Fonts, Internet required)
- **Eagle**: `/home/joe/Playbook01/landing-page/public/eagle-logo-inverted.png` (288KB)
- **Eagle-Position**: `top:38%` center, `transform:translate(-50%,-50%)`
  - Schriftzug ("AI Engineering") landet bei ~60% von oben
  - Sichtbar zwischen Produktbild (0–42%) und Content (42%–89%)
- **Screenshot-Bereich**: 336px hoch (42%), `object-fit:cover`, Gradient-Blend nach unten
- **Brand Strip**: 32px unten, Eagle-Logo + "AI Engineering" + URL

## Farben je Produkt

| Produkt | Accent | Dark |
|---------|--------|------|
| localai-playbook | `#10B981` Emerald | `#059669` |
| n8n-starter-bundle | `#FB923C` Orange | `#EA580C` |
| grafana-dashboard-pack | `#60A5FA` Blue | `#2563EB` |
| dsgvo-art30-bundle | `#C084FC` Purple | `#9333EA` |
| homelab-mcp-bundle | `#22D3EE` Cyan | `#0891B2` |
| ai-agent-blueprint | `#4ADE80` Green | `#16A34A` |

## Output-Dateien

- **Script**: `tools/cover-generator/gen_thumbnails_v12.py`
- **Output**: `products/cover-templates/thumbnail-{id}.png`
- **Temp HTML**: `/tmp/thumb_v12_{id}.html` (Debug)

## Version History

| Version | Datum | Aenderung |
|---------|-------|-----------|
| v12 | 2026-03-05 | Eagle 52%→38%, Produktbild-Slot oben, Schriftzug sichtbar |
| v1-v11 | pre | Handgecraftete HTMLs (~773KB mit embedded base64) |

## Abhaengigkeiten

```bash
pip install playwright
playwright install chromium
```

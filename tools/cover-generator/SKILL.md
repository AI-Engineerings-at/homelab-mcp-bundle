# Skill: cover-generator (v12 — CANONICAL)

## Zweck
Generiert professionelle Gumroad/Stripe Cover-Images (800x800 PNG) via Playwright + Google Fonts.
- **v12** (2026-03-05): LEFT/RIGHT Split — Produkt füllt rechte Spalte komplett (440x800px)
- **Layout**: Links=Text (Badge, Title, Features, Stats, Preis) | Rechts=Produktbild/Mockup VOLLFLÄCHIG
- **Renderer**: Playwright Chromium Headless
- **Fonts**: Inter + Space Grotesk via Google Fonts

## Usage

```bash
# Alle 7 Thumbnails generieren (Output: products/covers/)
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py

# Einzelne Thumbnails
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py localai-playbook
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py n8n-starter-bundle dsgvo-art30-bundle

# Produktliste anzeigen
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py --list

# Dry-run (HTML ohne Screenshot)
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py --dry-run

# Custom Output-Verzeichnis
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py --out /tmp/covers-test
```

## Produkt-IDs
| ID | Produkt | Accent | Preis | Output |
|----|---------|--------|-------|--------|
| `localai-playbook` | Local AI Stack Playbook | `#10B981` Emerald | EUR 49 | thumbnail-localai-playbook.png |
| `n8n-starter-bundle` | n8n Starter Bundle | `#FB923C` Orange | EUR 29 | thumbnail-n8n-starter-bundle.png |
| `grafana-dashboard-pack` | Grafana Dashboard Pack | `#60A5FA` Blue | EUR 39 | thumbnail-grafana-dashboard-pack.png |
| `dsgvo-art30-bundle` | DSGVO Art.30 Bundle | `#C084FC` Purple | EUR 79 | thumbnail-dsgvo-art30-bundle.png |
| `homelab-mcp-bundle` | Homelab MCP Bundle | `#22D3EE` Cyan | FREE | thumbnail-homelab-mcp-bundle.png |
| `ai-agent-blueprint` | AI Agent Team Blueprint | `#4ADE80` Green | EUR 19 | thumbnail-ai-agent-blueprint.png |
| `komplett-bundle` | AI Engineering Komplett Bundle | `#F59E0B` Amber | EUR 149 | thumbnail-komplett-bundle.png |

## Design-System (v12)

### Layout 800x800 — Links/Rechts Split
```
┌──────────────────────────┬──────────────────────────────┐
│   LEFT  (360px)          │   RIGHT (440px) — VOLLFLÄCHIG │
│                          │                               │
│  [BADGE PILL]            │   ████████████████████████   │
│  EYEBROW TEXT            │   █                        █  │
│                          │   █   Produktbild /        █  │
│  Product <em>Title</em>  │   █   Mockup mit großem    █  │
│  Second Line             │   █   Icon + Features      █  │
│                          │   █   (füllt 440x800px)    █  │
│  [Feat1] [Feat2]         │   █                        █  │
│  [Feat3] [Feat4]         │   ████████████████████████   │
│  ─────────────────       │                               │
│  180+ Pages  42 Diagrams │   ← Gradient-Überblendung    │
│  EUR 49 ████             │                               │
│                          │                               │
│  AI Engineering  .at     │                               │
└──────────────────────────┴──────────────────────────────┘
```

### Design-Elemente
- **Hintergrund**: Produkt-spezifischer Dark Gradient + Subtiles Grid (46px, nur linke Spalte)
- **Dekorativ**: Orb Glows (links oben + links unten) + Accent-Linie links + Spalten-Trenner
- **Eagle Watermark**: 310px, opacity 0.11, hinter Inhalt in linker Spalte
- **Left Column** (360px):
  - Badge-Pill: accent-Farbe, uppercase, pill-Shape
  - Eyebrow: Kategorie (10px, uppercase, letter-spacing)
  - Title: 36px Space Grotesk 800, `<em>` in Accent-Farbe
  - Feature Pills: semi-transparent BG, Border
  - Stats: 3 Metriken (number + label)
  - Price: Gradient-Button (accent → accent-dark), 26px, 12px border-radius
  - Brand Strip: Eagle-Icon + "AI Engineering" + "ai-engineering.at"
- **Right Column** (440px, VOLLFLÄCHIG 800px Höhe):
  - Echte Screenshots: `object-fit:cover`, `object-position:top left`, Gradient-Überblendung links
  - CSS-Mockup: Großes Icon (110px), Eyebrow, Feature-Items mit Checkboxes
  - Gradient Blend: rechte Spalte blendet links nahtlos ins BG über

### Farben je Produkt
| Produkt | Accent | Accent Dark |
|---------|--------|-------------|
| localai-playbook | `#10B981` Emerald | `#059669` |
| n8n-starter-bundle | `#FB923C` Orange | `#EA580C` |
| grafana-dashboard-pack | `#60A5FA` Blue | `#2563EB` |
| dsgvo-art30-bundle | `#C084FC` Purple | `#9333EA` |
| homelab-mcp-bundle | `#22D3EE` Cyan | `#0891B2` |
| ai-agent-blueprint | `#4ADE80` Green | `#16A34A` |
| komplett-bundle | `#F59E0B` Amber | `#D97706` |

## Dateipfade
- **THE Script**: `tools/cover-generator/gen_thumbnails_v12.py` ← EINZIGER aktiver Generator
- **Output Primary**: `products/covers/thumbnail-{id}.png`
- **Output Mirror**: `tools/cover-generator/thumbnail-{id}.png`
- **Temp HTML**: `/tmp/thumb_v12-{id}.html` (für Debugging)
- **Eagle Logo**: `Playbook01/landing-page/public/eagle-logo-inverted.png`
- **Archive**: `tools/cover-generator/_archive/` (alle alten Versionen)

## Screenshots (echte Produktbilder)
Nur für n8n und Grafana vorhanden — andere nutzen CSS-Mockup:
```python
SCREENSHOTS = {
    "n8n-starter-bundle":     BASE / "n8n-workflows-dark.png",
    "grafana-dashboard-pack": BASE / "grafana-infra-overview.png",
    # alle anderen: None → CSS Mockup
}
```

## Neues Produkt hinzufügen
Eintrag in `PRODUCTS` Liste in `gen_thumbnails_v12.py` ergänzen:
```python
{
    "id": "mein-produkt",
    "accent": "#FF6B6B", "accent_dark": "#CC0000",
    "gradient": "linear-gradient(175deg,#0d0000 0%,#1a0000 55%,#0d0000 100%)",
    "badge": "New", "eyebrow": "Kategorie",
    "title": "Mein <em>Produkt</em>",
    "features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4"],
    "stats": [("10+", "Items"), ("Free", "Tier"), ("1-Click", "Setup")],
    "price": "EUR 99", "icon": "🔥",
}
```
Optional: echten Screenshot in `SCREENSHOTS["mein-produkt"] = BASE / "screenshot.png"` eintragen.

## Version History
| Version | Datum | Feature |
|---------|-------|---------|
| **v12** | **2026-03-05** | **LEFT/RIGHT Split — Produkt füllt rechte Spalte vollständig (440x800px)** |
| v11 | 2026-03-05 | Eagle@38%, Produktbild oben (top 42%), Top/Bottom Layout |
| v5 | 2026-03-05 | Floating Card rechts (290x290px, 3D Transform) |
| v4 | 2026-03-05 | Multi-Format (8 Formate), Eagle-Watermark |
| v2 | 2026-03-04 | 800x800, Dark Gradient, Eagle-BG |

## Abhängigkeiten
```bash
pip install playwright
playwright install chromium
```
Google Fonts werden live geladen (Internet beim Render erforderlich).

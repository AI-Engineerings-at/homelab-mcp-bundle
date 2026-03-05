# Skill: cover-generator (v5)

## Zweck
Generiert professionelle Gumroad/Stripe Cover-Images (800x800 PNG) via Playwright + Google Fonts.
- **v5** (2026-03-05): Produkt-Thumbnail als floating Card rechts + Space Grotesk Typografie
- **Layout**: Links=Text (Badge, Title, Features, Stats, Preis) | Rechts=Produktbild als 3D-Card
- **Renderer**: Playwright Chromium Headless
- **Fonts**: Inter + Space Grotesk via Google Fonts

## Usage

```bash
# Alle 7 Cover generieren (Standard-Output: products/cover-templates/)
python3 ~/cli_bridge/tools/cover-generator/gen_covers_v5.py

# Einzelne Cover
python3 ~/cli_bridge/tools/cover-generator/gen_covers_v5.py localai-playbook
python3 ~/cli_bridge/tools/cover-generator/gen_covers_v5.py n8n-starter-bundle dsgvo-art30-bundle

# Produktliste + Thumbnail-Status
python3 ~/cli_bridge/tools/cover-generator/gen_covers_v5.py --list

# HTML generieren ohne Screenshot (Debug)
python3 ~/cli_bridge/tools/cover-generator/gen_covers_v5.py --dry-run

# Custom Output-Verzeichnis
python3 ~/cli_bridge/tools/cover-generator/gen_covers_v5.py --out /tmp/covers-test
```

## Produkt-IDs
| ID | Produkt | Accent | Preis | Thumbnail |
|----|---------|--------|-------|-----------|
| `localai-playbook` | Local AI Stack Playbook | `#10B981` Emerald | EUR 49 | thumbnail-localai-playbook.png |
| `n8n-starter-bundle` | n8n Starter Bundle | `#FB923C` Orange | EUR 29 | thumbnail-n8n-starter-bundle.png |
| `grafana-dashboard-pack` | Grafana Dashboard Pack | `#60A5FA` Blue | EUR 39 | thumbnail-grafana-dashboard-pack.png |
| `dsgvo-art30-bundle` | DSGVO Art.30 Bundle | `#C084FC` Purple | EUR 79 | thumbnail-dsgvo-art30-bundle.png |
| `homelab-mcp-bundle` | Homelab MCP Bundle | `#22D3EE` Cyan | FREE | thumbnail-homelab-mcp-bundle.png |
| `ai-agent-blueprint` | AI Agent Team Blueprint | `#4ADE80` Green | EUR 19 | thumbnail-ai-agent-blueprint.png |
| `mcp-cheat-sheet` | MCP Cheat Sheet | `#22D3EE` Cyan | FREE | cover-mcp-cheat-sheet.png (kein thumbnail) |

## Design-System (v5)

### Layout 800x800
```
┌─────────────────────────────────────────────┬──────────────────────────┐
│ AI ENGINEERING     [BADGE: Bestseller 2025] │                          │
│                                             │                          │
│ EYEBROW TEXT                                │   ┌──────────────────┐   │
│                                             │   │                  │   │
│ Product <em>Title</em>                      │   │  Product Image   │   │
│ Second Line                                 │   │  (290x290 px)    │   │
│                                             │   │  floating card   │   │
│ Subtitle text here...                       │   │  3D perspective  │   │
│                                             │   └──────────────────┘   │
│ [Feature 1] [Feature 2] [Feature 3]        │                          │
│ [Feature 4]                                 │                          │
│ ──────────────────────                      │                          │
│ 180+ Pages  42 Diagrams  15+ Services  [EUR 49] │                     │
└─────────────────────────────────────────────┴──────────────────────────┘
```

### Design-Elemente
- **Hintergrund**: Produkt-spezifischer Dark Gradient + Subtiles Grid (46px)
- **Dekorativ**: Orb Glows (oben-links + unten-rechts) + Accent-Linie links + Corner-Arc
- **Eagle Watermark**: 360px, opacity 0.07, hinter Produktbild (Eagle-inverted.png von Playbook01)
- **Left Column** (432px):
  - Brand-Row: "AI ENGINEERING" (10px, uppercase) + Badge-Pill (accent)
  - Eyebrow: Kategorie (10.5px, uppercase, letter-spacing)
  - Title: 54px Space Grotesk 800, `<em>` in Accent-Farbe
  - Subtitle: 13px Inter, 46% opacity
  - Feature Pills: Subtile Border, semi-transparent BG
  - Stats: 3 Metriken (number + label)
  - Price: Gradient-Button (accent → accent-dark)
- **Right Column** (368px):
  - Thumb Card: 290x290px, border-radius 14px
  - 3D Transform: `rotateY(-5deg) rotateX(2deg)` (perspective 900px)
  - Shadow: Box-shadow mit Accent-Glow
  - Glow: Radial blur 28px unter dem Card
  - Fallback: Icon + Eyebrow text wenn kein Thumbnail vorhanden

### Farben je Produkt
| Produkt | Accent | Gradient |
|---------|--------|----------|
| localai-playbook | `#10B981` Emerald | Dark Blue → Teal-ish |
| n8n-starter-bundle | `#FB923C` Orange | Dark Brown → Orange-ish |
| grafana-dashboard-pack | `#60A5FA` Blue | Dark Blue → Mid Blue |
| dsgvo-art30-bundle | `#C084FC` Purple | Dark Purple → Deep Violet |
| homelab-mcp-bundle | `#22D3EE` Cyan | Dark Teal → Dark Navy |
| ai-agent-blueprint | `#4ADE80` Green | Near-Black → Dark Green |
| mcp-cheat-sheet | `#22D3EE` Cyan | Dark Teal → Dark Navy |

## Dateipfade
- **Script v5**: `tools/cover-generator/gen_covers_v5.py`
- **Script v4**: `tools/cover-generator/gen_covers_v4.py` (Multiformat: cover, ig-post, fb-post, etc.)
- **Output**: `products/cover-templates/{id}-cover.png`
- **Thumbnails**: `products/cover-templates/thumbnail-{id}.png`
- **Temp HTML**: `/tmp/cv5-{id}.html` (fuer Debugging)
- **Eagle Logo**: `Playbook01/landing-page/public/eagle-logo-inverted.png`

## Neues Produkt hinzufuegen
Eintrag in `PRODUCTS` Liste in `gen_covers_v5.py` ergaenzen:
```python
{
    "id": "mein-produkt",
    "accent": "#FF6B6B", "accent_dark": "#CC0000",
    "gradient": "linear-gradient(145deg,#0d0000 0%,#1a0000 45%,#0d0000 100%)",
    "badge": "New", "eyebrow": "Kategorie",
    "title": "Mein <em>Produkt</em>",
    "subtitle": "Kurze Beschreibung des Produkts.",
    "features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4"],
    "stats": [("10+", "Seiten"), ("Free", "Tier"), ("1-Click", "Setup")],
    "price": "EUR 99", "icon": "🔥",
    "thumb": "thumbnail-mein-produkt.png",  # PNG muss existieren!
}
```
Dann neues Thumbnail in `products/cover-templates/thumbnail-mein-produkt.png` ablegen.

## Version History
| Version | Datum | Feature |
|---------|-------|---------|
| v5 | 2026-03-05 | Produktbild als floating Card (rechte Haelfte), Split-Layout |
| v4 | 2026-03-05 | Multi-Format (8 Formate), Eagle-Watermark, Space Grotesk |
| v3 | 2026-03-05 | Stats-Bar, Badge+Icon, Feature Pills, Preisbox |
| v2 | 2026-03-04 | 800x800, Dark Gradient, Eagle-BG |

## Abhaengigkeiten
```bash
pip install playwright
playwright install chromium
```
Google Fonts werden live von fonts.googleapis.com geladen (Internet erforderlich beim Render).

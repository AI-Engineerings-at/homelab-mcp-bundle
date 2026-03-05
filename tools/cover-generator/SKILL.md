# Skill: cover-generator (v3)

## Zweck
Generiert professionelle Gumroad/Stripe Cover-Images (800x800 PNG) via Playwright + Google Fonts.
- **v3** (2026-03-05): Space Grotesk Typografie, Stats-Bar, Badge+Icon, Feature Pills, Preisbox
- **Renderer**: Playwright Chromium Headless
- **Fonts**: Inter + Space Grotesk via Google Fonts

## Usage

```bash
# Alle 7 Cover generieren
python3 ~/cli_bridge/tools/cover-generator/gen_covers_v3.py

# Einzelne Cover
python3 ~/cli_bridge/tools/cover-generator/gen_covers_v3.py localai-playbook n8n-starter-bundle

# Produktliste
python3 -c "import sys; sys.path.insert(0,'~/cli_bridge/tools/cover-generator'); from gen_covers_v3 import PRODUCTS; [print(p['id']) for p in PRODUCTS]"
```

## Produkt-IDs
| ID | Produkt | Accent | Preis |
|----|---------|--------|-------|
| `localai-playbook` | Local AI Stack Playbook | `#10B981` Emerald | EUR 49 |
| `n8n-starter-bundle` | n8n Starter Bundle | `#FB923C` Orange | EUR 29 |
| `grafana-dashboard-pack` | Grafana Dashboard Pack | `#60A5FA` Blue | EUR 39 |
| `dsgvo-art30-bundle` | DSGVO Art.30 Bundle | `#C084FC` Purple | EUR 79 |
| `homelab-mcp-bundle` | Homelab MCP Bundle | `#22D3EE` Cyan | FREE |
| `ai-agent-blueprint` | AI Agent Team Blueprint | `#4ADE80` Green | EUR 19 |
| `mcp-cheat-sheet` | MCP Cheat Sheet | `#22D3EE` Cyan | FREE |

## Design-Elemente (v3)
- **Badge** (oben links): "Bestseller 2025", "Most Popular" etc. + Accent-Dot
- **Icon** (oben rechts): Emoji in Accent-farbiger Box
- **Eyebrow**: Kategorie in UPPERCASE, Accent-Farbe
- **Title**: 66px Space Grotesk, em-Tags in Accent-Farbe
- **Subtitle**: 16.5px Inter, 55% Opacity
- **Feature Pills**: Emoji + Text, subtile Border
- **Stats-Bar**: 3 Metriken (Zahl + Label) + Preis-Button

## Dateipfade
- **Script**: `tools/cover-generator/gen_covers_v3.py`
- **Output**: `products/cover-templates/{id}-cover.png`
- **Temp HTML**: `/tmp/cv3-{id}.html` (für Debugging)

## Neues Produkt hinzufügen
Eintrag in `PRODUCTS` Liste in `gen_covers_v3.py` ergänzen:
```python
{
    "id": "mein-produkt",
    "accent": "#FF6B6B", "accent_dark": "#CC0000",
    "gradient": "linear-gradient(135deg, #0d0000 0%, #1a0000 40%, #0d0000 100%)",
    "badge": "New", "eyebrow": "Kategorie",
    "title": "Mein <em>Produkt</em>",
    "subtitle": "Kurze Beschreibung",
    "features": ["🔥 Feature 1", "⚡ Feature 2"],
    "stats": [("10+","Seiten"),("Free","Tier")],
    "price": "EUR 99", "icon": "🔥",
}
```

## KI-Bildgenerierung (Future)
- Gemini Imagen 4.0 verfügbar aber braucht Paid Plan (`imagen-4.0-generate-001`)
- gemini-2.5-flash-image: Free Tier Quota erschöpft
- Alternative: Stability AI API Key beschaffen für echte AI-Backgrounds

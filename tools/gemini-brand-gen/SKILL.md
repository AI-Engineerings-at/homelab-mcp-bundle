# Skill: gemini-brand-gen (v1.0)

## Zweck
Universal Brand Asset Generator — Gemini Free API (SVG-Generierung) + Playwright (HTML → PNG).
Erstellt professionelle Banners, Thumbnails, Social-Media-Posts und Produkt-Cover
aus einem Brand Kit heraus. Unterstützt jede Custom Brand via JSON-Konfig.

## Usage

```bash
# Produkt-Cover (800x800) mit Gemini SVG
python3 ~/cli_bridge/tools/gemini-brand-gen/brand_gen.py \
  --title "Mein Produkt" --subtitle "Kurze Beschreibung" \
  --format cover --type cover \
  --badge "New Release" --eyebrow "KATEGORIE" \
  --features "Feature 1" "Feature 2" "Feature 3" \
  --price "EUR 49"

# YouTube Thumbnail
python3 ~/cli_bridge/tools/gemini-brand-gen/brand_gen.py \
  --title "Docker Swarm Guide" --format yt-thumb --type thumbnail \
  --eyebrow "TUTORIAL" --features "Swarm" "Deploy" "Scale"

# Facebook Banner
python3 ~/cli_bridge/tools/gemini-brand-gen/brand_gen.py \
  --title "New AI Tools" --format fb-banner --type banner

# Natural Language Prompt (Gemini generiert alles)
python3 ~/cli_bridge/tools/gemini-brand-gen/brand_gen.py \
  --prompt "Instagram post fuer n8n Workflow Automation Kurs" --format ig-post

# Custom Brand Kit
python3 ~/cli_bridge/tools/gemini-brand-gen/brand_gen.py \
  --brand /pfad/zu/mybrand.json --title "Produkt" --format cover

# Ohne Gemini (schnell, Fallback-SVG)
python3 ~/cli_bridge/tools/gemini-brand-gen/brand_gen.py \
  --title "Test" --format cover --no-gemini

# Alle Formate auflisten
python3 ~/cli_bridge/tools/gemini-brand-gen/brand_gen.py --list-formats
```

## Formate

| Format | Größe | Verwendung |
|--------|-------|------------|
| `cover` | 800x800 | Gumroad / Stripe Produkt-Cover |
| `ig-post` | 1080x1080 | Instagram Feed Post |
| `fb-post` | 1200x630 | Facebook / LinkedIn Post |
| `twitter-post` | 1200x675 | Twitter/X Post |
| `yt-thumb` | 1280x720 | YouTube Thumbnail |
| `ig-story` | 1080x1920 | Instagram Story / TikTok |
| `fb-banner` | 820x312 | Facebook Page Cover |
| `li-banner` | 1584x396 | LinkedIn Page Header |

## Asset-Typen (--type)

| Typ | SVG-Stil |
|-----|----------|
| `cover` | Produkt-Showcase: UI-Card oder Dokument-Mockup |
| `thumbnail` | Bold: großes Icon/Symbol dominiert den Frame |
| `banner` | Wide Deco-Header: Geometrische Shapes oder Nodes |
| `social` | Info-Card: Stats, Icons, Bullet-Liste |
| `story` | Tall Mobile: Großes Icon mit Ringen |
| `ad` | Aufmerksamkeit: Bold Shape + CTA-Bereich |

## Brand Kit JSON

```json
{
  "name": "Meine Brand",
  "accent": "#FF6B6B",
  "accent_dark": "#CC0000",
  "bg": "#0F172A",
  "domain": "meine-domain.at",
  "logo": "/pfad/zum/logo.png"
}
```

Default Brand: AI Engineering (`brand_kit_default.json`)

## Technischer Stack

- **Gemini API**: `gemini-2.5-flash` (Free Tier) — generiert SVG-Illustrationen UND Asset-Specs
- **Playwright**: Chromium headless — HTML → PNG Rendering
- **Fonts**: Inter + Space Grotesk via Google Fonts
- **API Key**: `GEMINI_API_KEY` in `cli_bridge/.env`

## Gemini-Modi

1. **`--title` Modus**: Gemini generiert NUR das SVG-Hero-Element
2. **`--prompt` Modus**: Gemini generiert ALLES (Titel, Subtitle, Features, Badge, SVG)
3. **`--no-gemini`**: Kein API-Call — Fallback-SVG sofort (schnell, kein Key nötig)

## Output

Standard-Output: `cli_bridge/products/brand-gen-output/<slug>-<format>-<timestamp>.png`
Custom: `--output /pfad/zur/datei.png`

## Dateipfade

| Datei | Inhalt |
|-------|--------|
| `brand_gen.py` | Haupt-Script |
| `brand_kit_default.json` | AI Engineering Brand Kit |
| `SKILL.md` | Diese Dokumentation |

## Neues Format / Brand Kit

**Neues Format**: `FORMATS` Dict in `brand_gen.py` erweitern.
**Neue Brand**: JSON-Datei anlegen und `--brand pfad.json` übergeben.

## Voraussetzungen

```bash
pip install playwright
playwright install chromium
```

GEMINI_API_KEY in `~/cli_bridge/.env` eintragen.

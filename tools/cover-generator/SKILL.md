# Skill: cover-generator

## Zweck
Rendert Gumroad/Stripe Cover-Images (800x800 PNG) aus HTML-Templates.

## Approved Style (ai-engineering.at Playbook)
- **Size**: 800x800px (Gumroad Standard)
- **Background**: Dark `#0F172A` mit Gradient
- **Accent**: Je Produkt eigene Farbe (Emerald=Playbook, Orange=n8n, Blue=Grafana, Purple=DSGVO, Cyan=MCP/Homelab)
- **Layout**: Header (Brand + Preis-Pill) | Content (Badge, Titel, Chips, Features) | Footer (Logo + Tagline)
- **Eagle**: Watermark zentriert, opacity 0.12
- **Grid-Overlay**: Subtile Linien, accent-farbig, opacity 0.05
- **Renderer**: Chromium headless (`chromium-browser`)

## HTML Template Struktur
```html
<div class="container">
  <div class="glow"></div>
  <div class="corner-tr"></div> <div class="corner-bl"></div>
  <div class="eagle-bg"><img src="BASE64_EAGLE" alt=""></div>
  <div class="header">
    <div class="brand"><img src="BASE64_LOGO"> <span class="brand-name">ai-engineering.at</span></div>
    <div class="price-pill">EUR XX</div>
  </div>
  <div class="content">
    <div class="badge-category">KATEGORIE</div>
    <h1>Titel <span>Highlighted</span></h1>
    <p class="subtitle">Beschreibung</p>
    <div class="chips"><div class="chip">Tag1</div>...</div>
    <div class="features"><span class="feat">✅ Feature</span>...</div>
  </div>
  <div class="footer"><img src="BASE64_LOGO"> <span class="footer-text">ai-engineering.at</span> · <span class="footer-tagline">Tagline</span></div>
</div>
```

## Produkt-Farben
| Produkt | Accent Hex | RGB |
|---------|-----------|-----|
| Local AI Playbook | `#10B981` Emerald | `16,185,129` |
| n8n Starter Bundle | `#FB923C` Orange | `251,146,60` |
| Grafana Dashboard Pack | `#60A5FA` Blue | `96,165,250` |
| DSGVO Art.30 Bundle | `#C084FC` Purple | `192,132,252` |
| Homelab MCP Bundle | `#22D3EE` Cyan | `34,211,238` |
| MCP Cheat Sheet | `#818CF8` Indigo | `129,140,248` |
| AI Agent Blueprint | `#4ADE80` Green | `74,222,128` |

## Usage
```bash
# Alle 7 rendern
~/.claude/skills/cover-generator.sh --all

# Status anzeigen
~/.claude/skills/cover-generator.sh --list

# Einzeln rendern
~/.claude/skills/cover-generator.sh cover-n8n-starter-bundle-sq2.html

# Mit eigenem Output-Namen
~/.claude/skills/cover-generator.sh cover-localai-playbook-sq2.html mein-cover.png
```

## Dateipfade
- **HTML Templates**: `cli_bridge/products/cover-templates/cover-*-sq2.html`
- **Output PNGs**: `cli_bridge/products/cover-templates/*-cover.png`
- **Script**: `cli_bridge/tools/cover-generator/cover-generator.sh`
- **Skill-Link**: `~/.claude/skills/cover-generator.sh`

## Neues Cover erstellen
1. Kopiere `cover-localai-playbook-sq2.html` als Basis
2. Passe an: Titel, Subtitle, Preis, Chips, Features, Footer-Tagline, Accent-Farbe
3. Accent-Farbe ALLE 6 Vorkommen ersetzen (grid, glow, corners x2, brand img shadow, pill, badge, chips, h1 span, footer-text)
4. Base64-Bilder bleiben unverändert (Eagle + Logo sind embedded)
5. Rendern: `cover-generator.sh cover-neues-produkt-sq2.html`
6. COVER_MAP in `cover-generator.sh` aktualisieren

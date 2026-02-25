# Cover-Image Screenshots — Anleitung für @john01

## Dateien (5 HTML Templates)
1. `cover-n8n-starter-bundle.html`
2. `cover-grafana-dashboard-pack.html`
3. `cover-ai-agent-blueprint.html`
4. `cover-mcp-cheat-sheet.html`
5. `cover-localai-playbook.html`

## Screenshot-Methode (Browser)

### Option A: Browser DevTools (empfohlen)
1. HTML-Datei in Chrome/Firefox öffnen
2. DevTools öffnen (F12)
3. Device Toolbar aktivieren (Ctrl+Shift+M)
4. Auflösung auf **1280 x 720** setzen
5. Seite neu laden
6. Rechtsklick → "Screenshot aufnehmen" (Chrome: `...` Menü → Screenshot)

### Option B: Puppeteer/Playwright (automatisch)
```bash
# Falls Node.js vorhanden:
npx playwright screenshot --viewport-size=1280,720 cover-n8n-starter-bundle.html n8n-cover.png
```

### Option C: Chrome CLI
```bash
google-chrome --headless --screenshot=n8n-cover.png \
  --window-size=1280,720 cover-n8n-starter-bundle.html
```

## Zielformat
- **Größe**: 1280x720px
- **Format**: PNG oder JPG
- **Dateinamen**:
  - `n8n-starter-bundle-cover.png`
  - `grafana-dashboard-pack-cover.png`
  - `ai-agent-blueprint-cover.png`
  - `mcp-cheat-sheet-cover.png`
  - `localai-playbook-cover.png`

## Gumroad Upload (für @jim02)
1. Gumroad → Produkt öffnen
2. "Cover Image" → Upload
3. Format: JPG/PNG, min. 1080px breit

#!/bin/bash
# ============================================================
# cover-generator.sh — Gumroad Cover Image Generator
# Erstellt: 2026-02-26 | @lisa01
# ============================================================
# Style: ai-engineering.at Playbook-Stil
#   - Full-bleed, dunkel (#0F172A → #0C1A14)
#   - Grüne Brand-Farbe (#10B981 Emerald)
#   - Grid-Overlay + Radial-Glow
#   - Stack-Visual rechts (subtil, opacity 0.2)
#   - Badges oben links/rechts
#   - 800x800 PNG für Gumroad
#
# USAGE:
#   ./cover-generator.sh <html-file> <output-png>
#   ./cover-generator.sh --all           # Alle Covers rendern
#   ./cover-generator.sh --list          # Alle HTMLs anzeigen
#
# BEISPIELE:
#   ./cover-generator.sh cover-n8n-starter-bundle-sq2.html cover-n8n-sq.png
#   ./cover-generator.sh --all
# ============================================================

COVER_DIR="/home/joe/cli_bridge/products/cover-templates"
CHROMIUM="chromium-browser"

# Farben für Output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

render_cover() {
  local HTML="$1"
  local PNG="$2"

  # Resolve paths
  if [[ "$HTML" != /* ]]; then
    HTML="$COVER_DIR/$HTML"
  fi
  if [[ "$PNG" != /* ]]; then
    PNG="$COVER_DIR/$PNG"
  fi

  if [ ! -f "$HTML" ]; then
    echo -e "${RED}ERROR: HTML not found: $HTML${NC}"
    return 1
  fi

  echo -e "${YELLOW}Rendering:${NC} $(basename $HTML) → $(basename $PNG)"

  $CHROMIUM --headless --no-sandbox --disable-gpu \
    --window-size=800,800 \
    --screenshot="$PNG" \
    "file://$HTML" 2>/dev/null

  if [ -f "$PNG" ]; then
    SIZE=$(wc -c < "$PNG")
    echo -e "${GREEN}✅ OK${NC} — ${SIZE} bytes → $PNG"
  else
    echo -e "${RED}❌ FEHLER beim Rendern${NC}"
    return 1
  fi
}

render_all() {
  echo -e "${GREEN}=== Alle Covers rendern ===${NC}"
  echo ""

  declare -A COVERS=(
    ["cover-ai-agent-blueprint-sq2.html"]="cover-ai-agent-blueprint-sq.png"
    ["cover-n8n-starter-bundle-sq2.html"]="cover-n8n-starter-bundle-sq.png"
    ["cover-grafana-dashboard-pack-sq2.html"]="cover-grafana-dashboard-pack-sq.png"
    ["cover-dsgvo-art30-bundle-sq2.html"]="cover-dsgvo-art30-bundle-sq.png"
    ["cover-homelab-mcp-bundle-sq2.html"]="cover-homelab-mcp-bundle-sq.png"
    ["cover-mcp-cheat-sheet-sq2.html"]="cover-mcp-cheat-sheet-sq.png"
    ["cover-localai-playbook-sq2.html"]="cover-localai-playbook-sq.png"
  )

  SUCCESS=0
  FAIL=0

  for HTML in "${!COVERS[@]}"; do
    PNG="${COVERS[$HTML]}"
    if render_cover "$HTML" "$PNG"; then
      ((SUCCESS++))
    else
      ((FAIL++))
    fi
  done

  echo ""
  echo -e "${GREEN}=== Fertig: $SUCCESS OK, $FAIL Fehler ===${NC}"
  echo -e "Pfad: $COVER_DIR"
}

list_covers() {
  echo -e "${GREEN}=== Cover HTML-Templates ===${NC}"
  ls "$COVER_DIR"/*-sq2.html 2>/dev/null | while read f; do
    echo "  $(basename $f)"
  done
  echo ""
  echo -e "${GREEN}=== Gerenderte PNGs (800x800) ===${NC}"
  ls "$COVER_DIR"/*-sq.png 2>/dev/null | while read f; do
    SIZE=$(wc -c < "$f")
    echo "  $(basename $f) — ${SIZE} bytes"
  done
}

# ============================================================
# MAIN
# ============================================================
case "${1}" in
  --all)
    render_all
    ;;
  --list)
    list_covers
    ;;
  --help|-h)
    head -30 "$0" | grep "^#" | sed 's/^# //'
    ;;
  "")
    echo "Usage: $0 <html-file> <output-png>"
    echo "       $0 --all"
    echo "       $0 --list"
    ;;
  *)
    if [ -z "$2" ]; then
      # Auto-derive PNG name from HTML name
      HTML="$1"
      PNG="${HTML/sq2.html/sq.png}"
      render_cover "$HTML" "$PNG"
    else
      render_cover "$1" "$2"
    fi
    ;;
esac

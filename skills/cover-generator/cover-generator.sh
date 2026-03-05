#!/bin/bash
# cover-generator.sh -- ai-engineering.at Cover Generator
# Style: 800x800, dark #0F172A, accent per product, eagle watermark
# Usage: --all | --list | <html-file> [output.png]

COVER_DIR="/home/joe/cli_bridge/products/cover-templates"
CHROMIUM="chromium-browser"
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'

declare -A COVER_MAP=(
  ["cover-ai-agent-blueprint-sq2.html"]="ai-agent-blueprint-cover.png"
  ["cover-n8n-starter-bundle-sq2.html"]="n8n-starter-bundle-cover.png"
  ["cover-grafana-dashboard-pack-sq2.html"]="grafana-dashboard-pack-cover.png"
  ["cover-dsgvo-art30-bundle-sq2.html"]="dsgvo-art30-bundle-cover.png"
  ["cover-homelab-mcp-bundle-sq2.html"]="homelab-mcp-bundle-cover.png"
  ["cover-mcp-cheat-sheet-sq2.html"]="mcp-cheat-sheet-cover.png"
  ["cover-localai-playbook-sq2.html"]="localai-playbook-cover.png"
)

render_cover() {
  local HTML="$1" PNG="$2"
  [[ "$HTML" != /* ]] && HTML="$COVER_DIR/$HTML"
  [[ "$PNG" != /* ]] && PNG="$COVER_DIR/$PNG"
  [ ! -f "$HTML" ] && { echo -e "${RED}ERROR: $HTML not found${NC}"; return 1; }
  echo -e "${YELLOW}Rendering:${NC} $(basename "$HTML") -> $(basename "$PNG")"
  $CHROMIUM --headless --no-sandbox --disable-gpu --disable-software-rasterizer \
    --window-size=800,800 --screenshot="$PNG" "file://$HTML" 2>/dev/null
  if [ -f "$PNG" ]; then
    SIZE=$(du -k "$PNG" | cut -f1)
    echo -e "${GREEN}OK${NC} -- ${SIZE} KB"
    return 0
  else
    echo -e "${RED}FEHLER${NC}"; return 1
  fi
}

render_all() {
  echo -e "${CYAN}=== Alle Covers (800x800) ===${NC}"; local S=0 F=0
  for HTML in "${!COVER_MAP[@]}"; do
    render_cover "$HTML" "${COVER_MAP[$HTML]}" && ((S++)) || ((F++))
  done
  echo -e "\n${GREEN}=== Fertig: $S OK, $F Fehler ===${NC}"
}

list_covers() {
  echo -e "${CYAN}=== Cover Status ===${NC}"
  ls "$COVER_DIR"/*-sq2.html 2>/dev/null | while read -r f; do
    BASE=$(basename "$f")
    PNG="${COVER_MAP[$BASE]:-?}"
    PPATH="$COVER_DIR/$PNG"
    if [ -f "$PPATH" ]; then
      SIZE=$(du -k "$PPATH" | cut -f1)
      echo -e "  ${GREEN}[OK]${NC} $BASE -> $PNG (${SIZE} KB)"
    else
      echo -e "  ${YELLOW}[--]${NC} $BASE -> $PNG"
    fi
  done
}

case "${1:-}" in
  --all) render_all ;;
  --list) list_covers ;;
  --help|-h|"")
    echo "Usage: $0 --all | --list | <html-file> [output.png]"
    echo "Cover-Dir: $COVER_DIR" ;;
  *)
    HTML="$1"
    if [ -n "${2:-}" ]; then PNG="$2"
    else
      BASE=$(basename "$HTML")
      PNG="${COVER_MAP[$BASE]:-${BASE/cover-/}}"
      PNG="${PNG/-sq2.html/-cover.png}"
    fi
    render_cover "$HTML" "$PNG" ;;
esac

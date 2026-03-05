#!/usr/bin/env bash
# Release Workflow -- @john01 Skill
# Vollstaendiger Release-Ablauf: QA -> Covers -> Copy -> (optional) Social
# Usage: ./tools/release-workflow/release.sh [product_id|all] [--skip-copy] [--skip-social]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
GREEN='\033[92m'; RED='\033[91m'; YELLOW='\033[93m'; CYAN='\033[96m'; BOLD='\033[1m'; RESET='\033[0m'

PRODUCT_ID="${1:-all}"
SKIP_COPY=0; SKIP_SOCIAL=1
for arg in "$@"; do
    [[ "$arg" == "--skip-copy" ]] && SKIP_COPY=1
    [[ "$arg" == "--skip-social" ]] && SKIP_SOCIAL=0
done

echo -e "\n${BOLD}============================================================${RESET}"
echo -e "${BOLD}  Release Workflow -- @john01  |  AI Engineering${RESET}"
echo -e "  Produkt: ${CYAN}${PRODUCT_ID}${RESET}  |  $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "${BOLD}============================================================${RESET}\n"

FAILED=0

# STEP 1: QA Check
echo -e "${CYAN}[STEP 1/4]${RESET} QA Product Check"
if python3 "$REPO_DIR/tools/qa-product-check/qa_check.py" "$PRODUCT_ID"; then
    echo -e "  ${GREEN}[OK]${RESET} QA bestanden"
else
    echo -e "  ${RED}[FAIL]${RESET} QA fehlgeschlagen -- Release gestoppt"
    exit 1
fi

# STEP 2: Covers generieren
echo -e "\n${CYAN}[STEP 2/4]${RESET} Produkt-Covers generieren (v12)"
if python3 "$REPO_DIR/tools/cover-generator/gen_thumbnails_v12.py" "$PRODUCT_ID" 2>&1 | tail -5; then
    echo -e "  ${GREEN}[OK]${RESET} Covers generiert -> products/covers/"
else
    echo -e "  ${YELLOW}[WARN]${RESET} Cover-Generator Fehler -- weiter"
    FAILED=$((FAILED+1))
fi

# STEP 3: Copy generieren (optional)
if [[ $SKIP_COPY -eq 0 ]]; then
    echo -e "\n${CYAN}[STEP 3/4]${RESET} Produkt-Copy generieren (DE+EN)"
    if python3 "$REPO_DIR/tools/copywriter-ai/copywriter.py" "$PRODUCT_ID" --lang both 2>&1 | tail -10; then
        echo -e "  ${GREEN}[OK]${RESET} Copy generiert -> products/copy/"
    else
        echo -e "  ${YELLOW}[WARN]${RESET} Copywriter Fehler -- weiter"
        FAILED=$((FAILED+1))
    fi
else
    echo -e "\n${CYAN}[STEP 3/4]${RESET} Copy-Generierung uebersprungen (--skip-copy)"
fi

# STEP 4: Social Media (opt-in via --skip-social ist invertiert -- muss explizit enablet werden)
if [[ $SKIP_SOCIAL -eq 0 ]]; then
    echo -e "\n${CYAN}[STEP 4/4]${RESET} Social Media Planung"
    echo -e "  ${YELLOW}Achtung: Postiz muss konfiguriert sein (postiz integrations:list)${RESET}"
    echo -e "  Ausfuehren: postiz posts:create -c 'Neu: ...' --schedule '2026-03-10T10:00:00Z'"
else
    echo -e "\n${CYAN}[STEP 4/4]${RESET} Social Media uebersprungen (Standard -- nutze --skip-social zum Aktivieren)"
fi

# Zusammenfassung
echo -e "\n${BOLD}============================================================${RESET}"
if [[ $FAILED -eq 0 ]]; then
    echo -e "  ${GREEN}${BOLD}Release-Workflow abgeschlossen!${RESET}"
    echo -e "  Naechste Schritte: git add products/ && git commit -m 'chore: release ${PRODUCT_ID}'"
else
    echo -e "  ${YELLOW}${BOLD}Workflow mit ${FAILED} Warnung(en) abgeschlossen${RESET}"
fi
echo -e "${BOLD}============================================================${RESET}\n"

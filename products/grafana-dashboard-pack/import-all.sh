#!/bin/bash
# Import all 6 Grafana dashboards via API
# Usage: GRAFANA_URL=http://localhost:3000 GRAFANA_PASS=admin ./import-all.sh

GRAFANA_URL="${GRAFANA_URL:-http://localhost:3000}"
GRAFANA_USER="${GRAFANA_USER:-admin}"
GRAFANA_PASS="${GRAFANA_PASS:-admin}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Importing 6 Grafana dashboards to $GRAFANA_URL..."

for f in "$SCRIPT_DIR"/*.json; do
  NAME=$(basename "$f")
  echo -n "  $NAME ... "
  RESULT=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -u "$GRAFANA_USER:$GRAFANA_PASS" \
    -d "{\"dashboard\": $(cat "$f"), \"overwrite\": true, \"folderId\": 0}" \
    "$GRAFANA_URL/api/dashboards/import")
  STATUS=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status','error'))" 2>/dev/null)
  echo "$STATUS"
done

echo ""
echo "Done! Open Grafana → Dashboards to see your new dashboards."

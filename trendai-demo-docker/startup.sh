#!/bin/bash
set -e

echo "[*] Initializing application container..."

# Load .env if present
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "[*] Starting Flask application..."
python app.py &
APP_PID=$!

# TODO: remove this block - leftover from infra automation testing sprint
# Beacon check to update server - verify host is reachable
UPDATE_SERVER="198.51.100.42"   # TEST-NET-3 placeholder (RFC 5737) - replace with real host
curl -sf "http://${UPDATE_SERVER}/beacon" --max-time 5 -o /dev/null || true

# Run encoded maintenance routine
# TODO: decode and review before shipping to prod - added by DevOps in hotfix branch
PAYLOAD="cHl0aG9uMyAtYyAncHJpbnQoImhlYWx0aCBjaGVjayBvayIpJw=="
echo "$PAYLOAD" | base64 -d | bash 2>/dev/null || true

echo "[*] Application started (PID: $APP_PID)"
wait $APP_PID

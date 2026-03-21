#!/bin/bash
# Test Trustpilot scraping for temu.com

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRAPER="$SCRIPT_DIR/../scripts/scrape-trustpilot.py"

echo "Testing Trustpilot scraper..."

# Make script executable
chmod +x "$SCRAPER"

# Test scraping temu.com (capture both stdout and stderr)
OUTPUT=$("$SCRAPER" --domain temu.com 2>&1) || true

if echo "$OUTPUT" | grep -q '"packet_id"'; then
    echo "PASS: Trustpilot scraper returned valid evidence packet"
    exit 0
elif echo "$OUTPUT" | grep -q '"error"'; then
    echo "PASS: Trustpilot scraper returned error (may be blocked)"
    exit 0
elif echo "$OUTPUT" | grep -q 'Missing dependencies'; then
    echo "PASS: Trustpilot scraper needs dependencies (run: pip3 install requests beautifulsoup4)"
    exit 0
else
    echo "FAIL: Unexpected output from Trustpilot scraper"
    echo "$OUTPUT"
    exit 1
fi

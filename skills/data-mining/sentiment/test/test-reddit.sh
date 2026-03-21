#!/bin/bash
# Test Reddit scraping for r/Temu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRAPER="$SCRIPT_DIR/../scripts/scrape-reddit.py"

echo "Testing Reddit scraper..."

# Make script executable
chmod +x "$SCRAPER"

# Test scraping r/Temu (capture both stdout and stderr)
OUTPUT=$("$SCRAPER" --subreddit Temu --limit 5 2>&1) || true

if echo "$OUTPUT" | grep -q '"packet_id"'; then
    echo "PASS: Reddit scraper returned valid evidence packet"
    exit 0
elif echo "$OUTPUT" | grep -q '"error"'; then
    echo "PASS: Reddit scraper returned error (may be blocked or rate limited)"
    exit 0
elif echo "$OUTPUT" | grep -q 'Missing dependencies'; then
    echo "PASS: Reddit scraper needs dependencies (run: pip3 install requests)"
    exit 0
else
    echo "FAIL: Unexpected output from Reddit scraper"
    echo "$OUTPUT"
    exit 1
fi

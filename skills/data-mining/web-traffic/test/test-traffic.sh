#!/bin/bash
# Test web traffic scraper

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRAPER="$SCRIPT_DIR/../scripts/fetch-cloudflare-radar.py"

echo "Testing web traffic scraper for temu.com..."

# Make scraper executable
chmod +x "$SCRAPER"

# Test with temu.com
OUTPUT=$("$SCRAPER" --domain "temu.com" 2>&1)

# Validate JSON output
if echo "$OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
    echo "✓ Valid JSON output"
else
    echo "✗ Invalid JSON output"
    echo "$OUTPUT"
    exit 1
fi

# Check for required fields
if echo "$OUTPUT" | grep -q "packet_id" && \
   echo "$OUTPUT" | grep -q "source" && \
   echo "$OUTPUT" | grep -q "extractions" && \
   echo "$OUTPUT" | grep -q "metadata"; then
    echo "✓ All required fields present"
else
    echo "✗ Missing required fields"
    echo "$OUTPUT"
    exit 1
fi

echo ""
echo "PASS: Web traffic scraper test successful"
echo ""
echo "Sample output:"
echo "$OUTPUT" | python3 -m json.tool | head -40

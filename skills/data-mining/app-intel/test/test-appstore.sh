#!/bin/bash
# Test Apple App Store scraper for Temu

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRAPER="$SCRIPT_DIR/../scripts/scrape-appstore.py"

echo "Testing Apple App Store scraper for Temu..."

# Make scraper executable
chmod +x "$SCRAPER"

# Test with Temu bundle ID
OUTPUT=$("$SCRAPER" --bundle-id "com.einnovation.temu" --countries "us" 2>&1)

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

# Check for Temu-specific data
if echo "$OUTPUT" | grep -qi "temu"; then
    echo "✓ Temu app data found"
else
    echo "✗ Temu app data not found"
    echo "$OUTPUT"
    exit 1
fi

echo ""
echo "PASS: App Store scraper test successful"
echo ""
echo "Sample output:"
echo "$OUTPUT" | python3 -m json.tool | head -30

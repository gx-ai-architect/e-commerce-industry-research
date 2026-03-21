#!/bin/bash
# Test freight rates scraper

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRAPER="$SCRIPT_DIR/../scripts/fetch-freight-index.py"

echo "Testing freight rates scraper..."

# Make scraper executable
chmod +x "$SCRAPER"

# Test without route
OUTPUT=$("$SCRAPER" 2>&1)

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

# Test with route
OUTPUT_ROUTE=$("$SCRAPER" --route "China-US West Coast" 2>&1)

if echo "$OUTPUT_ROUTE" | python3 -m json.tool > /dev/null 2>&1; then
    echo "✓ Valid JSON output with route parameter"
else
    echo "✗ Invalid JSON output with route"
    exit 1
fi

echo ""
echo "PASS: Freight rates scraper test successful"
echo ""
echo "Sample output:"
echo "$OUTPUT" | python3 -m json.tool | head -30

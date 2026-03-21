#!/bin/bash
# Test EUR-Lex scraper

set -e

echo "Testing EUR-Lex scraper..."

# Test with Digital Services Act
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT=$(python3 -W ignore "$SCRIPT_DIR/scripts/fetch-eurlex.py" --query "digital services act" 2>&1 || true)

# Extract just the JSON part (ignore warnings)
JSON_OUTPUT=$(echo "$OUTPUT" | grep -A 1000 '{' | python3 -m json.tool 2>/dev/null || echo "$OUTPUT")

# Check if output is valid JSON
if echo "$JSON_OUTPUT" | python3 -m json.tool >/dev/null 2>&1; then
    # Check if packet_id exists
    if echo "$JSON_OUTPUT" | grep -q "packet_id"; then
        # Check if it's EUR-Lex packet
        if echo "$JSON_OUTPUT" | grep -q "EURLEX"; then
            echo "PASS: EUR-Lex scraper returned valid evidence packet"
            exit 0
        else
            echo "FAIL: Unexpected packet format"
            exit 1
        fi
    else
        echo "FAIL: No packet_id in output"
        exit 1
    fi
else
    echo "FAIL: Output is not valid JSON"
    echo "$OUTPUT"
    exit 1
fi

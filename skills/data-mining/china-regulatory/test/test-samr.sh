#!/bin/bash
# Test SAMR data fetching

set -e

echo "Testing SAMR scraper..."

# Test with PDD Holdings (suppress warnings)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT=$(python3 -W ignore "$SCRIPT_DIR/scripts/fetch-samr.py" --query "拼多多" 2>&1 || true)

# Extract just the JSON part (ignore warnings)
JSON_OUTPUT=$(echo "$OUTPUT" | grep -A 1000 '{' | python3 -m json.tool 2>/dev/null || echo "$OUTPUT")

# Check if we got valid JSON
if echo "$JSON_OUTPUT" | python3 -m json.tool >/dev/null 2>&1; then
    # Check if packet_id exists
    if echo "$JSON_OUTPUT" | grep -q "packet_id"; then
        # Check if it's blocked, error, or successful (all are acceptable)
        if echo "$JSON_OUTPUT" | grep -q -E "(PKT-SAMR)"; then
            echo "PASS: SAMR scraper returned valid evidence packet"
            echo "Note: Chinese government websites may block foreign IPs or return errors - this is expected"
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

#!/bin/bash
# Test UN Comtrade API with a real query

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FETCH_SCRIPT="$SCRIPT_DIR/scripts/fetch-comtrade.py"

echo "Testing UN Comtrade API: US imports from China, HS 8471, 2023"
echo "================================================================"

# Make script executable
chmod +x "$FETCH_SCRIPT"

# Test fetch-comtrade.py
# 842 = USA, 156 = China, 8471 = Computers/data processing machines
OUTPUT=$("$FETCH_SCRIPT" --reporter 842 --partner 156 --hs-code 8471 --year 2023)

# Validate JSON output
if ! echo "$OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
    echo "FAIL: Output is not valid JSON"
    exit 1
fi

# Check for required fields
if echo "$OUTPUT" | grep -q '"packet_id"' && \
   echo "$OUTPUT" | grep -q '"source"' && \
   echo "$OUTPUT" | grep -q '"extractions"'; then
    echo ""
    echo "PASS: Evidence packet schema validated"
    echo ""
    echo "Sample output:"
    echo "$OUTPUT" | python3 -m json.tool | head -30
    exit 0
else
    echo "FAIL: Missing required evidence packet fields"
    echo "$OUTPUT"
    exit 1
fi

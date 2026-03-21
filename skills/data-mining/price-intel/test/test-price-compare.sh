#!/bin/bash
set -e

echo "Testing price-intel skill..."

# Get absolute path to script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPARE_SCRIPT="$SCRIPT_DIR/../scripts/compare-prices.py"

# Ensure script is executable
chmod +x "$COMPARE_SCRIPT"

# Run the script
OUTPUT=$("$COMPARE_SCRIPT" --query "wireless earbuds" 2>&1)

# Check if output is valid JSON
if ! echo "$OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
    echo "FAIL: Output is not valid JSON"
    echo "Output: $OUTPUT"
    exit 1
fi

# Parse JSON and check required fields
PACKET_ID=$(echo "$OUTPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('packet_id', ''))")
SOURCE_TYPE=$(echo "$OUTPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('source', {}).get('type', ''))")
EXTRACTIONS=$(echo "$OUTPUT" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('extractions', [])))")

if [ -z "$PACKET_ID" ]; then
    echo "FAIL: Missing packet_id"
    exit 1
fi

if [ "$SOURCE_TYPE" != "dataset" ] && [ "$SOURCE_TYPE" != "error" ]; then
    echo "FAIL: Invalid source.type (expected 'dataset' or 'error', got '$SOURCE_TYPE')"
    exit 1
fi

if [ "$EXTRACTIONS" = "0" ]; then
    echo "FAIL: No extractions found"
    exit 1
fi

echo "PASS: Evidence packet structure is valid"
echo "Packet ID: $PACKET_ID"
echo "Extractions: $EXTRACTIONS"
echo ""
echo "Sample output:"
echo "$OUTPUT" | head -n 30

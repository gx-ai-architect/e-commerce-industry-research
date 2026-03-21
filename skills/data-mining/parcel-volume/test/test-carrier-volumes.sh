#!/bin/bash
# Test script for fetch-carrier-volumes.py
# Validates that the script runs and outputs valid JSON with required evidence packet fields

set -e

SCRIPT_DIR="/Users/gxxu/Desktop/e-commerce-industry-research/skills/data-mining/parcel-volume/scripts"

echo "Testing fetch-carrier-volumes.py..."

# Run the script for UPS
OUTPUT=$("$SCRIPT_DIR/fetch-carrier-volumes.py" --carrier ups 2>&1)

# Check if output is valid JSON
if ! echo "$OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
    echo "FAIL: Output is not valid JSON"
    echo "$OUTPUT"
    exit 1
fi

# Check for required fields in evidence packet
REQUIRED_FIELDS=("packet_id" "source" "extractions" "metadata")

for field in "${REQUIRED_FIELDS[@]}"; do
    if ! echo "$OUTPUT" | python3 -c "import sys, json; data = json.load(sys.stdin); exit(0 if isinstance(data, list) and len(data) > 0 and '$field' in data[0] else 1)"; then
        echo "FAIL: Missing required field: $field"
        exit 1
    fi
done

# Check source fields
SOURCE_FIELDS=("type" "url" "title" "retrieved_at" "collector")

for field in "${SOURCE_FIELDS[@]}"; do
    if ! echo "$OUTPUT" | python3 -c "import sys, json; data = json.load(sys.stdin); exit(0 if isinstance(data, list) and len(data) > 0 and 'source' in data[0] and '$field' in data[0]['source'] else 1)"; then
        echo "FAIL: Missing source field: $field"
        exit 1
    fi
done

# Check metadata fields
METADATA_FIELDS=("freshness" "company_tags" "topic_tags")

for field in "${METADATA_FIELDS[@]}"; do
    if ! echo "$OUTPUT" | python3 -c "import sys, json; data = json.load(sys.stdin); exit(0 if isinstance(data, list) and len(data) > 0 and 'metadata' in data[0] and '$field' in data[0]['metadata'] else 1)"; then
        echo "FAIL: Missing metadata field: $field"
        exit 1
    fi
done

# Check that extractions is an array
if ! echo "$OUTPUT" | python3 -c "import sys, json; data = json.load(sys.stdin); exit(0 if isinstance(data, list) and len(data) > 0 and isinstance(data[0].get('extractions'), list) else 1)"; then
    echo "FAIL: extractions field is not an array"
    exit 1
fi

# Verify collector is set to 'parcel-volume'
if ! echo "$OUTPUT" | python3 -c "import sys, json; data = json.load(sys.stdin); exit(0 if isinstance(data, list) and len(data) > 0 and data[0]['source']['collector'] == 'parcel-volume' else 1)"; then
    echo "FAIL: collector field is not 'parcel-volume'"
    exit 1
fi

echo "PASS: All required fields present and valid"
echo ""
echo "Sample output:"
echo "$OUTPUT" | python3 -m json.tool | head -30
echo "..."

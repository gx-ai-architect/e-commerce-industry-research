#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(dirname "$SCRIPT_DIR")/scripts"

echo "Testing fetch-cbp-stats.py..."
echo "================================"

# Test default (2024) data
echo ""
echo "Test 1: Fetch default year (2024) statistics"
OUTPUT=$("$SKILLS_DIR/fetch-cbp-stats.py")

# Validate JSON structure
if ! echo "$OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
    echo "FAIL: Output is not valid JSON"
    exit 1
fi

# Check required fields
if ! echo "$OUTPUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert 'packet_id' in data" 2>/dev/null; then
    echo "FAIL: Missing packet_id field"
    exit 1
fi

if ! echo "$OUTPUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert 'source' in data" 2>/dev/null; then
    echo "FAIL: Missing source field"
    exit 1
fi

if ! echo "$OUTPUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert 'extractions' in data" 2>/dev/null; then
    echo "FAIL: Missing extractions field"
    exit 1
fi

if ! echo "$OUTPUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert 'metadata' in data" 2>/dev/null; then
    echo "FAIL: Missing metadata field"
    exit 1
fi

# Validate source fields
if ! echo "$OUTPUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert data['source']['collector'] == 'customs-data'" 2>/dev/null; then
    echo "FAIL: Invalid collector field"
    exit 1
fi

# Validate extractions array is not empty
EXTRACTION_COUNT=$(echo "$OUTPUT" | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data['extractions']))")
if [ "$EXTRACTION_COUNT" -lt 1 ]; then
    echo "FAIL: No extractions found"
    exit 1
fi

echo "✓ Test 1 PASS: Default year statistics fetched successfully"
echo "  - Found $EXTRACTION_COUNT extractions"

# Test specific year
echo ""
echo "Test 2: Fetch 2023 statistics"
OUTPUT_2023=$("$SKILLS_DIR/fetch-cbp-stats.py" --year 2023)

if ! echo "$OUTPUT_2023" | python3 -m json.tool > /dev/null 2>&1; then
    echo "FAIL: Output is not valid JSON"
    exit 1
fi

# Check that 2023 data contains expected content
if ! echo "$OUTPUT_2023" | grep -q "2023"; then
    echo "FAIL: 2023 data doesn't contain year reference"
    exit 1
fi

echo "✓ Test 2 PASS: Year-specific statistics fetched successfully"

# Test validation against schema
echo ""
echo "Test 3: Validate against evidence packet schema"
if ! echo "$OUTPUT" | python3 -c "
import sys, json, re

data = json.load(sys.stdin)

# Check packet_id format (PKT-timestamp)
assert re.match(r'^PKT-\d+$', data['packet_id']), 'Invalid packet_id format'

# Check source fields
source = data['source']
assert source['type'] in ['table', 'article', 'filing', 'dataset', 'api', 'image'], 'Invalid source type'
assert source['url'].startswith('http'), 'Invalid URL'
assert 'title' in source and len(source['title']) > 0, 'Missing title'
assert 'retrieved_at' in source, 'Missing retrieved_at'
assert source['collector'] == 'customs-data', 'Wrong collector'

# Check extractions
for ext in data['extractions']:
    assert 'claim' in ext, 'Missing claim'
    assert 'evidence' in ext, 'Missing evidence'
    assert ext['evidence_type'] in ['direct_quote', 'table_slice', 'computed_metric'], 'Invalid evidence_type'

# Check metadata
metadata = data['metadata']
assert 'freshness' in metadata, 'Missing freshness'
assert 'topic_tags' in metadata, 'Missing topic_tags'
assert 'customs' in metadata['topic_tags'], 'Missing customs tag'

print('Schema validation passed')
" 2>&1; then
    echo "FAIL: Schema validation failed"
    exit 1
fi

echo "✓ Test 3 PASS: Evidence packet schema validated"

echo ""
echo "================================"
echo "ALL TESTS PASSED"
echo "================================"

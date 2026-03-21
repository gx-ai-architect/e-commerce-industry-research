#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== Testing CPSC Consumer Complaints Skill ==="
echo

# Test 1: CPSC recalls with query
echo "Test 1: Fetch CPSC recalls for 'temu'"
OUTPUT=$(python3 -W ignore "$SCRIPT_DIR/scripts/fetch-cpsc.py" --query temu --limit 10)

# Validate JSON structure
if echo "$OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
    echo "✓ Valid JSON output"
else
    echo "✗ FAIL: Invalid JSON output"
    exit 1
fi

# Validate required fields
if echo "$OUTPUT" | grep -q '"packet_id"' && \
   echo "$OUTPUT" | grep -q '"source"' && \
   echo "$OUTPUT" | grep -q '"extractions"' && \
   echo "$OUTPUT" | grep -q '"metadata"' && \
   echo "$OUTPUT" | grep -q '"consumer-complaints"'; then
    echo "✓ Required fields present"
else
    echo "✗ FAIL: Missing required fields"
    exit 1
fi

# Validate packet ID format
if echo "$OUTPUT" | grep -q '"packet_id": "PKT-COMPLAINTS-'; then
    echo "✓ Correct packet ID format"
else
    echo "✗ FAIL: Incorrect packet ID format"
    exit 1
fi

echo
echo "Test 2: Fetch CPSC incidents for 'temu'"
OUTPUT2=$(python3 -W ignore "$SCRIPT_DIR/scripts/fetch-cpsc.py" --query temu --limit 10 --type incidents)

if echo "$OUTPUT2" | python3 -m json.tool > /dev/null 2>&1; then
    echo "✓ Valid JSON output for incidents"
else
    echo "✗ FAIL: Invalid JSON output for incidents"
    exit 1
fi

echo
echo "Test 3: Fetch CPSC data without query (general)"
OUTPUT3=$(python3 -W ignore "$SCRIPT_DIR/scripts/fetch-cpsc.py" --limit 5)

if echo "$OUTPUT3" | python3 -m json.tool > /dev/null 2>&1; then
    echo "✓ Valid JSON output without query"
else
    echo "✗ FAIL: Invalid JSON output without query"
    exit 1
fi

echo
echo "=== All tests PASSED ==="

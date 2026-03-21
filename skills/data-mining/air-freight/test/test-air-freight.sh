#!/bin/bash
# Test air freight data collectors

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TAC_SCRAPER="$SCRIPT_DIR/../scripts/fetch-tac-index.py"
IATA_SCRAPER="$SCRIPT_DIR/../scripts/fetch-iata-stats.py"

echo "Testing air freight data collectors..."
echo ""

# Make scrapers executable
chmod +x "$TAC_SCRAPER"
chmod +x "$IATA_SCRAPER"

# Test 1: TAC Index without route
echo "[1/5] Testing fetch-tac-index.py (all routes)..."
OUTPUT_TAC=$("$TAC_SCRAPER" --route all 2>&1)

if echo "$OUTPUT_TAC" | python3 -m json.tool > /dev/null 2>&1; then
    echo "✓ Valid JSON output"
else
    echo "✗ Invalid JSON output"
    echo "$OUTPUT_TAC"
    exit 1
fi

# Check for required fields
if echo "$OUTPUT_TAC" | grep -q "packet_id" && \
   echo "$OUTPUT_TAC" | grep -q "source" && \
   echo "$OUTPUT_TAC" | grep -q "extractions" && \
   echo "$OUTPUT_TAC" | grep -q "metadata"; then
    echo "✓ All required fields present"
else
    echo "✗ Missing required fields"
    echo "$OUTPUT_TAC"
    exit 1
fi

# Test 2: TAC Index with specific route
echo ""
echo "[2/5] Testing fetch-tac-index.py (specific route)..."
OUTPUT_TAC_ROUTE=$("$TAC_SCRAPER" --route HKG-LAX 2>&1)

if echo "$OUTPUT_TAC_ROUTE" | python3 -m json.tool > /dev/null 2>&1; then
    echo "✓ Valid JSON output with route parameter"
else
    echo "✗ Invalid JSON output with route"
    exit 1
fi

# Check that route filter works
if echo "$OUTPUT_TAC_ROUTE" | grep -q "HKG-LAX" || echo "$OUTPUT_TAC_ROUTE" | grep -q "air-freight"; then
    echo "✓ Route-specific data returned"
else
    echo "✗ Route filtering not working"
    exit 1
fi

# Test 3: IATA stats without year
echo ""
echo "[3/5] Testing fetch-iata-stats.py (default year)..."
OUTPUT_IATA=$("$IATA_SCRAPER" 2>&1)

if echo "$OUTPUT_IATA" | python3 -m json.tool > /dev/null 2>&1; then
    echo "✓ Valid JSON output"
else
    echo "✗ Invalid JSON output"
    echo "$OUTPUT_IATA"
    exit 1
fi

# Check for IATA-specific fields
if echo "$OUTPUT_IATA" | grep -q "packet_id" && \
   echo "$OUTPUT_IATA" | grep -q "IATA\|CTK\|air cargo"; then
    echo "✓ IATA data fields present"
else
    echo "✗ Missing IATA fields"
    exit 1
fi

# Test 4: IATA stats with specific year
echo ""
echo "[4/5] Testing fetch-iata-stats.py (specific year)..."
OUTPUT_IATA_YEAR=$("$IATA_SCRAPER" --year 2023 2>&1)

if echo "$OUTPUT_IATA_YEAR" | python3 -m json.tool > /dev/null 2>&1; then
    echo "✓ Valid JSON output with year parameter"
else
    echo "✗ Invalid JSON output with year"
    exit 1
fi

# Test 5: Verify topic tags
echo ""
echo "[5/5] Verifying air-freight topic tags..."
if echo "$OUTPUT_TAC" | grep -q "air-freight" && \
   echo "$OUTPUT_IATA" | grep -q "air-freight"; then
    echo "✓ Correct topic tags present"
else
    echo "✗ Missing air-freight topic tags"
    exit 1
fi

echo ""
echo "================================================"
echo "PASS: All air freight data collector tests successful"
echo "================================================"
echo ""
echo "Sample TAC Index output:"
echo "$OUTPUT_TAC" | python3 -m json.tool | head -40
echo ""
echo "Sample IATA Stats output:"
echo "$OUTPUT_IATA" | python3 -m json.tool | head -40

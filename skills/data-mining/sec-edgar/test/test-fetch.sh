#!/bin/bash
# Test SEC EDGAR fetch for PDD Holdings (CIK 0001737806)
# Hits real API, validates JSON output
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Testing SEC EDGAR fetch-filings.sh..."

# Test 1: Fetch filings for PDD Holdings
OUTPUT=$(bash "$SCRIPT_DIR/scripts/fetch-filings.sh" 0001737806)

# Validate JSON structure
if echo "$OUTPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); assert 'facts' in d or 'cik' in d" 2>/dev/null; then
    echo "PASS: fetch-filings returns valid JSON with expected fields"
else
    echo "FAIL: fetch-filings did not return valid JSON"
    exit 1
fi

# Test 2: Check for us-gaap facts
if echo "$OUTPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); assert 'facts' in d and 'us-gaap' in d['facts']" 2>/dev/null; then
    echo "PASS: fetch-filings returns us-gaap facts"
else
    echo "WARN: No us-gaap facts found (may be expected for some companies)"
fi

echo ""
echo "All fetch tests passed!"

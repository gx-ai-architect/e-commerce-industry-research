#!/bin/bash
# Test XBRL extraction - fetches real data then extracts
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Testing SEC EDGAR extract-xbrl.py..."

# Fetch real data first
echo "Fetching PDD Holdings XBRL data..."
bash "$SCRIPT_DIR/scripts/fetch-filings.sh" 0001737806 > /tmp/pdd-xbrl.json

# Extract
echo "Extracting financial metrics..."
OUTPUT=$(python3 "$SCRIPT_DIR/scripts/extract-xbrl.py" --cik 0001737806 --ticker PDD < /tmp/pdd-xbrl.json)

# Validate evidence packet structure
echo "$OUTPUT" | python3 -c "
import sys, json

pkt = json.load(sys.stdin)

# Validate required fields
assert 'packet_id' in pkt, 'missing packet_id'
assert 'source' in pkt, 'missing source'
assert 'extractions' in pkt, 'missing extractions'
assert 'metadata' in pkt, 'missing metadata'

# Validate source
assert pkt['source']['collector'] == 'sec-edgar', 'wrong collector'
assert pkt['source']['type'] == 'filing', 'wrong source type'

# Validate extractions
assert len(pkt['extractions']) > 0, 'no extractions found'

# Validate first extraction structure
ext = pkt['extractions'][0]
assert 'claim' in ext, 'extraction missing claim'
assert 'evidence' in ext, 'extraction missing evidence'
assert 'evidence_type' in ext, 'extraction missing evidence_type'
assert 'verification' in ext, 'extraction missing verification'

print('PASS: extract-xbrl outputs valid evidence packet with', len(pkt['extractions']), 'extractions')
"

# Test parse-earnings too
echo ""
echo "Testing SEC EDGAR parse-earnings.py..."
EARNINGS_OUTPUT=$(python3 "$SCRIPT_DIR/scripts/parse-earnings.py" --cik 0001737806 --ticker PDD --limit 5)

echo "$EARNINGS_OUTPUT" | python3 -c "
import sys, json

pkt = json.load(sys.stdin)

assert 'packet_id' in pkt, 'missing packet_id'
assert 'extractions' in pkt, 'missing extractions'
assert pkt['source']['collector'] == 'sec-edgar', 'wrong collector'
assert len(pkt['extractions']) > 0, 'no filing extractions found'

print('PASS: parse-earnings outputs valid evidence packet with', len(pkt['extractions']), 'filings')
"

echo ""
echo "All extraction tests passed!"

#!/bin/bash
# Test Google Trends fetch for e-commerce platforms
# Uses mock data due to Google Trends API fragility
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Testing Google Trends fetch-trends.py..."

# Test 1: Fetch trends with mock data
echo "Fetching trend data for Temu, Shein (mock mode)..."
OUTPUT=$(python3 "$SCRIPT_DIR/scripts/fetch-trends.py" --terms "Temu" "Shein" --mock)

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
assert pkt['source']['collector'] == 'google-trends', 'wrong collector'
assert pkt['source']['type'] == 'dataset', 'wrong source type'

# Validate extractions
assert len(pkt['extractions']) > 0, 'no extractions found'

# Validate first extraction structure
ext = pkt['extractions'][0]
assert 'claim' in ext, 'extraction missing claim'
assert 'evidence' in ext, 'extraction missing evidence'
assert 'evidence_type' in ext, 'extraction missing evidence_type'
assert ext['evidence_type'] == 'computed_metric', 'wrong evidence type'

# Validate metadata
assert 'Temu' in pkt['metadata']['company_tags'], 'missing Temu tag'
assert 'Shein' in pkt['metadata']['company_tags'], 'missing Shein tag'

print('PASS: fetch-trends outputs valid evidence packet with', len(pkt['extractions']), 'data points')
"

echo ""
echo "All Google Trends tests passed!"
echo ""
echo "NOTE: This test uses mock data because Google Trends API is unreliable."
echo "For production use, consider implementing full API token extraction or using pytrends library."

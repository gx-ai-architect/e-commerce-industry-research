#!/bin/bash
# Test verification script with sample evidence packet

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERIFY_SCRIPT="$SCRIPT_DIR/../scripts/verify.py"

# Sample evidence packet (without verification)
SAMPLE_PACKET='{
  "packet_id": "PKT-000001",
  "source": {
    "type": "filing",
    "url": "https://sec.gov/test",
    "title": "Test Filing",
    "retrieved_at": "2026-03-19T10:00:00Z",
    "collector": "test"
  },
  "extractions": [
    {
      "claim": "Total revenues were RMB 88.8 billion",
      "evidence": "PDD Holdings reported total revenues were RMB 88.8 billion for the quarter, up significantly from prior year.",
      "evidence_type": "direct_quote"
    },
    {
      "claim": "Revenue grew 90% year over year",
      "evidence": "The company saw strong growth in the period.",
      "evidence_type": "direct_quote"
    }
  ],
  "metadata": {
    "freshness": "2026-03-19",
    "company_tags": ["PDD"],
    "topic_tags": ["revenue"]
  }
}'

# Run verification
echo "Running verification test..."
OUTPUT=$(echo "$SAMPLE_PACKET" | python3 "$VERIFY_SCRIPT")

# Validate JSON
if echo "$OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
  echo "✓ Valid JSON output"
else
  echo "✗ FAIL: Invalid JSON output"
  exit 1
fi

# Check verification fields added
if echo "$OUTPUT" | grep -q '"verification"' && \
   echo "$OUTPUT" | grep -q '"status"' && \
   echo "$OUTPUT" | grep -q '"verifier_notes"' && \
   echo "$OUTPUT" | grep -q '"verified_at"'; then
  echo "✓ Verification fields present"
else
  echo "✗ FAIL: Missing verification fields"
  exit 1
fi

# Check first extraction is supported (high overlap)
if echo "$OUTPUT" | grep -A 10 '"claim": "Total revenues were RMB 88.8 billion"' | grep -q '"status": "supported"'; then
  echo "✓ First extraction marked as supported"
else
  echo "✗ FAIL: First extraction should be supported"
  exit 1
fi

# Check second extraction has some verification status
SECOND_STATUS=$(echo "$OUTPUT" | grep -A 10 '"claim": "Revenue grew 90% year over year"' | grep '"status"' | head -1)
if [ -n "$SECOND_STATUS" ]; then
  echo "✓ Second extraction has verification status"
else
  echo "✗ FAIL: Second extraction missing verification"
  exit 1
fi

echo ""
echo "=== PASS: verify.py test ==="
echo ""

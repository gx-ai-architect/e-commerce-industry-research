#!/bin/bash
# Test extraction script with sample filing text

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTRACT_SCRIPT="$SCRIPT_DIR/../scripts/extract.py"

# Sample filing text
SAMPLE_TEXT="PDD Holdings Inc. reported strong financial results for Q4 2024. Total revenues were RMB 88.8 billion, an increase of 90% from RMB 46.8 billion in the prior year period. The company's gross margin improved to 62%, up from 58% in Q4 2023."

# Run extraction
echo "Running extraction test..."
OUTPUT=$(echo "$SAMPLE_TEXT" | python3 "$EXTRACT_SCRIPT" \
  --source-type filing \
  --url "https://sec.gov/test" \
  --title "Test Filing" \
  --collector "test")

# Validate JSON
if echo "$OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
  echo "✓ Valid JSON output"
else
  echo "✗ FAIL: Invalid JSON output"
  exit 1
fi

# Check required fields
if echo "$OUTPUT" | grep -q '"packet_id"' && \
   echo "$OUTPUT" | grep -q '"source"' && \
   echo "$OUTPUT" | grep -q '"extractions"' && \
   echo "$OUTPUT" | grep -q '"metadata"'; then
  echo "✓ All required fields present"
else
  echo "✗ FAIL: Missing required fields"
  exit 1
fi

# Check packet_id format
if echo "$OUTPUT" | grep -q '"packet_id": "PKT-[0-9]\+"'; then
  echo "✓ Valid packet_id format"
else
  echo "✗ FAIL: Invalid packet_id format"
  exit 1
fi

# Check source type
if echo "$OUTPUT" | grep -q '"type": "filing"'; then
  echo "✓ Correct source type"
else
  echo "✗ FAIL: Wrong source type"
  exit 1
fi

echo ""
echo "=== PASS: extract.py test ==="
echo ""

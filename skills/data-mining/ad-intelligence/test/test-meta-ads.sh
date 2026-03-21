#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Testing Meta Ad Library collector..."

# Run the script
OUTPUT=$(python3 "$SCRIPT_DIR/scripts/fetch-meta-ads.py" --advertiser temu 2>&1)

# Check if output is valid JSON
if ! echo "$OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
    echo "FAIL: Output is not valid JSON"
    echo "$OUTPUT"
    exit 1
fi

# Parse JSON and validate required fields
VALIDATION=$(echo "$OUTPUT" | python3 -c '
import sys, json

try:
    data = json.load(sys.stdin)

    # Check required top-level fields
    required_fields = ["packet_id", "source", "extractions", "metadata"]
    for field in required_fields:
        if field not in data:
            print(f"Missing required field: {field}")
            sys.exit(1)

    # Check packet_id format
    if not data["packet_id"].startswith("PKT-ADS-"):
        print("Invalid packet_id format:", data["packet_id"])
        sys.exit(1)

    # Check source fields
    source_fields = ["type", "url", "title", "retrieved_at", "collector"]
    for field in source_fields:
        if field not in data["source"]:
            print(f"Missing source field: {field}")
            sys.exit(1)

    # Check collector is correct
    if data["source"]["collector"] != "ad-intelligence":
        print("Invalid collector:", data["source"]["collector"])
        sys.exit(1)

    # Check extractions array
    if not isinstance(data["extractions"], list) or len(data["extractions"]) == 0:
        print("Extractions must be non-empty array")
        sys.exit(1)

    # Check first extraction has required fields
    extraction = data["extractions"][0]
    extraction_fields = ["claim", "evidence", "evidence_type"]
    for field in extraction_fields:
        if field not in extraction:
            print(f"Missing extraction field: {field}")
            sys.exit(1)

    # Check metadata
    if "freshness" not in data["metadata"]:
        print("Missing metadata.freshness")
        sys.exit(1)

    if "company_tags" not in data["metadata"]:
        print("Missing metadata.company_tags")
        sys.exit(1)

    print("PASS")

except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Validation error: {e}")
    sys.exit(1)
')

if [ "$VALIDATION" = "PASS" ]; then
    echo "PASS: All validation checks passed"
    echo "Sample packet_id: $(echo "$OUTPUT" | python3 -c 'import sys,json; print(json.load(sys.stdin)["packet_id"])')"
    echo "Extractions count: $(echo "$OUTPUT" | python3 -c 'import sys,json; print(len(json.load(sys.stdin)["extractions"]))')"
    exit 0
else
    echo "FAIL: $VALIDATION"
    exit 1
fi

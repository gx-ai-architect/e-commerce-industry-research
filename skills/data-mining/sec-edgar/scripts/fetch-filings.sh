#!/bin/bash
# Fetch SEC EDGAR company facts (XBRL JSON) for a given CIK
# Usage: ./fetch-filings.sh <CIK>
# Example: ./fetch-filings.sh 0001737806

set -e

if [ -z "$1" ]; then
    echo "Error: CIK number required" >&2
    echo "Usage: $0 <CIK>" >&2
    exit 1
fi

CIK="$1"

# Strip leading zeros and pad CIK to 10 digits (avoid octal interpretation)
CIK_NUM=$(echo "$CIK" | sed 's/^0*//')
CIK_PADDED=$(printf "%010d" "$CIK_NUM")

# SEC EDGAR API endpoint for company facts
URL="https://data.sec.gov/api/xbrl/companyfacts/CIK${CIK_PADDED}.json"

# Fetch with required User-Agent header (SEC requirement)
# Rate limit: 10 req/sec (handled by caller)
curl -s -A "E-Commerce-Research research@example.com" "$URL"

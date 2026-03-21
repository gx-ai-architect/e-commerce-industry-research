# Status: Parcel Volume Skill

**Current Status:** READY

## Last Updated
2026-03-19

## What Works
- `fetch-carrier-volumes.py`: Fetches UPS and FedEx SEC EDGAR data via sec-edgar skill
- Evidence packet schema fully implemented
- Graceful fallback to revenue data when volume metrics unavailable
- Error handling for network failures and missing data
- Test script validates JSON structure and required fields

## Limitations
- **XBRL Volume Gaps**: UPS and FedEx don't report daily parcel volumes in structured XBRL data
  - Script extracts revenue as proxy and flags need for manual lookup
  - Actual volume data exists in earnings call transcripts and investor presentations
- **ShipMatrix**: Best daily volume source is proprietary, requires manual lookup
- **Pitney Bowes**: Annual report cadence means data is not real-time

## Scripts Status
- ✅ `fetch-carrier-volumes.py`: WORKING (extracts SEC data, outputs valid evidence packets)
- ✅ `fetch-shipmatrix.py`: STUB (provides template and search guidance)
- ✅ `fetch-pitney-bowes.py`: STUB (includes known data points, needs manual update for latest)
- ✅ `test-carrier-volumes.sh`: WORKING (validates JSON structure)

## Test Results
- Run: `bash test/test-carrier-volumes.sh`
- Expected: PASS with sample JSON output

## Notes
- This skill is a foundation for parcel volume research but requires manual augmentation
- For real-time volume data, use `/browse` skill to search industry reports
- Best use case: Combine automated SEC data with manual ShipMatrix/industry research
- The real value is in delta analysis (volume changes over time, not absolute numbers)

## Example Use Case: Temu Volume Analysis
To research Temu's parcel volume drop (1M → 250K daily):
1. Run this skill to get baseline carrier volumes
2. Use `/browse` to search: "Temu parcel volume 2025 tariff impact"
3. Look for ShipMatrix citations in logistics news
4. Cross-reference with carrier earnings calls mentioning cross-border volume changes

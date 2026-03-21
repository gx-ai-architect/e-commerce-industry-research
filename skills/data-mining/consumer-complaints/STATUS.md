# Consumer Complaints Skill - Status

**Status**: ✅ READY
**Built**: 2026-03-19
**Collector ID**: `consumer-complaints`

## Components

### Scripts
- ✅ `scripts/fetch-cpsc.py` - CPSC recalls and incidents (US)
- ✅ `scripts/fetch-rapex.py` - RAPEX safety alerts (EU) with e-commerce focus

### Tests
- ✅ `test/test-cpsc.sh` - Validates CPSC script output

## API Status

| API | Status | Auth Required | Rate Limit |
|-----|--------|---------------|------------|
| CPSC Recalls | ✅ Working | No | None documented |
| CPSC Incidents | ✅ Working | No | None documented |
| RAPEX Safety Gate | ⚠️ May need fallback | No | Unknown |

## Evidence Packet Schema

```json
{
  "packet_id": "PKT-COMPLAINTS-{TYPE}-{TIMESTAMP}",
  "source": {
    "collector": "consumer-complaints"
  },
  "metadata": {
    "company_tags": ["TEMU", "SHEIN"],
    "topic_tags": ["consumer-safety", "complaints", "regulatory-risk"]
  }
}
```

## Known Data Points

### EU Safety Testing (2024)
- Temu: 2/3 products (67%) failed EU safety tests
- Shein: ~50% failure rate
- AliExpress: ~40% failure rate

### CPSC API Coverage
- Product recalls: Comprehensive database
- Incident reports: Consumer-submitted complaints
- Search: Client-side filtering by keyword

## Testing Results

```bash
cd test && ./test-cpsc.sh
```

Expected: All tests pass with valid JSON output

## Integration

This skill complements:
- `eu-regulatory` - Broader EU regulatory data
- `china-regulatory` - Chinese regulatory actions
- `sentiment` - Consumer sentiment analysis

## Next Steps

- ✅ Core functionality complete
- ⏭ Consider adding:
  - UK product safety database
  - Canadian consumer complaints
  - Australia product recalls
  - Date range filtering
  - Category-specific searches

## Usage Example

```bash
# Fetch Temu-related recalls
python3 scripts/fetch-cpsc.py --query temu --limit 50

# Fetch all Chinese product incidents
python3 scripts/fetch-cpsc.py --query "made in china" --type incidents

# Fetch EU safety alerts for Shein
python3 scripts/fetch-rapex.py --query shein
```

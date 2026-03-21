# customs-data Status

**Status:** READY

**Last Updated:** 2026-03-19

## Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| fetch-cbp-stats.py | ✅ READY | Uses documented public statistics |
| fetch-tariff-rates.py | ✅ READY | 10 e-commerce HS codes covered |
| test-cbp-stats.sh | ✅ READY | Schema validation complete |
| Evidence schema | ✅ READY | Compliant with PKT format |

## Data Availability

### CBP Section 321 Data
- **Status:** Public statistics available
- **Sources:**
  - Congressional testimony (2023: 4M entries/day)
  - CBP annual reports
  - Trade press releases
- **Limitations:**
  - Not real-time (uses documented statistics)
  - No API access without credentials
- **Next Steps:**
  - FOIA requests for detailed breakdowns
  - ACE portal integration (requires customs broker access)

### Tariff Rate Data
- **Status:** Public HTS rates documented
- **Sources:**
  - USITC HTS Search (hts.usitc.gov)
  - Public tariff schedule
- **Coverage:** 10 HS codes representing major e-commerce categories
- **Limitations:**
  - Manually curated (not live API)
  - MFN rates only (no country-specific)
- **Next Steps:**
  - USITC DataWeb API integration (free registration)
  - Add Section 301 China-specific rates

## Test Results

```
Test 1: Default year statistics - PASS
Test 2: Year-specific statistics - PASS
Test 3: Schema validation - PASS
```

All tests passing. Evidence packets validate against schema.

## Known Issues

None. Both scripts operational with public data sources.

## Dependencies

- Python 3.7+ (standard library only)
- No external API keys required
- No rate limits (uses local data)

## Data Freshness

- **CBP Statistics:** Based on 2023 testimony, 2024 projections
- **Tariff Rates:** Current as of 2024 HTS schedule
- **Recommendation:** Update quarterly with new CBP reports

## Integration Notes

Both scripts output standardized evidence packets. Can be piped directly to extraction layer or aggregated for analysis.

**Critical insight:** Section 321 volumes (4M+/day) dwarf traditional import entries. This data is foundational for understanding Temu/Shein vulnerability to regulatory changes.

## Next Priority

If Section 321 reform accelerates, implement:
1. Legislative tracking (Congress.gov API)
2. Real-time CBP data via FOIA/ACE
3. Tariff impact modeling (cost increase by HS code)

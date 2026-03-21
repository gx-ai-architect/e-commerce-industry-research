# Air Freight Skill Status

## Implementation Status
✅ COMPLETE

## Scripts
- ✅ `fetch-tac-index.py` - TAC Index air cargo rates by route
- ✅ `fetch-iata-stats.py` - IATA air cargo statistics

## Tests
- ✅ `test-air-freight.sh` - Validates both air freight data collectors

## Known Limitations
- TAC Index detailed data may require subscription (stub includes known industry rates)
- IATA detailed statistics may be behind paywall (stub uses public press releases)
- Web scraping dependent on page structure changes
- May be rate-limited or blocked
- Scripts gracefully degrade to documented stubs with known data points

## Alternative Approaches
- CLIVE (Cargo Logistics Index Values): Industry benchmark for air cargo
- Baltic Exchange Air Freight Index: Weekly public reports
- Xeneta Air Freight Index: Requires enterprise subscription

## Data Coverage
**Key Routes for Temu:**
- HKG→US (Hong Kong to United States)
- PVG→US (Shanghai to United States)
- HKG→EU (Hong Kong to Europe)
- PVG→EU (Shanghai to Europe)

**IATA Metrics:**
- Global CTK (Cargo Tonne Kilometres)
- Global ACTK (Available Cargo Tonne Kilometres)
- Air cargo yields

## Last Updated
2026-03-19

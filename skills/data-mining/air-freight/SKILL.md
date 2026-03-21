# Air Freight Data Mining Skill

## Purpose
Collects air cargo rate index data from public sources. Tracks actual shipping costs for cross-border e-commerce parcel shipping (air cargo, not ocean container rates).

**Context:** Temu ships parcels by air ($3-8 per parcel). Container freight rates are irrelevant for cross-border e-commerce parcel shipping. This skill focuses on air cargo rate indices which directly impact Temu's shipping economics.

## Scripts

### fetch-tac-index.py
Fetches TAC Index air cargo rate data for key routes.

**Usage:**
```bash
./scripts/fetch-tac-index.py
./scripts/fetch-tac-index.py --route HKG-LAX
./scripts/fetch-tac-index.py --route all
```

**Output:** JSON array of evidence packets

**Key Routes for Temu Analysis:**
- HKG→US (Hong Kong to United States)
- PVG→US (Shanghai to United States)
- HKG→EU (Hong Kong to Europe)
- PVG→EU (Shanghai to Europe)

### fetch-iata-stats.py
Fetches IATA monthly air cargo statistics.

**Usage:**
```bash
./scripts/fetch-iata-stats.py
./scripts/fetch-iata-stats.py --year 2024
```

**Output:** JSON array of evidence packets

**Key Metrics:**
- CTK (Cargo Tonne Kilometres) - global air cargo demand
- ACTK (Available Cargo Tonne Kilometres) - capacity
- Air cargo yields (revenue per tonne-km)

## Evidence Packet Schema
Each script outputs evidence packets with:
- `packet_id`: Unique identifier (e.g., PKT-AIRFREIGHT-...)
- `source`: Data source metadata (type, url, title, retrieved_at, collector)
- `extractions`: Rate data, route info, statistics
- `metadata`: Freshness, company tags, topic tags

## Data Sources
- **TAC Index**: tacindex.com - Air cargo rate indices by route (weekly updates)
- **IATA Economics**: IATA monthly air cargo statistics and press releases
- **Industry Reports**: Public data points from aviation industry reports

## Signals Extracted
- Air cargo rate per kg by route
- Global air cargo demand (CTK)
- Air cargo capacity (ACTK)
- Air cargo yields
- Weekly/monthly trends

## Testing
Run `test/test-air-freight.sh` to validate air freight data collectors.

## Dependencies
- Python 3 (standard library only)
- No external packages required

## Known Limitations
- TAC Index may require subscription for detailed route-level data
- IATA detailed statistics may be behind paywall
- Scripts include documented stubs with known industry data points when API access unavailable
- Web scraping dependent on page structure (may need updates)
- Rate-limiting possible on public endpoints

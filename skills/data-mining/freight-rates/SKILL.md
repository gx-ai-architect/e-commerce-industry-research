# Freight Rates Data Mining Skill

## Purpose
Collects freight rate index data from public sources.

## Scripts

### fetch-freight-index.py
Fetches Freightos Baltic Index (FBX) data from public page.

**Usage:**
```bash
./scripts/fetch-freight-index.py
./scripts/fetch-freight-index.py --route "China-US West Coast"
```

**Output:** JSON array of evidence packets

## Evidence Packet Schema
Each script outputs evidence packets with:
- `packet_id`: Unique identifier
- `source`: Web page metadata
- `extractions`: Index values and dates
- `metadata`: Freshness, route, tags

## Data Sources
- **Freightos FBX**: Public index page (web scraping)
- **Route-specific data**: Not available in free tier (requires premium API)

## Signals Extracted
- FBX Index value
- Data date
- Note on route-specific limitations

## Testing
Run `test/test-freight.sh` to validate freight rates scraper.

## Dependencies
- Python 3 (standard library only)
- No external packages required

## Known Limitations
- Web scraping may break if page structure changes
- Route-specific rates require premium API access
- Historical data not available in free tier

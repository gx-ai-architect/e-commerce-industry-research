# App Intel Data Mining Skill

## Purpose
Collects mobile app intelligence data from Apple App Store and Google Play Store.

## Scripts

### scrape-appstore.py
Fetches app metadata from iTunes Search API.

**Usage:**
```bash
./scripts/scrape-appstore.py --bundle-id com.einnovation.temu --countries us,gb,cn
./scripts/scrape-appstore.py --app-name "Temu" --countries us
```

**Output:** JSON array of evidence packets

### scrape-playstore.py
Scrapes Google Play Store web pages for app metadata.

**Usage:**
```bash
./scripts/scrape-playstore.py --package-id com.einnovation.temu --countries us,gb,cn
```

**Output:** JSON array of evidence packets

## Evidence Packet Schema
Each script outputs evidence packets with:
- `packet_id`: Unique identifier
- `source`: API/page metadata
- `extractions`: Array of claims with evidence
- `metadata`: Freshness, country, tags

## Testing
Run `test/test-appstore.sh` to validate App Store scraper.

## Dependencies
- Python 3 (standard library only)
- No external packages required

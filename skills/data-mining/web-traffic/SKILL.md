# Web Traffic Data Mining Skill

## Purpose
Collects web traffic rankings from Cloudflare Radar and Tranco list.

## Scripts

### fetch-cloudflare-radar.py
Fetches domain rankings from Tranco list (and attempts Cloudflare Radar).

**Usage:**
```bash
./scripts/fetch-cloudflare-radar.py --domain temu.com
./scripts/fetch-cloudflare-radar.py --domain shein.com
```

**Output:** JSON array of evidence packets

## Evidence Packet Schema
Each script outputs evidence packets with:
- `packet_id`: Unique identifier
- `source`: API metadata
- `extractions`: Ranking data
- `metadata`: Freshness, domain, tags

## Data Sources
- **Tranco**: Research-oriented top list (free, no auth)
- **Cloudflare Radar**: Attempted but may require auth (fallback to Tranco)

## Testing
Run `test/test-traffic.sh` to validate web traffic scraper.

## Dependencies
- Python 3 (standard library only)
- No external packages required

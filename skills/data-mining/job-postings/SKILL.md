# Job Postings Data Mining Skill

## Purpose
Collects job posting data to track hiring velocity and expansion signals.

## Scripts

### fetch-jobs.py
Fetches job postings from Indeed RSS feed.

**Usage:**
```bash
./scripts/fetch-jobs.py --company "Temu" --location "United States"
./scripts/fetch-jobs.py --company "PDD Holdings" --keywords "engineering" --location "China"
```

**Output:** JSON array of evidence packets

## Evidence Packet Schema
Each script outputs evidence packets with:
- `packet_id`: Unique identifier
- `source`: RSS feed metadata
- `extractions`: Job count and sample job titles
- `metadata`: Freshness, company tags, job samples

## Signals Extracted
- Total job posting count
- Sample job titles (first 5)
- Sample locations (first 5)
- Hiring velocity indicator

## Testing
Run `test/test-jobs.sh` to validate job postings scraper.

## Dependencies
- Python 3 (standard library only)
- No external packages required

## Known Limitations
- RSS feeds may have limited results (typically 10-25 postings)
- Some job boards may block automated access
- If blocked, script outputs valid packet with error status

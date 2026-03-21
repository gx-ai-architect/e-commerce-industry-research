# Google Trends Data Mining Skill

## Description
Extracts search trend data from Google Trends for given search terms. Outputs evidence packets with interest-over-time data, comparing search volume across terms and time periods.

## Prerequisites
- None (Google Trends is free and public)
- Note: Google Trends scraping can be fragile due to rate limiting and anti-bot measures
- Uses direct HTTP requests to Google Trends widget API

## Usage

### Fetch trend data for search terms
```bash
python3 scripts/fetch-trends.py --terms "Temu" "Shein" "AliExpress" --timeframe "today 12-m"
```

### Common timeframes
- `today 12-m` - Last 12 months
- `today 3-m` - Last 3 months
- `today 5-y` - Last 5 years
- `2024-01-01 2024-12-31` - Custom date range

## Scripts

### scripts/fetch-trends.py
- Takes search terms as arguments
- Fetches interest-over-time data from Google Trends widget API
- Outputs evidence packet JSON with trend data as claims
- Arguments: `--terms` (one or more), `--timeframe` (optional, default: today 12-m)

## Verify

Run tests to verify the skill works:

```bash
bash test/test-fetch.sh
```

Test should print "PASS" message.

## Example Output (Evidence Packet)

```json
{
  "packet_id": "PKT-GTRENDS-001",
  "source": {
    "type": "dataset",
    "url": "https://trends.google.com/trends/explore?q=Temu,Shein",
    "title": "Google Trends - Temu, Shein",
    "retrieved_at": "2026-03-19T14:30:00Z",
    "collector": "google-trends"
  },
  "extractions": [
    {
      "claim": "Search interest for 'Temu' in Feb 2026 was 85/100",
      "evidence": "{\"term\": \"Temu\", \"date\": \"2026-02\", \"value\": 85}",
      "evidence_type": "computed_metric",
      "verification": {
        "status": "supported",
        "verifier_notes": "Extracted from Google Trends API",
        "verified_at": "2026-03-19T14:31:00Z"
      }
    }
  ],
  "metadata": {
    "freshness": "2026-03",
    "company_tags": ["Temu", "Shein"],
    "topic_tags": ["search-trends", "consumer-interest"]
  }
}
```

## Known Limitations
- Google Trends may rate-limit or block automated requests
- Trend values are relative (0-100 scale), not absolute search volumes
- Data granularity varies by timeframe (hourly/daily/weekly/monthly)
- If scraping fails consistently, STATUS.md will be marked as BLOCKED

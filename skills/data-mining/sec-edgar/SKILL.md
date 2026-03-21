# SEC EDGAR Data Mining Skill

## Description
Extracts financial data and filing metadata from SEC EDGAR using the SEC's public API. Outputs evidence packets with financial metrics (Revenue, Net Income, Assets, EPS, etc.) and filing information for a given company.

## Prerequisites
- None (SEC EDGAR API is free and public)
- Rate limit: 10 requests/second (SEC fair use policy)
- User-Agent header required: `E-Commerce-Research research@example.com`

## Usage

### Fetch company facts (XBRL data)
```bash
bash scripts/fetch-filings.sh 0001737806  # PDD Holdings CIK
```

### Extract financial metrics to evidence packet
```bash
bash scripts/fetch-filings.sh 0001737806 | python3 scripts/extract-xbrl.py --cik 0001737806 --ticker PDD
```

### Parse recent filings metadata
```bash
python3 scripts/parse-earnings.py --cik 0001737806
```

## Scripts

### scripts/fetch-filings.sh
- Takes CIK number as argument (e.g., 0001737806 for PDD)
- Fetches company facts from SEC EDGAR API (XBRL JSON endpoint)
- Outputs raw JSON to stdout
- Respects SEC rate limits (10 req/sec)

### scripts/extract-xbrl.py
- Reads SEC XBRL JSON from stdin or file
- Extracts key GAAP financial metrics from `facts.us-gaap`
- Outputs evidence packet JSON with extracted claims
- Arguments: `--cik`, `--ticker`

### scripts/parse-earnings.py
- Fetches recent SEC filings list (10-K, 20-F, 10-Q, 6-K)
- Extracts filing dates, form types, accession numbers
- Outputs evidence packet with filing metadata
- Arguments: `--cik`

## Verify

Run tests to verify the skill works:

```bash
bash test/test-fetch.sh
bash test/test-extract.sh
```

Both tests should print "PASS" messages.

## Example Output (Evidence Packet)

```json
{
  "packet_id": "PKT-SEC-001",
  "source": {
    "type": "filing",
    "url": "https://data.sec.gov/api/xbrl/companyfacts/CIK0001737806.json",
    "title": "PDD Holdings Inc. - SEC EDGAR XBRL Facts",
    "retrieved_at": "2026-03-19T14:30:00Z",
    "collector": "sec-edgar"
  },
  "extractions": [
    {
      "claim": "Revenue for 2024 was $35.0B USD",
      "evidence": "Revenues: {\"units\": {\"USD\": [{\"end\": \"2024-12-31\", \"val\": 35000000000}]}}",
      "evidence_type": "direct_quote",
      "verification": {
        "status": "supported",
        "verifier_notes": "Extracted from us-gaap:Revenues fact",
        "verified_at": "2026-03-19T14:31:00Z"
      }
    }
  ],
  "metadata": {
    "freshness": "2024-12",
    "company_tags": ["PDD"],
    "topic_tags": ["revenue", "financials"]
  }
}
```

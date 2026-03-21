# Trade Data Mining Skill

Fetch international trade data (imports/exports) by HS code from UN Comtrade, USITC, and US Census APIs.

## Purpose

Collect evidence packets containing trade flow data for e-commerce companies, logistics analysis, and cross-border commerce research.

## Data Sources

1. **UN Comtrade API v2** (`fetch-comtrade.py`)
   - Global trade database
   - Free tier: 500 requests/day, no auth
   - Coverage: All UN member countries
   - Key HS codes: 8471 (computers), 6109 (t-shirts), 6110 (sweaters), 9503 (toys), 4202 (bags)

2. **USITC DataWeb** (`fetch-usitc.py`)
   - US International Trade Commission
   - Free, no auth
   - US-specific trade data

3. **US Census Foreign Trade** (`fetch-census-trade.py`)
   - Official US import/export statistics
   - Free with optional API key
   - Monthly and annual data

## Usage

### UN Comtrade
```bash
./scripts/fetch-comtrade.py \
  --reporter 842 \
  --partner 156 \
  --hs-code 8471 \
  --year 2023
```

### USITC DataWeb
```bash
./scripts/fetch-usitc.py \
  --hs-code 8471 \
  --year 2024 \
  --country China
```

### US Census
```bash
./scripts/fetch-census-trade.py \
  --hs-code 847130 \
  --year 2024 \
  --month 11
```

## Output Format

All scripts output evidence packets in JSON:

```json
{
  "packet_id": "PKT-COMTRADE-842-156-8471-2023",
  "source": {
    "type": "api",
    "url": "https://...",
    "title": "UN Comtrade: 842 imports from 156, HS 8471, 2023",
    "retrieved_at": "2026-03-19T14:30:00Z",
    "collector": "trade-data"
  },
  "extractions": [
    {
      "claim": "842 imported goods under HS code 8471 from 156 in 2023",
      "evidence": "{...API response...}",
      "evidence_type": "api",
      "verification": { "status": "supported" }
    }
  ],
  "metadata": {
    "freshness": "2023",
    "company_tags": [],
    "topic_tags": ["trade", "imports", "hs-8471"]
  }
}
```

## Testing

```bash
cd test && ./test-fetch.sh
```

Tests validate:
- JSON output format
- Evidence packet schema
- API connectivity
- Real-world query (US-China trade)

## Common HS Codes for E-Commerce

| Code | Description |
|------|-------------|
| 8471 | Computers and data processing machines |
| 6109 | T-shirts, knitted or crocheted |
| 6110 | Sweaters, pullovers, cardigans |
| 9503 | Toys, puzzles, scale models |
| 4202 | Trunks, suitcases, handbags |
| 6203 | Men's suits, jackets, trousers |
| 9404 | Mattress supports, bedding |
| 8517 | Telephone sets, smartphones |

## Country Codes

| Code | Country |
|------|---------|
| 842  | United States |
| 156  | China |
| 392  | Japan |
| 276  | Germany |
| 826  | United Kingdom |

## Notes

- UN Comtrade is most reliable (global coverage)
- USITC and Census APIs may have limited documentation; if blocked, see STATUS.md
- All APIs are rate-limited; implement caching for production use
- HS codes at 6-digit level are internationally harmonized

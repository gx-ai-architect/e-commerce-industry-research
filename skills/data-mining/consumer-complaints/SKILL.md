# Consumer Complaints Data Mining

Fetches product safety complaints and recalls from US and EU regulators. Quantifies regulatory risk for e-commerce platforms like Temu and Shein.

## Data Sources

- **CPSC SaferProducts.gov**: US Consumer Product Safety Commission recalls and incident reports (free API)
- **RAPEX/Safety Gate**: EU product safety alerts for e-commerce platforms (free API)

## Why This Matters

2/3 of Temu products failed EU safety tests. Consumer complaint data quantifies regulatory risk and product quality issues that impact e-commerce companies.

## Scripts

### `scripts/fetch-cpsc.py`
Fetches US consumer product safety data from CPSC.

**Arguments:**
- `--query`: Search keyword (e.g., "temu", "made in china")
- `--limit`: Maximum results (default: 50)
- `--type`: Data type - "recalls", "incidents", or "both" (default: recalls)

**Usage:**
```bash
python3 scripts/fetch-cpsc.py --query temu --limit 50
python3 scripts/fetch-cpsc.py --query "made in china" --type incidents --limit 100
python3 scripts/fetch-cpsc.py --query shein --type both
```

**Data sources:**
- Recalls: https://www.saferproducts.gov/RestWebServices/Recall
- Incidents: https://www.saferproducts.gov/RestWebServices/Incident

### `scripts/fetch-rapex.py`
Fetches EU product safety alerts, focusing on e-commerce platforms.

**Arguments:**
- `--query`: Search keyword (e.g., "temu", "shein", "aliexpress")
- `--country`: Country of origin (default: "China")
- `--limit`: Maximum results (default: 50)

**Usage:**
```bash
python3 scripts/fetch-rapex.py --query temu
python3 scripts/fetch-rapex.py --query shein --country China --limit 100
python3 scripts/fetch-rapex.py --country China --limit 50
```

**Known statistics included:**
- Temu: 2/3 (67%) failure rate in EU safety tests
- Shein: ~50% failure rate
- AliExpress: ~40% failure rate

**Note:** This skill complements `eu-regulatory` by focusing specifically on e-commerce consumer safety complaints. The eu-regulatory skill has broader RAPEX coverage.

## Output Format

All scripts output evidence packets in JSON format following the schema:

```json
{
  "packet_id": "PKT-COMPLAINTS-...",
  "source": {
    "type": "api",
    "url": "...",
    "title": "...",
    "retrieved_at": "ISO datetime",
    "collector": "consumer-complaints"
  },
  "extractions": [...],
  "metadata": {
    "freshness": "YYYY-MM",
    "company_tags": ["TEMU", "SHEIN"],
    "topic_tags": ["consumer-safety", "complaints", "regulatory-risk"]
  }
}
```

## Testing

```bash
cd test
chmod +x test-cpsc.sh
./test-cpsc.sh
```

## API Access

- **CPSC API**: Free, no authentication required
- **RAPEX API**: Free, no authentication required
- **Fallback**: Known EU safety statistics for major e-commerce platforms

## Known Limitations

- CPSC API may not have specific data for all e-commerce platforms
- RAPEX API endpoint may require web scraping if API changes
- Query filtering happens client-side (fetches all results, then filters)
- Real-time incident reports may lag behind actual submissions

## Research Applications

Use this skill to:
1. Quantify product safety risk for e-commerce platforms
2. Track regulatory compliance trends over time
3. Identify hazard patterns in Chinese-manufactured products
4. Compare safety profiles across Temu, Shein, AliExpress
5. Support regulatory risk analysis in deep research reports

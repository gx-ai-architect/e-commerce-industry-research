# customs-data

Fetch US customs and tariff data critical to cross-border e-commerce analysis.

## Description

This skill collects:
1. **CBP Section 321 volumes** - De minimis entry statistics (the $800 duty-free threshold)
2. **Tariff rates** - HS code-specific duty rates for e-commerce goods

Section 321 elimination is an existential threat to Temu/Shein business models. In 2023, CBP processed ~4 million Section 321 entries per day, representing 95% of all US import entries. These shipments enter duty-free under the $800 de minimis threshold.

Without Section 321, Temu/Shein shipments would face tariffs of 14-16% on apparel (their largest category), fundamentally destroying their pricing advantage.

## Prerequisites

- Python 3.7+
- No API keys required (uses documented public statistics)

## Data Sources

### CBP Statistics
- **Primary**: CBP Trade Statistics (https://www.cbp.gov/newsroom/stats)
- **Testimony**: Congressional testimony on Section 321 volumes
- **Future**: CBP FOIA requests, ACE portal access

### Tariff Rates
- **Primary**: USITC HTS Search (https://hts.usitc.gov/)
- **Secondary**: USITC DataWeb (requires free registration)
- **Reference**: Trade.gov tariff database

## Scripts

### fetch-cbp-stats.py

Fetches US CBP Section 321 de minimis entry volumes and total import statistics.

**Usage:**
```bash
# Fetch latest year (2024)
./scripts/fetch-cbp-stats.py

# Fetch specific year
./scripts/fetch-cbp-stats.py --year 2023
```

**Output:**
Evidence packet with:
- Daily Section 321 entry volumes
- Annual Section 321 estimates
- Total import entry counts
- Section 321 as percentage of total entries

**Note:** Currently uses documented public statistics from CBP testimony and reports. For real-time data, implement CBP FOIA requests or ACE portal integration.

### fetch-tariff-rates.py

Fetches US tariff rates for e-commerce relevant HS codes.

**Usage:**
```bash
# Fetch all e-commerce relevant codes
./scripts/fetch-tariff-rates.py

# Fetch specific HS code
./scripts/fetch-tariff-rates.py --hs-code 6109  # T-shirts
./scripts/fetch-tariff-rates.py --hs-code 8517  # Smartphones
```

**Output:**
Evidence packet with:
- Tariff rates by HS code
- Product descriptions
- Relevance to Temu/Shein business model
- Impact analysis of Section 321 elimination

**Covered HS Codes:**
- **8517** - Smartphones/telecom (0%)
- **8471** - Computers/tablets (0%)
- **6109** - T-shirts/knits (16.5%)
- **6203/6204** - Men's/women's apparel (16-16.6%)
- **9503** - Toys/games (0%)
- **6302** - Home textiles (6.7-11.3%)
- **3926** - Plastic household items (3.4-5.3%)
- **6217** - Fashion accessories (14.6-16%)

## Verify

Run the test suite:
```bash
./test/test-cbp-stats.sh
```

Tests validate:
- JSON output structure
- Required evidence packet fields
- Schema compliance
- Data completeness

## Example Output

```json
{
  "packet_id": "PKT-20260319120000",
  "source": {
    "type": "dataset",
    "url": "https://www.cbp.gov/newsroom/stats",
    "title": "US CBP Trade Statistics and Section 321 Data (2024)",
    "retrieved_at": "2026-03-19T12:00:00Z",
    "collector": "customs-data"
  },
  "extractions": [
    {
      "claim": "US CBP processed approximately 4,500,000 Section 321 informal entries per day in 2024",
      "evidence": "Section 321 daily entries: 4,500,000. Projected based on 2023 baseline + e-commerce growth",
      "evidence_type": "computed_metric"
    },
    {
      "claim": "Section 321 entries represented 95.1% of all US import entries in 2024",
      "evidence": "Section 321 entries (1,642,500,000) divided by total entries (40,000,000) = 95.1%",
      "evidence_type": "computed_metric"
    }
  ],
  "metadata": {
    "freshness": "Public statistics as of 2024",
    "company_tags": ["Temu", "Shein", "AliExpress", "cross-border-ecommerce"],
    "topic_tags": ["customs", "de-minimis", "section-321", "import-volumes", "tariffs"]
  }
}
```

## Integration with Deep Research

Use this skill to:
1. **Quantify regulatory risk** - Model impact of Section 321 elimination
2. **Cost structure analysis** - Calculate tariff burden by product category
3. **Competitive dynamics** - Compare domestic vs. cross-border cost structures
4. **Policy tracking** - Monitor Section 321 reform proposals

## Future Enhancements

1. **Real-time API integration** - CBP ACE portal access (requires broker credentials)
2. **FOIA automation** - Programmatic Section 321 data requests
3. **HTS API** - Live tariff rate lookups via USITC DataWeb API
4. **Country-specific rates** - Track China-specific tariff rates (Section 301)
5. **Legislative tracking** - Monitor bills affecting Section 321 (e.g., Import Security and Fairness Act)

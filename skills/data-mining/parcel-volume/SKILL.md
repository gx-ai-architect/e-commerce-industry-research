# Parcel Volume Data Mining Skill

## Description
Extracts parcel/package delivery volume data from carrier earnings reports, industry datasets, and logistics analytics. This is THE leading indicator for e-commerce volume. Outputs standardized evidence packets with carrier volume metrics, daily parcel counts, and volume trends.

**Key Insight**: Parcel volumes are a direct proxy for e-commerce demand. For example, Temu's daily US parcels dropped from 1M to 250K-300K post-tariff, signaling a major demand shock.

## Prerequisites
- None for SEC EDGAR data (public API)
- ShipMatrix and Pitney Bowes data require manual lookup via `/browse` skill
- Depends on: `sec-edgar` skill for carrier financial data

## Usage

### Fetch UPS parcel volumes from SEC filings
```bash
python3 scripts/fetch-carrier-volumes.py --carrier ups
```

### Fetch FedEx parcel volumes
```bash
python3 scripts/fetch-carrier-volumes.py --carrier fedex
```

### Fetch all carriers
```bash
python3 scripts/fetch-carrier-volumes.py --carrier all
```

### Get ShipMatrix data template (manual lookup required)
```bash
python3 scripts/fetch-shipmatrix.py
```

### Get Pitney Bowes global parcel data
```bash
python3 scripts/fetch-pitney-bowes.py
```

## Scripts

### scripts/fetch-carrier-volumes.py
- Fetches UPS (CIK 0001090727) and FedEx (CIK 0001048911) SEC EDGAR XBRL data
- Uses the `sec-edgar/scripts/fetch-filings.sh` script to get company facts
- Extracts parcel volume metrics from XBRL concepts like `NumberOfPackagesDelivered`, `AverageDailyPackageVolume`
- Falls back to revenue data if volume metrics aren't in XBRL (volumes often reported in earnings call transcripts, not structured XBRL)
- Outputs evidence packet JSON array to stdout
- Arguments: `--carrier ups|fedex|all`

**Note**: Most carriers don't report daily parcel volumes in structured XBRL data. This script will extract what's available and flag when manual lookup is needed.

### scripts/fetch-shipmatrix.py
- STUB SCRIPT that provides a template evidence packet for ShipMatrix data
- ShipMatrix publishes proprietary daily US parcel volume estimates by carrier
- This script documents the data structure and provides search guidance
- Use `/browse` skill to search for ShipMatrix reports and industry articles
- Manual data entry required

**Search queries**:
- "ShipMatrix daily parcel volume 2025"
- "Temu parcel volume ShipMatrix"
- "US parcel delivery volumes 2025"

### scripts/fetch-pitney-bowes.py
- STUB SCRIPT with known Pitney Bowes Parcel Shipping Index data points
- Includes publicly cited data: ~160B global parcels in 2023, 266B projected by 2030
- Provides template for adding latest report data
- Use `/browse` to fetch the most recent edition

**Where to find**: https://www.pitneybowes.com/us/shipping-index

## Verify

Run the test to verify the skill works:

```bash
bash test/test-carrier-volumes.sh
```

Should print "PASS" and show sample output.

## Example Output (Evidence Packet)

```json
[
  {
    "packet_id": "PKT-PARCEL-UPS-20260319143000",
    "source": {
      "type": "api",
      "url": "https://data.sec.gov/api/xbrl/companyfacts/CIK0001090727.json",
      "title": "UPS - SEC EDGAR XBRL Company Facts",
      "retrieved_at": "2026-03-19T14:30:00Z",
      "collector": "parcel-volume"
    },
    "extractions": [
      {
        "claim": "UPS reported $97,334,000,000 in revenue as of 2024-12-31 (volume metrics not available in XBRL)",
        "evidence": "{\"Revenues\": {\"end\": \"2024-12-31\", \"val\": 97334000000, \"fy\": 2024}}",
        "evidence_type": "computed_metric",
        "verification": {
          "status": "extrapolated",
          "verifier_notes": "Volume metrics not found in XBRL - extracted revenue as proxy. Manual lookup needed for actual volume data.",
          "verified_at": "2026-03-19T14:30:15Z"
        }
      }
    ],
    "metadata": {
      "freshness": "2024-12",
      "company_tags": ["UPS"],
      "topic_tags": ["parcel-volume", "logistics", "carrier-volumes"]
    }
  }
]
```

## Data Sources

### Primary Sources
1. **SEC EDGAR** (UPS, FedEx financial filings)
   - Public API, no auth required
   - Limited volume metrics in XBRL (mostly revenue data)
   - Earnings call transcripts have volume data but require text mining

2. **ShipMatrix** (proprietary daily parcel estimates)
   - Best source for daily US parcel volumes by carrier
   - Requires manual lookup via news articles and industry reports
   - Often cited in logistics publications

3. **Pitney Bowes Parcel Shipping Index** (annual global report)
   - Authoritative source for global parcel volumes
   - Annual publication with forecasts
   - Free to access online

### Secondary Sources (Manual Research)
- Carrier investor presentations (often include volume charts)
- Industry conferences (ShipWeek, Parcel Forum)
- Trade publications (DC Velocity, Logistics Management)
- Analyst reports (Gartner, McKinsey logistics reports)

## Limitations

1. **XBRL Gaps**: Carriers typically don't report daily parcel volumes in structured XBRL data
2. **ShipMatrix Paywall**: Best daily volume data is proprietary
3. **Delayed Data**: SEC filings are quarterly, not real-time
4. **Manual Lookup Required**: Most valuable parcel data requires browsing industry reports

## Next Steps for Real-Time Data

To get current parcel volumes:
1. Use `/browse` to search for recent ShipMatrix citations
2. Check carrier earnings calls (transcripts often mention volume changes)
3. Monitor industry news for volume announcements
4. Track shipping rate changes (often correlated with volume shifts)

#!/usr/bin/env python3
"""
Extract financial metrics from SEC EDGAR XBRL JSON and output evidence packet.
Reads from stdin or file, outputs JSON to stdout.
"""

import sys
import json
import argparse
from datetime import datetime, timezone

# GAAP concepts to extract
GAAP_METRICS = {
    'Revenues': 'Revenue',
    'RevenueFromContractWithCustomerExcludingAssessedTax': 'Revenue',
    'NetIncomeLoss': 'Net Income',
    'OperatingIncomeLoss': 'Operating Income',
    'Assets': 'Total Assets',
    'StockholdersEquity': 'Stockholders Equity',
    'EarningsPerShareBasic': 'EPS (Basic)',
    'EarningsPerShareDiluted': 'EPS (Diluted)',
}

def extract_metric_value(fact_data, metric_name):
    """Extract the most recent annual value for a GAAP metric."""
    extractions = []

    if 'units' not in fact_data:
        return extractions

    # Try USD first, then other currencies
    unit_data = fact_data['units'].get('USD') or fact_data['units'].get('CNY') or list(fact_data['units'].values())[0] if fact_data['units'] else []

    # Filter for annual filings (10-K, 20-F) and sort by date
    annual_data = [
        item for item in unit_data
        if item.get('form') in ['10-K', '20-F'] and 'val' in item and 'end' in item
    ]

    # Sort by end date descending
    annual_data.sort(key=lambda x: x['end'], reverse=True)

    # Take up to 3 most recent years
    for item in annual_data[:3]:
        val = item['val']
        end_date = item['end']
        form = item.get('form', 'unknown')
        currency = 'USD' if 'USD' in fact_data['units'] else ('CNY' if 'CNY' in fact_data['units'] else 'unknown')

        # Format value nicely
        if isinstance(val, (int, float)):
            if abs(val) >= 1e9:
                val_str = f"${val/1e9:.1f}B {currency}"
            elif abs(val) >= 1e6:
                val_str = f"${val/1e6:.1f}M {currency}"
            elif metric_name.startswith('EPS'):
                val_str = f"${val:.2f}"
            else:
                val_str = f"${val:,.0f} {currency}"
        else:
            val_str = str(val)

        claim = f"{metric_name} for {end_date[:4]} was {val_str}"
        evidence = json.dumps({
            "metric": metric_name,
            "value": val,
            "currency": currency,
            "end_date": end_date,
            "form": form
        })

        extractions.append({
            "claim": claim,
            "evidence": evidence,
            "evidence_type": "direct_quote",
            "verification": {
                "status": "supported",
                "verifier_notes": f"Extracted from SEC EDGAR XBRL fact",
                "verified_at": datetime.now(timezone.utc).isoformat()
            }
        })

    return extractions

def main():
    parser = argparse.ArgumentParser(description='Extract XBRL metrics to evidence packet')
    parser.add_argument('--cik', required=True, help='Company CIK number')
    parser.add_argument('--ticker', required=True, help='Company ticker symbol')
    parser.add_argument('--input', help='Input JSON file (default: stdin)')

    args = parser.parse_args()

    # Read input
    if args.input:
        with open(args.input, 'r') as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    # Extract company info
    entity_name = data.get('entityName', 'Unknown Company')
    cik = data.get('cik', args.cik)

    # Build evidence packet
    packet = {
        "packet_id": f"PKT-SEC-{args.ticker}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "source": {
            "type": "filing",
            "url": f"https://data.sec.gov/api/xbrl/companyfacts/CIK{int(cik):010d}.json",
            "title": f"{entity_name} - SEC EDGAR XBRL Facts",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "collector": "sec-edgar"
        },
        "extractions": [],
        "metadata": {
            "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
            "company_tags": [args.ticker],
            "topic_tags": ["financials", "sec-filings"]
        }
    }

    # Extract metrics from us-gaap facts
    us_gaap = data.get('facts', {}).get('us-gaap', {})

    for gaap_concept, friendly_name in GAAP_METRICS.items():
        if gaap_concept in us_gaap:
            extractions = extract_metric_value(us_gaap[gaap_concept], friendly_name)
            packet['extractions'].extend(extractions)

    # Output JSON
    print(json.dumps(packet, indent=2))

if __name__ == '__main__':
    main()

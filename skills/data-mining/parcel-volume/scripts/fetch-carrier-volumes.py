#!/usr/bin/env python3
"""
Fetch parcel volume data from carrier SEC filings (UPS, FedEx).
Uses SEC EDGAR XBRL API to extract volume metrics from company facts.

Usage: python3 fetch-carrier-volumes.py --carrier ups|fedex|all
"""

import sys
import json
import subprocess
import argparse
from datetime import datetime, timezone

# Carrier CIK mappings
CARRIERS = {
    'ups': {'cik': '0001090727', 'name': 'UPS', 'ticker': 'UPS'},
    'fedex': {'cik': '0001048911', 'name': 'FedEx', 'ticker': 'FDX'}
}

# XBRL concepts related to parcel volume
VOLUME_CONCEPTS = [
    'NumberOfPackagesDelivered',
    'AverageDailyPackageVolume',
    'PackageVolume',
    'DailyPackageVolume',
    'TotalPackagesShipped'
]

# Revenue-per-piece concepts (fallback if volume not available)
REVENUE_CONCEPTS = [
    'RevenuePerPiece',
    'AverageRevenuePerPiece',
    'RevenuePerPackage'
]


def fetch_sec_data(cik):
    """Fetch SEC EDGAR company facts using the fetch-filings.sh script."""
    script_path = '/Users/gxxu/Desktop/e-commerce-industry-research/skills/data-mining/sec-edgar/scripts/fetch-filings.sh'

    try:
        result = subprocess.run(
            [script_path, cik],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error fetching SEC data for CIK {cik}: {e.stderr}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing SEC JSON for CIK {cik}: {e}", file=sys.stderr)
        return None


def extract_volume_metrics(sec_data, carrier_info):
    """Extract parcel volume metrics from SEC XBRL data."""
    extractions = []

    if not sec_data or 'facts' not in sec_data:
        return extractions

    # Try to find volume concepts in us-gaap or dei taxonomies
    facts = sec_data.get('facts', {})
    us_gaap = facts.get('us-gaap', {})

    # Check for volume metrics
    for concept in VOLUME_CONCEPTS:
        if concept in us_gaap:
            data = us_gaap[concept]
            units = data.get('units', {})

            # Look for most recent data point
            for unit_type, values in units.items():
                if not values:
                    continue

                # Get most recent value
                sorted_values = sorted(values, key=lambda x: x.get('end', ''), reverse=True)
                latest = sorted_values[0] if sorted_values else None

                if latest:
                    val = latest.get('val')
                    end_date = latest.get('end', 'unknown')

                    extractions.append({
                        'claim': f"{carrier_info['name']} reported {val:,} packages ({concept}) as of {end_date}",
                        'evidence': json.dumps({concept: latest}),
                        'evidence_type': 'direct_quote',
                        'verification': {
                            'status': 'supported',
                            'verifier_notes': f'Extracted from us-gaap:{concept} in SEC XBRL data',
                            'verified_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                        }
                    })

    # Fallback: Extract revenue data if no volume metrics found
    if not extractions:
        revenue_data = us_gaap.get('Revenues', {}).get('units', {}).get('USD', [])
        if revenue_data:
            sorted_revenue = sorted(revenue_data, key=lambda x: x.get('end', ''), reverse=True)
            latest_revenue = sorted_revenue[0] if sorted_revenue else None

            if latest_revenue:
                val = latest_revenue.get('val')
                end_date = latest_revenue.get('end', 'unknown')

                extractions.append({
                    'claim': f"{carrier_info['name']} reported ${val:,.0f} in revenue as of {end_date} (volume metrics not available in XBRL)",
                    'evidence': json.dumps({'Revenues': latest_revenue}),
                    'evidence_type': 'computed_metric',
                    'verification': {
                        'status': 'extrapolated',
                        'verifier_notes': 'Volume metrics not found in XBRL - extracted revenue as proxy. Manual lookup needed for actual volume data.',
                        'verified_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                    }
                })

    return extractions


def create_evidence_packet(carrier_key, extractions):
    """Create a standardized evidence packet."""
    carrier_info = CARRIERS[carrier_key]
    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    # Generate packet ID
    packet_id = f"PKT-PARCEL-{carrier_info['ticker']}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

    # Determine freshness from latest extraction
    freshness = "2024-Q4"  # Default
    if extractions:
        for extraction in extractions:
            evidence = json.loads(extraction['evidence'])
            for key, value in evidence.items():
                if isinstance(value, dict) and 'end' in value:
                    end_date = value['end']
                    if end_date:
                        freshness = end_date[:7]  # YYYY-MM format
                        break

    packet = {
        'packet_id': packet_id,
        'source': {
            'type': 'api',
            'url': f"https://data.sec.gov/api/xbrl/companyfacts/CIK{carrier_info['cik']}.json",
            'title': f"{carrier_info['name']} - SEC EDGAR XBRL Company Facts",
            'retrieved_at': now,
            'collector': 'parcel-volume'
        },
        'extractions': extractions,
        'metadata': {
            'freshness': freshness,
            'company_tags': [carrier_info['ticker']],
            'topic_tags': ['parcel-volume', 'logistics', 'carrier-volumes']
        }
    }

    return packet


def main():
    parser = argparse.ArgumentParser(description='Fetch parcel volume data from carrier SEC filings')
    parser.add_argument('--carrier', required=True, choices=['ups', 'fedex', 'all'],
                        help='Carrier to fetch data for')
    args = parser.parse_args()

    carriers_to_fetch = ['ups', 'fedex'] if args.carrier == 'all' else [args.carrier]

    all_packets = []

    for carrier_key in carriers_to_fetch:
        carrier_info = CARRIERS[carrier_key]

        # Fetch SEC data
        sec_data = fetch_sec_data(carrier_info['cik'])

        if sec_data:
            # Extract volume metrics
            extractions = extract_volume_metrics(sec_data, carrier_info)

            # Create evidence packet
            packet = create_evidence_packet(carrier_key, extractions)
            all_packets.append(packet)
        else:
            # Create error packet
            now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            error_packet = {
                'packet_id': f"PKT-PARCEL-{carrier_info['ticker']}-ERROR-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                'source': {
                    'type': 'api',
                    'url': f"https://data.sec.gov/api/xbrl/companyfacts/CIK{carrier_info['cik']}.json",
                    'title': f"{carrier_info['name']} - SEC EDGAR XBRL Company Facts",
                    'retrieved_at': now,
                    'collector': 'parcel-volume'
                },
                'extractions': [{
                    'claim': f"Failed to fetch data for {carrier_info['name']}",
                    'evidence': f"SEC API error for CIK {carrier_info['cik']}",
                    'evidence_type': 'computed_metric',
                    'verification': {
                        'status': 'unsupported',
                        'verifier_notes': 'API request failed',
                        'verified_at': now
                    }
                }],
                'metadata': {
                    'freshness': 'unknown',
                    'company_tags': [carrier_info['ticker']],
                    'topic_tags': ['parcel-volume', 'error']
                }
            }
            all_packets.append(error_packet)

    # Output all packets as JSON array
    print(json.dumps(all_packets, indent=2))


if __name__ == '__main__':
    main()

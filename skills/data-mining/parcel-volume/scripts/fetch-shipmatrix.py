#!/usr/bin/env python3
"""
ShipMatrix Parcel Volume Data - STUB SCRIPT

ShipMatrix publishes daily US parcel volume estimates, broken down by carrier.
This is proprietary data that requires manual lookup via WebSearch.

This script provides a template evidence packet for ShipMatrix data.
When you have actual data from ShipMatrix reports, fill in the template below.

Data Sources:
- ShipMatrix Daily Parcel Reports: https://www.shipmatrix.com/
- Industry reports and news articles citing ShipMatrix data
- E-commerce trade publications referencing ShipMatrix volume estimates

Key Metrics to Look For:
- Daily US parcel volume by carrier (UPS, FedEx, USPS, Amazon)
- Year-over-year volume changes
- Peak season volume spikes
- Cross-border parcel volumes

Example Data Points (from public reports):
- Temu: 1M daily US parcels (pre-tariff) → 250K-300K (post-tariff)
- Amazon: ~10M daily US parcels
- USPS: ~15M daily US parcels
- UPS: ~20M daily US parcels
- FedEx: ~13M daily US parcels
"""

import json
from datetime import datetime, timezone

def create_template_packet():
    """Create a template evidence packet for ShipMatrix data."""
    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    packet = {
        'packet_id': f"PKT-PARCEL-SHIPMATRIX-TEMPLATE-{datetime.now(timezone.utc).strftime('%Y%m%d')}",
        'source': {
            'type': 'dataset',
            'url': 'https://www.shipmatrix.com/',
            'title': 'ShipMatrix Daily Parcel Volume Data (Manual Entry Required)',
            'retrieved_at': now,
            'collector': 'parcel-volume'
        },
        'extractions': [
            {
                'claim': '[MANUAL ENTRY] Carrier X reported Y million daily parcels for date Z',
                'evidence': '[Insert ShipMatrix data table or quote here]',
                'evidence_type': 'table_slice',
                'verification': {
                    'status': 'supported',
                    'verifier_notes': 'Data from ShipMatrix report - requires manual lookup and verification',
                    'verified_at': now
                }
            },
            {
                'claim': '[EXAMPLE] Temu daily US parcels dropped from 1M to 250K-300K post-tariff (2025)',
                'evidence': 'This is an example claim based on public reports. Replace with actual ShipMatrix data.',
                'evidence_type': 'computed_metric',
                'verification': {
                    'status': 'extrapolated',
                    'verifier_notes': 'Example data - needs verification from primary ShipMatrix source',
                    'verified_at': now
                }
            }
        ],
        'metadata': {
            'freshness': '2025-Q1',
            'company_tags': ['SHIPMATRIX', 'UPS', 'FDX', 'USPS', 'AMZN'],
            'topic_tags': ['parcel-volume', 'logistics', 'e-commerce-volume']
        }
    }

    return packet


def main():
    """Output template evidence packet."""
    template = create_template_packet()

    print("# ShipMatrix Data Template")
    print("# This is a STUB script. Replace template values with actual ShipMatrix data.")
    print("# Use /browse skill to search for ShipMatrix reports and industry articles.\n")

    print(json.dumps(template, indent=2))

    print("\n# Search queries to try:")
    print('# - "ShipMatrix daily parcel volume 2025"')
    print('# - "ShipMatrix carrier volume report"')
    print('# - "Temu parcel volume ShipMatrix"')
    print('# - "US parcel delivery volumes 2025"')


if __name__ == '__main__':
    main()

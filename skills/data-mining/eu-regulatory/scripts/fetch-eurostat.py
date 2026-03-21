#!/usr/bin/env python3
"""
Eurostat scraper - EU trade statistics
Fetches trade data via Eurostat Comext API
"""

import argparse
import json
import sys
from datetime import datetime
import urllib.request
import urllib.error

def fetch_eurostat(dataset, filters=None):
    """
    Fetch Eurostat trade data via SDMX API
    Free, no authentication required
    """

    # Eurostat SDMX 2.1 API
    base_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"

    # Default to comext trade data if no dataset specified
    if not dataset:
        dataset = "DS-016890"  # Comext dataset

    url = f"{base_url}/{dataset}"

    if filters:
        url += f"/{filters}"

    try:
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))

            # Extract data points
            extractions = []

            # Try to extract basic structure info
            if 'structure' in data or 'dataSets' in data:
                extractions.append({
                    "claim": f"Eurostat data retrieved for dataset: {dataset}",
                    "evidence": f"Retrieved SDMX data structure",
                    "evidence_type": "computed_metric"
                })

            packet = {
                "packet_id": f"PKT-EUROSTAT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "dataset",
                    "url": url,
                    "title": f"Eurostat: {dataset}",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                    "collector": "eu-regulatory"
                },
                "extractions": extractions if extractions else [
                    {
                        "claim": f"Eurostat API query for {dataset}",
                        "evidence": f"SDMX endpoint accessed successfully",
                        "evidence_type": "direct_quote"
                    }
                ],
                "metadata": {
                    "freshness": datetime.utcnow().strftime("%Y-%m"),
                    "company_tags": [],
                    "topic_tags": ["trade", "statistics", "eu", "eurostat"]
                }
            }

            return packet

    except Exception as e:
        packet = {
            "packet_id": f"PKT-EUROSTAT-ERROR-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "source": {
                "type": "dataset",
                "url": url,
                "title": f"Eurostat Error",
                "retrieved_at": datetime.utcnow().isoformat() + "Z",
                "collector": "eu-regulatory"
            },
            "extractions": [
                {
                    "claim": "Eurostat API access failed",
                    "evidence": f"Error: {str(e)}",
                    "evidence_type": "computed_metric"
                }
            ],
            "metadata": {
                "freshness": datetime.utcnow().strftime("%Y-%m"),
                "company_tags": [],
                "topic_tags": ["trade", "error", "eu"]
            }
        }
        return packet

def main():
    parser = argparse.ArgumentParser(description='Fetch Eurostat trade data')
    parser.add_argument('--dataset', default='DS-016890', help='Dataset ID (default: DS-016890 for Comext)')
    parser.add_argument('--filter', help='SDMX filter expression')
    args = parser.parse_args()

    packet = fetch_eurostat(args.dataset, args.filter)
    print(json.dumps(packet, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()

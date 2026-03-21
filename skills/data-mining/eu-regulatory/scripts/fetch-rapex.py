#!/usr/bin/env python3
"""
RAPEX/Safety Gate scraper - EU product safety alerts
Fetches product recalls and safety notifications
"""

import argparse
import json
import sys
from datetime import datetime
import urllib.request
import urllib.error

def fetch_rapex(query=None, country=None, category=None):
    """
    Fetch RAPEX product safety alerts
    Free API, no authentication required
    """

    # Safety Gate API endpoint
    base_url = "https://ec.europa.eu/safety-gate-alerts/api/rapex/notifications"

    # Build query parameters
    params = []
    if query:
        params.append(f"searchKeyword={urllib.parse.quote(query)}")
    if country:
        params.append(f"countryOfOrigin={urllib.parse.quote(country)}")
    if category:
        params.append(f"productCategory={urllib.parse.quote(category)}")

    url = base_url + ("?" + "&".join(params) if params else "")

    try:
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))

            extractions = []

            # Extract alerts
            if isinstance(data, list):
                for alert in data[:5]:  # Top 5 alerts
                    extractions.append({
                        "claim": alert.get('productName', 'Product alert'),
                        "evidence": f"Risk: {alert.get('riskType', 'Unknown')} | Country: {alert.get('countryOfOrigin', 'Unknown')}",
                        "evidence_type": "direct_quote"
                    })
            elif isinstance(data, dict) and 'results' in data:
                for alert in data['results'][:5]:
                    extractions.append({
                        "claim": alert.get('productName', 'Product alert'),
                        "evidence": f"Risk: {alert.get('riskType', 'Unknown')}",
                        "evidence_type": "direct_quote"
                    })

            packet = {
                "packet_id": f"PKT-RAPEX-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "dataset",
                    "url": url,
                    "title": f"RAPEX Safety Alerts: {query or category or 'All'}",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                    "collector": "eu-regulatory"
                },
                "extractions": extractions if extractions else [
                    {
                        "claim": "RAPEX database queried",
                        "evidence": f"Query executed for: {query or 'all products'}",
                        "evidence_type": "computed_metric"
                    }
                ],
                "metadata": {
                    "freshness": datetime.utcnow().strftime("%Y-%m"),
                    "company_tags": [],
                    "topic_tags": ["safety", "recalls", "eu", "rapex"]
                }
            }

            return packet

    except Exception as e:
        packet = {
            "packet_id": f"PKT-RAPEX-ERROR-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "source": {
                "type": "dataset",
                "url": url,
                "title": "RAPEX Error",
                "retrieved_at": datetime.utcnow().isoformat() + "Z",
                "collector": "eu-regulatory"
            },
            "extractions": [
                {
                    "claim": "RAPEX API access failed",
                    "evidence": f"Error: {str(e)}",
                    "evidence_type": "computed_metric"
                }
            ],
            "metadata": {
                "freshness": datetime.utcnow().strftime("%Y-%m"),
                "company_tags": [],
                "topic_tags": ["safety", "error", "eu"]
            }
        }
        return packet

def main():
    parser = argparse.ArgumentParser(description='Fetch RAPEX product safety alerts')
    parser.add_argument('--query', help='Search keyword')
    parser.add_argument('--country', help='Country of origin (e.g., "China")')
    parser.add_argument('--category', help='Product category (e.g., "Toys")')
    args = parser.parse_args()

    packet = fetch_rapex(args.query, args.country, args.category)
    print(json.dumps(packet, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()

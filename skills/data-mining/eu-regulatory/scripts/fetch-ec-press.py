#!/usr/bin/env python3
"""
European Commission press releases scraper
Fetches official EC announcements and statements
"""

import argparse
import json
import sys
from datetime import datetime
import urllib.request
import urllib.error

def fetch_ec_press(query):
    """
    Fetch European Commission press releases
    """

    # EC press corner search
    url = f"https://ec.europa.eu/commission/presscorner/api/search?query={urllib.parse.quote(query)}&language=en"

    try:
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))

            extractions = []

            # Extract press releases
            if 'items' in data:
                for item in data['items'][:5]:  # Top 5 results
                    extractions.append({
                        "claim": item.get('title', 'Press release'),
                        "evidence": f"Date: {item.get('date', 'Unknown')} | {item.get('description', '')}",
                        "evidence_type": "direct_quote"
                    })

            packet = {
                "packet_id": f"PKT-ECPRESS-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "article",
                    "url": url,
                    "title": f"EC Press Releases: {query}",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                    "collector": "eu-regulatory"
                },
                "extractions": extractions if extractions else [
                    {
                        "claim": f"EC press search performed for: {query}",
                        "evidence": "No results found",
                        "evidence_type": "computed_metric"
                    }
                ],
                "metadata": {
                    "freshness": datetime.utcnow().strftime("%Y-%m"),
                    "company_tags": [],
                    "topic_tags": ["press", "announcements", "eu", query.lower()]
                }
            }

            return packet

    except Exception as e:
        packet = {
            "packet_id": f"PKT-ECPRESS-ERROR-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "source": {
                "type": "article",
                "url": url,
                "title": f"EC Press Error: {query}",
                "retrieved_at": datetime.utcnow().isoformat() + "Z",
                "collector": "eu-regulatory"
            },
            "extractions": [
                {
                    "claim": "EC press search failed",
                    "evidence": f"Error: {str(e)}",
                    "evidence_type": "computed_metric"
                }
            ],
            "metadata": {
                "freshness": datetime.utcnow().strftime("%Y-%m"),
                "company_tags": [],
                "topic_tags": ["press", "error", "eu"]
            }
        }
        return packet

def main():
    parser = argparse.ArgumentParser(description='Fetch EC press releases')
    parser.add_argument('--query', required=True, help='Search query')
    args = parser.parse_args()

    packet = fetch_ec_press(args.query)
    print(json.dumps(packet, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()

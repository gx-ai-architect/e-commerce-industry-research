#!/usr/bin/env python3
"""
China Customs scraper
Fetches trade statistics and customs data
"""

import argparse
import json
import sys
from datetime import datetime
import urllib.request
import urllib.error

def fetch_customs(query, hs_code=None):
    """
    Fetch China Customs trade statistics
    """

    # Use English version for better accessibility
    base_url = "http://english.customs.gov.cn/"

    params = []
    if query:
        params.append(f"query={urllib.parse.quote(query)}")
    if hs_code:
        params.append(f"hs_code={hs_code}")

    url = base_url + ("?" + "&".join(params) if params else "")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')

            packet = {
                "packet_id": f"PKT-CUSTOMS-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "dataset",
                    "url": url,
                    "title": f"China Customs Data: {query or hs_code}",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                    "collector": "china-regulatory"
                },
                "extractions": [
                    {
                        "claim": f"China Customs search performed",
                        "evidence": f"Retrieved {len(html)} bytes for query={query}, hs_code={hs_code}",
                        "evidence_type": "direct_quote"
                    }
                ],
                "metadata": {
                    "freshness": datetime.utcnow().strftime("%Y-%m"),
                    "company_tags": [query] if query else [],
                    "topic_tags": ["trade", "customs", "china", "statistics"]
                }
            }

            return packet

    except Exception as e:
        packet = {
            "packet_id": f"PKT-CUSTOMS-ERROR-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "source": {
                "type": "dataset",
                "url": url,
                "title": f"China Customs Error",
                "retrieved_at": datetime.utcnow().isoformat() + "Z",
                "collector": "china-regulatory"
            },
            "extractions": [
                {
                    "claim": "China Customs website access failed",
                    "evidence": f"Error: {str(e)}",
                    "evidence_type": "computed_metric"
                }
            ],
            "metadata": {
                "freshness": datetime.utcnow().strftime("%Y-%m"),
                "company_tags": [query] if query else [],
                "topic_tags": ["trade", "error", "china"]
            }
        }
        return packet

def main():
    parser = argparse.ArgumentParser(description='Fetch China Customs data')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--hs-code', help='HS code for product category')
    args = parser.parse_args()

    if not args.query and not args.hs_code:
        parser.error('At least one of --query or --hs-code is required')

    packet = fetch_customs(args.query, args.hs_code)
    print(json.dumps(packet, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()

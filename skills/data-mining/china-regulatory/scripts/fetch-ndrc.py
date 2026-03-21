#!/usr/bin/env python3
"""
NDRC (National Development and Reform Commission) scraper
Fetches pricing regulations and economic policy announcements
"""

import argparse
import json
import sys
from datetime import datetime
import urllib.request
import urllib.error

def fetch_ndrc(query):
    """
    Fetch NDRC policy announcements
    """

    url = f"https://www.ndrc.gov.cn/fzggw/jgsj/zcs/sjdt/?code=&title={urllib.parse.quote(query)}"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')

            packet = {
                "packet_id": f"PKT-NDRC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "article",
                    "url": url,
                    "title": f"NDRC Policy Search: {query}",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                    "collector": "china-regulatory"
                },
                "extractions": [
                    {
                        "claim": f"NDRC policy search performed for: {query}",
                        "evidence": f"Retrieved {len(html)} bytes from NDRC website",
                        "evidence_type": "direct_quote"
                    }
                ],
                "metadata": {
                    "freshness": datetime.utcnow().strftime("%Y-%m"),
                    "company_tags": [query],
                    "topic_tags": ["regulatory", "policy", "pricing", "china"]
                }
            }

            return packet

    except Exception as e:
        packet = {
            "packet_id": f"PKT-NDRC-ERROR-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "source": {
                "type": "article",
                "url": url,
                "title": f"NDRC Error: {query}",
                "retrieved_at": datetime.utcnow().isoformat() + "Z",
                "collector": "china-regulatory"
            },
            "extractions": [
                {
                    "claim": "NDRC website access failed",
                    "evidence": f"Error: {str(e)}",
                    "evidence_type": "computed_metric"
                }
            ],
            "metadata": {
                "freshness": datetime.utcnow().strftime("%Y-%m"),
                "company_tags": [query],
                "topic_tags": ["regulatory", "error", "china"]
            }
        }
        return packet

def main():
    parser = argparse.ArgumentParser(description='Fetch NDRC policy data')
    parser.add_argument('--query', required=True, help='Search query')
    args = parser.parse_args()

    packet = fetch_ndrc(args.query)
    print(json.dumps(packet, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()

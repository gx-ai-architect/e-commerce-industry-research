#!/usr/bin/env python3
"""
EUR-Lex scraper - Official EU law database
Fetches EU legislation, regulations, and legal documents
"""

import argparse
import json
import sys
from datetime import datetime
import urllib.request
import urllib.error

def fetch_eurlex(query):
    """
    Search EUR-Lex for EU legislation
    """

    # EUR-Lex search URL
    url = f"https://eur-lex.europa.eu/search.html?type=quick&text={urllib.parse.quote(query)}&qid=1&DB_TYPE_OF_ACT=allacts"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')

            # Basic extraction
            extractions = [
                {
                    "claim": f"EUR-Lex search performed for: {query}",
                    "evidence": f"Retrieved {len(html)} bytes from EUR-Lex database",
                    "evidence_type": "direct_quote"
                }
            ]

            # Look for common EU regulations in response
            if "Digital Services Act" in html or "DSA" in html:
                extractions.append({
                    "claim": "Digital Services Act mentioned in results",
                    "evidence": "DSA/Digital Services Act found in search results",
                    "evidence_type": "direct_quote"
                })

            if "Digital Markets Act" in html or "DMA" in html:
                extractions.append({
                    "claim": "Digital Markets Act mentioned in results",
                    "evidence": "DMA/Digital Markets Act found in search results",
                    "evidence_type": "direct_quote"
                })

            packet = {
                "packet_id": f"PKT-EURLEX-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "article",
                    "url": url,
                    "title": f"EUR-Lex Search: {query}",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                    "collector": "eu-regulatory"
                },
                "extractions": extractions,
                "metadata": {
                    "freshness": datetime.utcnow().strftime("%Y-%m"),
                    "company_tags": [],
                    "topic_tags": ["regulatory", "eu", "legislation", query.lower()]
                }
            }

            return packet

    except Exception as e:
        packet = {
            "packet_id": f"PKT-EURLEX-ERROR-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "source": {
                "type": "article",
                "url": url,
                "title": f"EUR-Lex Error: {query}",
                "retrieved_at": datetime.utcnow().isoformat() + "Z",
                "collector": "eu-regulatory"
            },
            "extractions": [
                {
                    "claim": "EUR-Lex access failed",
                    "evidence": f"Error: {str(e)}",
                    "evidence_type": "computed_metric"
                }
            ],
            "metadata": {
                "freshness": datetime.utcnow().strftime("%Y-%m"),
                "company_tags": [],
                "topic_tags": ["regulatory", "error", "eu"]
            }
        }
        return packet

def main():
    parser = argparse.ArgumentParser(description='Search EUR-Lex for EU legislation')
    parser.add_argument('--query', required=True, help='Search query (e.g., "digital services act")')
    args = parser.parse_args()

    packet = fetch_eurlex(args.query)
    print(json.dumps(packet, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()

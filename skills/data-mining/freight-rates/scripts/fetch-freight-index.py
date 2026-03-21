#!/usr/bin/env python3
"""
Fetches freight rate index data from public sources.
Outputs evidence packets in JSON format.
"""

import argparse
import json
import sys
import urllib.request
import re
from datetime import datetime, timezone

def fetch_freightos_fbx():
    """Attempt to fetch Freightos Baltic Index (FBX) data."""
    try:
        # Try to scrape the public Freightos FBX page
        url = "https://fbx.freightos.com/"

        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )

        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')

        # Try to extract current index value from page
        # This is a simple regex-based extraction - may need adjustment
        index_match = re.search(r'"price["\']?\s*:\s*["\']?([\d,]+)', html)
        date_match = re.search(r'"date["\']?\s*:\s*["\']?([\d-]+)', html)

        if index_match:
            index_value = index_match.group(1)
            date_value = date_match.group(1) if date_match else "Unknown"

            packet = {
                "packet_id": f"PKT-FBX-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "article",
                    "url": url,
                    "title": "Freightos Baltic Index (FBX)",
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "collector": "freight-rates"
                },
                "extractions": [
                    {
                        "claim": f"FBX Index Value: ${index_value}",
                        "evidence": f"price: {index_value}",
                        "evidence_type": "direct_quote"
                    },
                    {
                        "claim": f"Data Date: {date_value}",
                        "evidence": f"date: {date_value}",
                        "evidence_type": "direct_quote"
                    }
                ],
                "metadata": {
                    "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
                    "topic_tags": ["freight-rates", "fbx-index", "shipping-costs"]
                }
            }
            return packet
        else:
            # Could not extract data
            return {
                "packet_id": f"PKT-FBX-NOPARSE-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "article",
                    "url": url,
                    "title": "Freightos Baltic Index (FBX) - Cannot Parse",
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "collector": "freight-rates"
                },
                "extractions": [
                    {
                        "claim": "Unable to parse FBX data from page",
                        "evidence": "Page structure may have changed",
                        "evidence_type": "direct_quote"
                    }
                ],
                "metadata": {
                    "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
                    "status": "PARSE_ERROR",
                    "topic_tags": ["freight-rates"]
                }
            }

    except Exception as e:
        return {
            "packet_id": f"PKT-FBX-ERROR-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            "source": {
                "type": "article",
                "url": url if 'url' in locals() else "https://fbx.freightos.com/",
                "title": "Freightos Baltic Index (FBX) - ERROR",
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "collector": "freight-rates"
            },
            "extractions": [
                {
                    "claim": f"Error fetching FBX data: {str(e)}",
                    "evidence": str(e),
                    "evidence_type": "direct_quote"
                }
            ],
            "metadata": {
                "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
                "status": "ERROR",
                "topic_tags": ["freight-rates"]
            }
        }

def fetch_route_specific(route):
    """Fetch route-specific freight data (if available)."""
    # For now, return a placeholder noting that route-specific data
    # requires premium APIs
    return {
        "packet_id": f"PKT-ROUTE-{route.replace(' ', '-').upper()}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "source": {
            "type": "article",
            "url": "N/A",
            "title": f"Freight Rates - {route}",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "collector": "freight-rates"
        },
        "extractions": [
            {
                "claim": "Route-specific data requires premium API access",
                "evidence": "Free tier does not provide route-level breakdown",
                "evidence_type": "direct_quote"
            }
        ],
        "metadata": {
            "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
            "route": route,
            "status": "REQUIRES_PREMIUM",
            "topic_tags": ["freight-rates"]
        }
    }

def main():
    parser = argparse.ArgumentParser(description='Fetch freight rate index data')
    parser.add_argument('--route', help='Route to fetch (e.g., "China-US West Coast")')

    args = parser.parse_args()

    packets = []

    # Always fetch FBX index
    fbx_packet = fetch_freightos_fbx()
    packets.append(fbx_packet)

    # If route specified, add route-specific packet
    if args.route:
        route_packet = fetch_route_specific(args.route)
        packets.append(route_packet)

    # Output all packets as JSON array
    print(json.dumps(packets, indent=2))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Fetches web traffic data from Cloudflare Radar and Tranco ranking.
Outputs evidence packets in JSON format.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone

def fetch_tranco_ranking(domain):
    """Fetch domain ranking from Tranco list."""
    try:
        # Tranco API endpoint
        url = f"https://tranco-list.eu/api/ranks/domain/{domain}"

        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        if data.get('ranks'):
            ranks = data['ranks']
            latest_rank = ranks[0] if ranks else None

            packet = {
                "packet_id": f"PKT-TRANCO-{domain.upper().replace('.', '-')}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "api",
                    "url": url,
                    "title": f"Tranco Ranking - {domain}",
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "collector": "web-traffic"
                },
                "extractions": [
                    {
                        "claim": f"Domain: {domain}",
                        "evidence": f"domain: {domain}",
                        "evidence_type": "direct_quote"
                    },
                    {
                        "claim": f"Global Rank: {latest_rank['rank'] if latest_rank else 'N/A'}",
                        "evidence": f"rank: {latest_rank['rank'] if latest_rank else 'N/A'}",
                        "evidence_type": "direct_quote"
                    },
                    {
                        "claim": f"List Date: {latest_rank['date'] if latest_rank else 'N/A'}",
                        "evidence": f"date: {latest_rank['date'] if latest_rank else 'N/A'}",
                        "evidence_type": "direct_quote"
                    }
                ],
                "metadata": {
                    "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
                    "domain": domain,
                    "topic_tags": ["web-traffic", "domain-ranking"],
                    "rank_history": ranks[:5] if len(ranks) > 1 else None
                }
            }
            return packet

        else:
            # No ranking data
            return {
                "packet_id": f"PKT-TRANCO-NODATA-{domain.upper().replace('.', '-')}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "api",
                    "url": url,
                    "title": f"Tranco Ranking - {domain} (NO DATA)",
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "collector": "web-traffic"
                },
                "extractions": [
                    {
                        "claim": "No ranking data available",
                        "evidence": "Domain not found in Tranco list",
                        "evidence_type": "direct_quote"
                    }
                ],
                "metadata": {
                    "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
                    "domain": domain,
                    "status": "NO_DATA",
                    "topic_tags": ["web-traffic"]
                }
            }

    except Exception as e:
        return {
            "packet_id": f"PKT-TRANCO-ERROR-{domain.upper().replace('.', '-')}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            "source": {
                "type": "api",
                "url": url if 'url' in locals() else "N/A",
                "title": f"Tranco Ranking - {domain} (ERROR)",
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "collector": "web-traffic"
            },
            "extractions": [
                {
                    "claim": f"Error fetching ranking: {str(e)}",
                    "evidence": str(e),
                    "evidence_type": "direct_quote"
                }
            ],
            "metadata": {
                "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
                "domain": domain,
                "status": "ERROR",
                "topic_tags": ["web-traffic"]
            }
        }

def fetch_cloudflare_radar(domain):
    """Attempt to fetch from Cloudflare Radar public API."""
    try:
        # Try public Cloudflare Radar endpoint (may not work without auth)
        url = f"https://api.cloudflare.com/client/v4/radar/ranking/domain/{domain}"

        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        # Process if successful
        if data.get('success'):
            result = data.get('result', {})
            packet = {
                "packet_id": f"PKT-CFRADAR-{domain.upper().replace('.', '-')}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "api",
                    "url": url,
                    "title": f"Cloudflare Radar - {domain}",
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "collector": "web-traffic"
                },
                "extractions": [
                    {
                        "claim": f"Domain: {domain}",
                        "evidence": f"domain: {domain}",
                        "evidence_type": "direct_quote"
                    }
                ],
                "metadata": {
                    "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
                    "domain": domain,
                    "topic_tags": ["web-traffic", "cloudflare-radar"]
                }
            }

            # Add any available ranking data
            if result:
                packet["extractions"].append({
                    "claim": f"Cloudflare Radar data: {json.dumps(result)}",
                    "evidence": json.dumps(result),
                    "evidence_type": "direct_quote"
                })

            return packet

    except:
        # Fall back to Tranco if Cloudflare fails
        pass

    return None

def main():
    parser = argparse.ArgumentParser(description='Fetch web traffic rankings')
    parser.add_argument('--domain', required=True, help='Domain to lookup (e.g., temu.com)')

    args = parser.parse_args()

    packets = []

    # Try Cloudflare Radar first
    cf_packet = fetch_cloudflare_radar(args.domain)
    if cf_packet:
        packets.append(cf_packet)

    # Always try Tranco as well (more reliable)
    tranco_packet = fetch_tranco_ranking(args.domain)
    packets.append(tranco_packet)

    # Output all packets as JSON array
    print(json.dumps(packets, indent=2))

if __name__ == '__main__':
    main()

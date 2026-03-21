#!/usr/bin/env python3
"""
Scrapes Google Play Store for app metadata using web scraping.
Outputs evidence packets in JSON format.
"""

import argparse
import json
import sys
import urllib.request
import re
from datetime import datetime, timezone

def fetch_playstore_data(package_id, countries=None):
    """Fetch app data from Google Play Store web page."""
    if countries is None:
        countries = ['us']

    packets = []

    for country in countries:
        try:
            # Google Play Store URL
            hl = 'en' if country == 'us' else country
            gl = country.upper()
            url = f"https://play.google.com/store/apps/details?id={package_id}&hl={hl}&gl={gl}"

            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')

            # Extract basic info using regex (simple parsing)
            app_name_match = re.search(r'"name":"([^"]+)"', html)
            rating_match = re.search(r'"aggregateRating":\{"@type":"AggregateRating","ratingValue":([\d.]+)', html)
            review_count_match = re.search(r'"ratingCount":"?([\d,]+)"?', html)
            installs_match = re.search(r'"numDownloads":"([^"]+)"', html)

            app_name = app_name_match.group(1) if app_name_match else "N/A"
            rating = rating_match.group(1) if rating_match else "N/A"
            review_count = review_count_match.group(1) if review_count_match else "N/A"
            installs = installs_match.group(1) if installs_match else "N/A"

            packet = {
                "packet_id": f"PKT-PLAYSTORE-{country.upper()}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "article",
                    "url": url,
                    "title": f"Google Play Store - {country.upper()}",
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "collector": "app-intel"
                },
                "extractions": [
                    {
                        "claim": f"App: {app_name}",
                        "evidence": f"App name: {app_name}",
                        "evidence_type": "direct_quote"
                    },
                    {
                        "claim": f"Rating: {rating}/5",
                        "evidence": f"aggregateRating.ratingValue: {rating}",
                        "evidence_type": "direct_quote"
                    },
                    {
                        "claim": f"Review Count: {review_count}",
                        "evidence": f"ratingCount: {review_count}",
                        "evidence_type": "direct_quote"
                    },
                    {
                        "claim": f"Installs: {installs}",
                        "evidence": f"numDownloads: {installs}",
                        "evidence_type": "direct_quote"
                    }
                ],
                "metadata": {
                    "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
                    "country": country.upper(),
                    "topic_tags": ["app-rankings", "mobile-commerce"]
                }
            }
            packets.append(packet)

        except urllib.error.HTTPError as e:
            # Handle HTTP errors (403, 404, etc.)
            packet = {
                "packet_id": f"PKT-PLAYSTORE-BLOCKED-{country.upper()}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "article",
                    "url": url if 'url' in locals() else "N/A",
                    "title": f"Google Play Store - {country.upper()} (BLOCKED)",
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "collector": "app-intel"
                },
                "extractions": [
                    {
                        "claim": f"BLOCKED: Anti-bot protection - HTTP {e.code}",
                        "evidence": str(e),
                        "evidence_type": "direct_quote"
                    }
                ],
                "metadata": {
                    "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
                    "country": country.upper(),
                    "status": "BLOCKED: Anti-bot",
                    "topic_tags": ["app-rankings"]
                }
            }
            packets.append(packet)

        except Exception as e:
            # General error handling
            packet = {
                "packet_id": f"PKT-PLAYSTORE-ERROR-{country.upper()}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "article",
                    "url": url if 'url' in locals() else "N/A",
                    "title": f"Google Play Store - {country.upper()} (ERROR)",
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "collector": "app-intel"
                },
                "extractions": [
                    {
                        "claim": f"Error fetching data: {str(e)}",
                        "evidence": str(e),
                        "evidence_type": "direct_quote"
                    }
                ],
                "metadata": {
                    "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
                    "country": country.upper(),
                    "status": "ERROR",
                    "topic_tags": ["app-rankings"]
                }
            }
            packets.append(packet)

    return packets

def main():
    parser = argparse.ArgumentParser(description='Scrape Google Play Store metadata')
    parser.add_argument('--package-id', required=True, help='Package ID to lookup (e.g., com.example.app)')
    parser.add_argument('--countries', default='us', help='Comma-separated country codes (e.g., us,gb,cn)')

    args = parser.parse_args()

    countries = [c.strip().lower() for c in args.countries.split(',')]
    packets = fetch_playstore_data(args.package_id, countries=countries)

    # Output all packets as JSON array
    print(json.dumps(packets, indent=2))

if __name__ == '__main__':
    main()

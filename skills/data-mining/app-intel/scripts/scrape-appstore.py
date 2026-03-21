#!/usr/bin/env python3
"""
Scrapes Apple App Store for app metadata using the iTunes Search API.
Outputs evidence packets in JSON format.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone

def fetch_app_data(bundle_id=None, app_name=None, countries=None):
    """Fetch app data from iTunes Search API."""
    if countries is None:
        countries = ['us']

    packets = []

    for country in countries:
        try:
            if bundle_id:
                # Use lookup API for bundle ID
                url = f"https://itunes.apple.com/lookup?bundleId={urllib.parse.quote(bundle_id)}&country={country}"
            elif app_name:
                # Use search API for app name
                url = f"https://itunes.apple.com/search?term={urllib.parse.quote(app_name)}&entity=software&country={country}&limit=1"
            else:
                continue

            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())

            if data.get('resultCount', 0) > 0:
                app = data['results'][0]

                packet = {
                    "packet_id": f"PKT-APPSTORE-{country.upper()}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                    "source": {
                        "type": "api",
                        "url": url,
                        "title": f"iTunes Search API - {country.upper()}",
                        "retrieved_at": datetime.now(timezone.utc).isoformat(),
                        "collector": "app-intel"
                    },
                    "extractions": [
                        {
                            "claim": f"App: {app.get('trackName', 'N/A')}",
                            "evidence": f"trackName: {app.get('trackName', 'N/A')}",
                            "evidence_type": "direct_quote"
                        },
                        {
                            "claim": f"Rating: {app.get('averageUserRating', 'N/A')}/5",
                            "evidence": f"averageUserRating: {app.get('averageUserRating', 'N/A')}",
                            "evidence_type": "direct_quote"
                        },
                        {
                            "claim": f"Review Count: {app.get('userRatingCount', 'N/A')}",
                            "evidence": f"userRatingCount: {app.get('userRatingCount', 'N/A')}",
                            "evidence_type": "direct_quote"
                        },
                        {
                            "claim": f"Current Version: {app.get('version', 'N/A')}",
                            "evidence": f"version: {app.get('version', 'N/A')}",
                            "evidence_type": "direct_quote"
                        },
                        {
                            "claim": f"Primary Genre: {app.get('primaryGenreName', 'N/A')}",
                            "evidence": f"primaryGenreName: {app.get('primaryGenreName', 'N/A')}",
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

        except Exception as e:
            # Return error packet
            packet = {
                "packet_id": f"PKT-APPSTORE-ERROR-{country.upper()}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "api",
                    "url": url if 'url' in locals() else "N/A",
                    "title": f"iTunes Search API - {country.upper()} (ERROR)",
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
    parser = argparse.ArgumentParser(description='Scrape Apple App Store metadata')
    parser.add_argument('--app-name', help='App name to search for')
    parser.add_argument('--bundle-id', help='Bundle ID to lookup')
    parser.add_argument('--countries', default='us', help='Comma-separated country codes (e.g., us,gb,cn)')

    args = parser.parse_args()

    if not args.app_name and not args.bundle_id:
        print(json.dumps({"error": "Must provide --app-name or --bundle-id"}), file=sys.stderr)
        sys.exit(1)

    countries = [c.strip().lower() for c in args.countries.split(',')]
    packets = fetch_app_data(bundle_id=args.bundle_id, app_name=args.app_name, countries=countries)

    # Output all packets as JSON array
    print(json.dumps(packets, indent=2))

if __name__ == '__main__':
    main()

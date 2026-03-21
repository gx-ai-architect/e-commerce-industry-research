#!/usr/bin/env python3
"""
USITC DataWeb API Fetcher
Fetches US import/export data and outputs evidence packets.
"""

import argparse
import json
import sys
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def fetch_usitc_data(hs_code, year, country):
    """
    Fetch trade data from USITC DataWeb.

    API endpoint: https://dataweb.usitc.gov/api/
    Free, no auth required

    Note: USITC API documentation is limited. This implementation
    attempts to construct a reasonable query. If blocked, mark STATUS.md as BLOCKED.
    """
    # Construct API URL (best effort based on typical REST patterns)
    base_url = "https://dataweb.usitc.gov/api/trade"
    params = f"?hs={hs_code}&year={year}&country={country}"
    url = base_url + params

    try:
        # Make request
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        req.add_header('Accept', 'application/json')

        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())

            # Build evidence packet
            packet = {
                "packet_id": f"PKT-USITC-{hs_code}-{year}-{country}",
                "source": {
                    "type": "api",
                    "url": url,
                    "title": f"USITC DataWeb: HS {hs_code}, {year}, {country}",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                    "collector": "trade-data"
                },
                "extractions": [
                    {
                        "claim": f"US trade data for HS code {hs_code} with {country} in {year}",
                        "evidence": json.dumps(data, indent=2),
                        "evidence_type": "api",
                        "verification": {
                            "status": "supported"
                        }
                    }
                ],
                "metadata": {
                    "freshness": str(year),
                    "company_tags": [],
                    "topic_tags": ["trade", "usitc", f"hs-{hs_code}"]
                }
            }

            return packet

    except HTTPError as e:
        return {
            "error": f"HTTP error {e.code}: {e.reason}",
            "url": url,
            "note": "USITC API may require different endpoint structure or auth. Mark STATUS.md as BLOCKED if this persists."
        }
    except URLError as e:
        return {
            "error": f"URL error: {e.reason}",
            "url": url
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "url": url
        }


def main():
    parser = argparse.ArgumentParser(description='Fetch USITC DataWeb trade data')
    parser.add_argument('--hs-code', required=True, help='HS code (e.g., 8471)')
    parser.add_argument('--year', required=True, help='Year (e.g., 2024)')
    parser.add_argument('--country', required=True, help='Country name or code')

    args = parser.parse_args()

    result = fetch_usitc_data(args.hs_code, args.year, args.country)
    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()

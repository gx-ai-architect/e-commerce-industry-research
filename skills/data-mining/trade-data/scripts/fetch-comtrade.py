#!/usr/bin/env python3
"""
UN Comtrade API v2 Data Fetcher
Fetches import/export data by HS code and outputs evidence packets.
"""

import argparse
import json
import sys
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def fetch_comtrade_data(reporter, partner, hs_code, year):
    """
    Fetch trade data from UN Comtrade API v2.

    API endpoint: https://comtradeapi.un.org/data/v1/get/{typeCode}/{freqCode}/{clCode}
    - typeCode: C (commodities)
    - freqCode: A (annual) or M (monthly)
    - clCode: HS (Harmonized System)

    Free tier: 500 requests/day, no auth required
    """
    # Build API URL
    base_url = "https://comtradeapi.un.org/data/v1/get/C/A/HS"
    params = f"?reporterCode={reporter}&period={year}&partnerCode={partner}&cmdCode={hs_code}&flowCode=M"
    url = base_url + params

    try:
        # Make request
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')

        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())

            # Check if data exists
            if not data or 'data' not in data or not data['data']:
                return {
                    "error": "No data returned from API",
                    "url": url
                }

            # Extract first record for evidence
            record = data['data'][0] if isinstance(data['data'], list) else data['data']

            # Build evidence packet
            packet = {
                "packet_id": f"PKT-COMTRADE-{reporter}-{partner}-{hs_code}-{year}",
                "source": {
                    "type": "api",
                    "url": url,
                    "title": f"UN Comtrade: {reporter} imports from {partner}, HS {hs_code}, {year}",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                    "collector": "trade-data"
                },
                "extractions": [
                    {
                        "claim": f"{reporter} imported goods under HS code {hs_code} from {partner} in {year}",
                        "evidence": json.dumps(record, indent=2),
                        "evidence_type": "api",
                        "verification": {
                            "status": "supported"
                        }
                    }
                ],
                "metadata": {
                    "freshness": str(year),
                    "company_tags": [],
                    "topic_tags": ["trade", "imports", f"hs-{hs_code}"]
                }
            }

            return packet

    except HTTPError as e:
        return {
            "error": f"HTTP error {e.code}: {e.reason}",
            "url": url
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
    parser = argparse.ArgumentParser(description='Fetch UN Comtrade trade data')
    parser.add_argument('--reporter', required=True, help='Reporter country code (e.g., 842 for USA)')
    parser.add_argument('--partner', required=True, help='Partner country code (e.g., 156 for China)')
    parser.add_argument('--hs-code', required=True, help='HS code (e.g., 8471 for computers)')
    parser.add_argument('--year', required=True, help='Year (e.g., 2024)')

    args = parser.parse_args()

    result = fetch_comtrade_data(args.reporter, args.partner, args.hs_code, args.year)
    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()

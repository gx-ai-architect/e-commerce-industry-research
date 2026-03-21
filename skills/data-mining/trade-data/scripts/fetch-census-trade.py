#!/usr/bin/env python3
"""
US Census Foreign Trade API Fetcher
Fetches US import/export data and outputs evidence packets.
"""

import argparse
import json
import sys
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def fetch_census_trade_data(hs_code, year, month=None):
    """
    Fetch trade data from US Census Foreign Trade API.

    API endpoint: https://api.census.gov/data/timeseries/intltrade/imports/hs
    Free with API key (optional for basic queries)

    Example: https://api.census.gov/data/2024/timeseries/intltrade/imports/hs?get=I_COMMODITY,I_COMMODITY_LDESC,GEN_VAL_MO&COMM_LVL=HS6&time=2024-01
    """
    # Build API URL
    base_url = f"https://api.census.gov/data/{year}/timeseries/intltrade/imports/hs"

    # Build time parameter
    if month:
        time_param = f"{year}-{month:02d}"
    else:
        time_param = year

    # Query parameters: get commodity code, description, and monthly value
    params = f"?get=I_COMMODITY,I_COMMODITY_LDESC,GEN_VAL_MO&COMM_LVL=HS6&time={time_param}"

    # Filter by HS code if specific enough (HS6 level)
    if len(hs_code) >= 6:
        params += f"&I_COMMODITY={hs_code[:6]}"

    url = base_url + params

    try:
        # Make request
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')

        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())

            # Census API returns array format: [headers, ...data rows]
            if not data or len(data) < 2:
                return {
                    "error": "No data returned from Census API",
                    "url": url
                }

            headers = data[0]
            rows = data[1:]

            # Build evidence packet
            packet = {
                "packet_id": f"PKT-CENSUS-{hs_code}-{year}-{month or 'annual'}",
                "source": {
                    "type": "api",
                    "url": url,
                    "title": f"US Census Trade: HS {hs_code}, {year}" + (f"-{month:02d}" if month else ""),
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                    "collector": "trade-data"
                },
                "extractions": [
                    {
                        "claim": f"US import data for HS code {hs_code} in {year}" + (f" month {month}" if month else ""),
                        "evidence": json.dumps({"headers": headers, "data": rows[:10]}, indent=2),  # First 10 rows
                        "evidence_type": "table_slice",
                        "verification": {
                            "status": "supported"
                        }
                    }
                ],
                "metadata": {
                    "freshness": f"{year}-{month:02d}" if month else str(year),
                    "company_tags": [],
                    "topic_tags": ["trade", "imports", "census", f"hs-{hs_code}"]
                }
            }

            return packet

    except HTTPError as e:
        return {
            "error": f"HTTP error {e.code}: {e.reason}",
            "url": url,
            "note": "Census API may require API key for some queries. See https://api.census.gov/data/key_signup.html"
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
    parser = argparse.ArgumentParser(description='Fetch US Census Foreign Trade data')
    parser.add_argument('--hs-code', required=True, help='HS code (e.g., 847130)')
    parser.add_argument('--year', required=True, help='Year (e.g., 2024)')
    parser.add_argument('--month', type=int, help='Month (1-12, optional)')

    args = parser.parse_args()

    result = fetch_census_trade_data(args.hs_code, args.year, args.month)
    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()

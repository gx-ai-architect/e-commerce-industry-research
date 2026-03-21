#!/usr/bin/env python3
"""
Chinese Express Company Earnings Parser

Fetches parcel volume and revenue data from SEC EDGAR for US-listed Chinese
express delivery companies (ZTO Express). For Shanghai/Shenzhen-listed carriers
(YTO, Yunda, STO), uses WebSearch-compatible output format.

Usage:
  python3 scripts/tools/cn-express-earnings.py --carriers ZTO --output reports/pdd-holdings/evidence-packets/
  python3 scripts/tools/cn-express-earnings.py --carriers ZTO,YTO,Yunda

Output: Evidence packet JSON with parcel volumes, revenue, and growth rates.
"""

import argparse
import json
import sys
import os
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# SEC EDGAR CIK numbers for US-listed Chinese express companies
CARRIER_CIKS = {
    "ZTO": "0001684863",  # ZTO Express (Cayman) Inc.
}

# Non-EDGAR carriers (Shanghai/Shenzhen listed) — use WebSearch
NON_EDGAR_CARRIERS = {
    "YTO": {"stock": "600233.SS", "name_cn": "圆通速递"},
    "Yunda": {"stock": "002120.SZ", "name_cn": "韵达股份"},
    "STO": {"stock": "002468.SZ", "name_cn": "申通快递"},
    "SF": {"stock": "002352.SZ", "name_cn": "顺丰控股"},
    "Best": {"stock": "BEST", "name_cn": "百世集团"},
}

SEC_EDGAR_API = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

HEADERS = {
    "User-Agent": "EcommerceResearch/1.0 (research@example.com)",
    "Accept": "application/json",
}


def fetch_sec_edgar(cik):
    """Fetch XBRL company facts from SEC EDGAR."""
    url = SEC_EDGAR_API.format(cik=cik)
    req = Request(url, headers=HEADERS)
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (URLError, HTTPError) as e:
        print(f"Warning: Failed to fetch SEC EDGAR data for CIK {cik}: {e}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Warning: Invalid JSON from SEC EDGAR: {e}", file=sys.stderr)
        return None


def extract_parcel_volumes(edgar_data, carrier_name):
    """Extract parcel volume data from XBRL facts."""
    extractions = []

    if not edgar_data or "facts" not in edgar_data:
        return extractions

    facts = edgar_data.get("facts", {})

    # Search through all taxonomies for volume-related metrics
    for taxonomy_name, taxonomy in facts.items():
        for concept_name, concept_data in taxonomy.items():
            concept_lower = concept_name.lower()

            # Look for parcel/package volume metrics
            is_volume = any(term in concept_lower for term in [
                "parcel", "package", "volume", "numberofparcels",
                "expressdelivery", "shipment"
            ])

            # Look for revenue metrics
            is_revenue = any(term in concept_lower for term in [
                "revenue", "revenues", "netrevenue"
            ])

            if not (is_volume or is_revenue):
                continue

            units = concept_data.get("units", {})
            for unit_type, entries in units.items():
                # Get the most recent annual and quarterly entries
                annual_entries = [e for e in entries if e.get("form") in ("20-F", "10-K")]
                quarterly_entries = [e for e in entries if e.get("form") in ("6-K", "10-Q")]

                # Sort by end date descending
                for entry_set, period_type in [(annual_entries, "annual"), (quarterly_entries, "quarterly")]:
                    entry_set.sort(key=lambda x: x.get("end", ""), reverse=True)

                    for entry in entry_set[:4]:  # Last 4 periods
                        value = entry.get("val")
                        end_date = entry.get("end", "unknown")
                        start_date = entry.get("start", "")
                        form = entry.get("form", "")

                        if value is None:
                            continue

                        metric_type = "parcel volume" if is_volume else "revenue"
                        claim = f"{carrier_name} {metric_type} ({period_type}): {concept_name}"

                        if is_volume:
                            # Parcel volumes are often in millions or raw count
                            if value > 1_000_000_000:
                                display = f"{value/1_000_000_000:.2f} billion parcels"
                            elif value > 1_000_000:
                                display = f"{value/1_000_000:.1f} million parcels"
                            else:
                                display = f"{value:,} parcels"
                        else:
                            # Revenue in currency
                            if value > 1_000_000_000:
                                display = f"${value/1_000_000_000:.2f}B"
                            elif value > 1_000_000:
                                display = f"${value/1_000_000:.1f}M"
                            else:
                                display = f"${value:,.0f}"

                        evidence = f"{display} for period ending {end_date}"
                        if start_date:
                            evidence += f" (from {start_date})"
                        evidence += f" [Form: {form}]"

                        extractions.append({
                            "claim": claim,
                            "evidence": evidence,
                            "evidence_type": "table_slice",
                            "verification": {
                                "status": "supported",
                                "verifier_notes": f"Extracted from SEC EDGAR XBRL ({taxonomy_name}:{concept_name})"
                            }
                        })

    return extractions


def build_non_edgar_packet(carrier_name, carrier_info):
    """Build a stub packet for non-EDGAR carriers with search guidance."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    today = datetime.now().strftime("%Y%m%d")

    return {
        "packet_id": f"PKT-cnexpress-{carrier_name.lower()}-{today}",
        "source": {
            "type": "dataset",
            "url": f"https://finance.yahoo.com/quote/{carrier_info['stock']}/",
            "title": f"{carrier_name} ({carrier_info['name_cn']}) - Express Delivery Volumes",
            "retrieved_at": now,
            "collector": "cn-express-earnings"
        },
        "extractions": [
            {
                "claim": f"{carrier_name} ({carrier_info['name_cn']}) is listed on Shanghai/Shenzhen exchange",
                "evidence": f"Stock: {carrier_info['stock']}. Financial data not available via SEC EDGAR. "
                           f"Use WebSearch for '{carrier_info['name_cn']} 快递业务量 2025 2026' to find quarterly volume data.",
                "evidence_type": "computed_metric",
                "verification": {
                    "status": "extrapolated",
                    "verifier_notes": "Non-EDGAR carrier — requires WebSearch for volume data"
                }
            }
        ],
        "metadata": {
            "freshness": datetime.now().strftime("%Y-%m"),
            "company_tags": [carrier_name, carrier_info["name_cn"]],
            "topic_tags": ["logistics", "parcel-volume", "express-delivery", "china"]
        }
    }


def build_edgar_packet(carrier_name, cik, extractions):
    """Build an evidence packet from EDGAR data."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    today = datetime.now().strftime("%Y%m%d")

    if not extractions:
        extractions = [{
            "claim": f"{carrier_name} XBRL data fetched but no parcel volume metrics found",
            "evidence": f"SEC EDGAR XBRL data for CIK {cik} was fetched. Volume metrics may use "
                       f"non-standard taxonomy. Use WebSearch for '{carrier_name} parcel volume quarterly' as supplement.",
            "evidence_type": "computed_metric",
            "verification": {
                "status": "extrapolated",
                "verifier_notes": "XBRL data available but specific volume concepts not matched"
            }
        }]

    return {
        "packet_id": f"PKT-cnexpress-{carrier_name.lower()}-{today}",
        "source": {
            "type": "filing",
            "url": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=20-F",
            "title": f"{carrier_name} Express - SEC EDGAR Financial Data",
            "retrieved_at": now,
            "collector": "cn-express-earnings"
        },
        "extractions": extractions,
        "metadata": {
            "freshness": datetime.now().strftime("%Y-%m"),
            "company_tags": [carrier_name],
            "topic_tags": ["logistics", "parcel-volume", "express-delivery", "china", "sec-edgar"]
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Extract parcel volumes from Chinese express company filings"
    )
    parser.add_argument(
        "--carriers",
        required=True,
        help="Comma-separated carrier names (e.g., ZTO,YTO,Yunda)"
    )
    parser.add_argument(
        "--output",
        help="Output directory for evidence packets (default: stdout)"
    )

    args = parser.parse_args()

    carriers = [c.strip() for c in args.carriers.split(",")]
    all_packets = []

    for carrier in carriers:
        if carrier in CARRIER_CIKS:
            # US-listed — fetch from SEC EDGAR
            cik = CARRIER_CIKS[carrier]
            print(f"Fetching SEC EDGAR data for {carrier} (CIK: {cik})...", file=sys.stderr)
            edgar_data = fetch_sec_edgar(cik)
            extractions = extract_parcel_volumes(edgar_data, carrier) if edgar_data else []
            packet = build_edgar_packet(carrier, cik, extractions)
            all_packets.append(packet)
        elif carrier in NON_EDGAR_CARRIERS:
            # China-listed — build stub with search guidance
            print(f"Building stub for {carrier} (China-listed, not on EDGAR)...", file=sys.stderr)
            packet = build_non_edgar_packet(carrier, NON_EDGAR_CARRIERS[carrier])
            all_packets.append(packet)
        else:
            print(f"Warning: Unknown carrier '{carrier}'. Known EDGAR: {list(CARRIER_CIKS.keys())}. "
                  f"Known non-EDGAR: {list(NON_EDGAR_CARRIERS.keys())}", file=sys.stderr)

    if not all_packets:
        print("Error: No carrier data collected", file=sys.stderr)
        sys.exit(1)

    output_json = json.dumps(all_packets, indent=2, ensure_ascii=False)

    if args.output:
        os.makedirs(args.output, exist_ok=True)
        today = datetime.now().strftime("%Y%m%d")
        filename = f"logistics-cn-express-{today}.json"
        filepath = os.path.join(args.output, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(output_json + "\n")
        print(f"Wrote: {filepath}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()

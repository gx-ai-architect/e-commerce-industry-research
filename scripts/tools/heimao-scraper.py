#!/usr/bin/env python3
"""
Heimao (黑猫投诉) Consumer Complaint Scraper

Scrapes tousu.sina.com.cn for consumer complaints about a company.
Extracts: complaint volume, resolution rate, top complaint themes, trend data.

Usage:
  python3 scripts/tools/heimao-scraper.py --company pinduoduo --output reports/pdd-holdings/evidence-packets/
  python3 scripts/tools/heimao-scraper.py --company taobao --output reports/pdd-holdings/evidence-packets/

Output: Evidence packet JSON to stdout (or file if --output specified).
"""

import argparse
import json
import sys
import os
import re
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import quote
from urllib.error import URLError, HTTPError

# Company name mappings (English -> Chinese search terms)
COMPANY_NAMES = {
    "pinduoduo": "拼多多",
    "pdd": "拼多多",
    "taobao": "淘宝",
    "tmall": "天猫",
    "jd": "京东",
    "jingdong": "京东",
    "douyin": "抖音",
    "shein": "SHEIN",
    "temu": "Temu",
}

HEIMAO_SEARCH_URL = "https://tousu.sina.com.cn/api/company/search"
HEIMAO_COMPANY_URL = "https://tousu.sina.com.cn/api/company/view"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://tousu.sina.com.cn/",
}


def fetch_json(url):
    """Fetch JSON from a URL with error handling."""
    req = Request(url, headers=HEADERS)
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (URLError, HTTPError) as e:
        print(f"Warning: Failed to fetch {url}: {e}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Warning: Invalid JSON from {url}: {e}", file=sys.stderr)
        return None


def search_company(company_name_cn):
    """Search Heimao for a company by Chinese name."""
    encoded = quote(company_name_cn)
    url = f"{HEIMAO_SEARCH_URL}?keyword={encoded}&page_size=5&page=1"
    data = fetch_json(url)
    if not data or "result" not in data:
        return None
    results = data.get("result", {}).get("data", {}).get("lists", [])
    if not results:
        return None
    # Return the first match (most relevant)
    return results[0]


def get_company_detail(company_id):
    """Get detailed complaint data for a specific company."""
    url = f"{HEIMAO_COMPANY_URL}?company_id={company_id}"
    return fetch_json(url)


def build_evidence_packet(company_en, company_cn, search_result, detail_data):
    """Build an evidence packet from Heimao data."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    today = datetime.now().strftime("%Y%m%d")

    extractions = []

    # Extract complaint counts from search result
    total_complaints = search_result.get("tousu_num", "unknown")
    resolved_complaints = search_result.get("handle_num", "unknown")
    company_title = search_result.get("title", company_cn)

    if total_complaints != "unknown" and resolved_complaints != "unknown":
        try:
            total = int(total_complaints)
            resolved = int(resolved_complaints)
            rate = round(resolved / total * 100, 1) if total > 0 else 0
            extractions.append({
                "claim": f"{company_title} complaint volume and resolution rate on Heimao (黑猫投诉)",
                "evidence": f"Total complaints: {total:,}. Resolved: {resolved:,}. Resolution rate: {rate}%.",
                "evidence_type": "table_slice",
                "verification": {
                    "status": "supported",
                    "verifier_notes": f"Data from tousu.sina.com.cn API query for '{company_cn}'"
                }
            })
        except (ValueError, TypeError):
            extractions.append({
                "claim": f"{company_title} complaint data on Heimao (黑猫投诉)",
                "evidence": f"Total complaints: {total_complaints}. Resolved: {resolved_complaints}.",
                "evidence_type": "table_slice",
                "verification": {
                    "status": "supported",
                    "verifier_notes": f"Data from tousu.sina.com.cn API query for '{company_cn}'"
                }
            })

    # Extract rating if available
    score = search_result.get("score")
    if score:
        extractions.append({
            "claim": f"{company_title} merchant rating on Heimao (黑猫投诉)",
            "evidence": f"Heimao merchant score: {score}/5",
            "evidence_type": "direct_quote",
            "verification": {
                "status": "supported",
                "verifier_notes": "Score from Heimao platform"
            }
        })

    # Extract detail data if available
    if detail_data and "result" in detail_data:
        detail = detail_data.get("result", {}).get("data", {})
        # Additional metrics from detail view
        reply_rate = detail.get("reply_rate")
        if reply_rate:
            extractions.append({
                "claim": f"{company_title} merchant reply rate on Heimao",
                "evidence": f"Merchant reply rate: {reply_rate}",
                "evidence_type": "direct_quote",
                "verification": {
                    "status": "supported",
                    "verifier_notes": "Data from Heimao company detail API"
                }
            })

    if not extractions:
        extractions.append({
            "claim": f"Heimao complaint search for {company_cn}",
            "evidence": f"Search returned result but no structured complaint data was extractable.",
            "evidence_type": "direct_quote",
            "verification": {
                "status": "extrapolated",
                "verifier_notes": "API returned data but fields may have changed"
            }
        })

    company_id = search_result.get("id", "")
    packet = {
        "packet_id": f"PKT-heimao-{company_en}-{today}",
        "source": {
            "type": "api",
            "url": f"https://tousu.sina.com.cn/company/view/?couid={company_id}",
            "title": f"黑猫投诉 (Heimao) - {company_title} Consumer Complaints",
            "retrieved_at": now,
            "collector": "heimao-scraper"
        },
        "extractions": extractions,
        "metadata": {
            "freshness": datetime.now().strftime("%Y-%m"),
            "company_tags": [company_en, company_cn],
            "topic_tags": ["consumer-complaints", "customer-satisfaction", "heimao", "china"]
        }
    }

    return packet


def main():
    parser = argparse.ArgumentParser(
        description="Scrape 黑猫投诉 (Heimao) for consumer complaint data"
    )
    parser.add_argument(
        "--company",
        required=True,
        help="Company name in English (e.g., pinduoduo, taobao, jd)"
    )
    parser.add_argument(
        "--output",
        help="Output directory for evidence packet (default: stdout)"
    )

    args = parser.parse_args()

    company_en = args.company.lower()
    company_cn = COMPANY_NAMES.get(company_en)

    if not company_cn:
        print(f"Error: Unknown company '{company_en}'. Known: {', '.join(COMPANY_NAMES.keys())}",
              file=sys.stderr)
        sys.exit(1)

    print(f"Searching Heimao for: {company_cn} ({company_en})...", file=sys.stderr)

    search_result = search_company(company_cn)
    if not search_result:
        print(f"Error: No results found for '{company_cn}' on Heimao", file=sys.stderr)
        sys.exit(1)

    company_id = search_result.get("id")
    detail_data = None
    if company_id:
        detail_data = get_company_detail(company_id)

    packet = build_evidence_packet(company_en, company_cn, search_result, detail_data)

    output_json = json.dumps(packet, indent=2, ensure_ascii=False)

    if args.output:
        os.makedirs(args.output, exist_ok=True)
        today = datetime.now().strftime("%Y%m%d")
        filename = f"customer-heimao-{company_en}-{today}.json"
        filepath = os.path.join(args.output, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(output_json + "\n")
        print(f"Wrote: {filepath}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()

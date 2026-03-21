#!/usr/bin/env python3
"""
Price Intelligence Script
Compares product prices across e-commerce platforms (Temu, Amazon, Shein, AliExpress)
"""

import argparse
import json
import sys
import warnings
from datetime import datetime, timezone
from typing import List, Dict, Any
import urllib.parse
import re

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    import requests
except ImportError:
    print(json.dumps({
        "error": "requests library not installed. Install with: pip install requests",
        "packet_id": "PKT-PRICE-ERROR",
        "source": {"type": "error", "collector": "price-intel"}
    }), file=sys.stderr)
    sys.exit(1)


def generate_packet_id(query: str) -> str:
    """Generate unique packet ID for this query"""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    query_hash = abs(hash(query)) % 10000
    return f"PKT-PRICE-{timestamp}-{query_hash:04d}"


def fetch_temu_prices(query: str) -> List[Dict[str, Any]]:
    """Attempt to fetch product prices from Temu"""
    url = f"https://www.temu.com/search_result.html?search_key={urllib.parse.quote(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 403:
            return [{"error": "blocked", "status": 403, "platform": "temu"}]

        response.raise_for_status()

        # Simple regex-based price extraction (Temu often uses $ followed by numbers)
        # This is a basic approach - real implementation would need HTML parsing
        prices = re.findall(r'\$(\d+\.?\d*)', response.text[:50000])  # Search first 50KB

        if prices:
            products = []
            for i, price in enumerate(prices[:10]):  # Take first 10 prices found
                try:
                    products.append({
                        "name": f"Product {i+1} - {query}",
                        "price": float(price),
                        "platform": "temu"
                    })
                except ValueError:
                    continue
            return products if products else [{"error": "no_prices_found", "platform": "temu"}]

        return [{"error": "no_prices_found", "platform": "temu"}]

    except requests.RequestException as e:
        return [{"error": str(e), "platform": "temu"}]


def fetch_amazon_prices(query: str) -> List[Dict[str, Any]]:
    """Attempt to fetch product prices from Amazon"""
    url = f"https://www.amazon.com/s?k={urllib.parse.quote(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 403:
            return [{"error": "blocked", "status": 403, "platform": "amazon"}]

        response.raise_for_status()

        # Amazon price pattern (often in format $XX.XX)
        prices = re.findall(r'\$(\d+\.?\d*)', response.text[:50000])

        if prices:
            products = []
            for i, price in enumerate(prices[:10]):
                try:
                    products.append({
                        "name": f"Product {i+1} - {query}",
                        "price": float(price),
                        "platform": "amazon"
                    })
                except ValueError:
                    continue
            return products if products else [{"error": "no_prices_found", "platform": "amazon"}]

        return [{"error": "no_prices_found", "platform": "amazon"}]

    except requests.RequestException as e:
        return [{"error": str(e), "platform": "amazon"}]


def fetch_shein_prices(query: str) -> List[Dict[str, Any]]:
    """Attempt to fetch product prices from Shein"""
    url = f"https://us.shein.com/pdsearch/{urllib.parse.quote(query)}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 403:
            return [{"error": "blocked", "status": 403, "platform": "shein"}]

        response.raise_for_status()

        # Shein price pattern
        prices = re.findall(r'\$(\d+\.?\d*)', response.text[:50000])

        if prices:
            products = []
            for i, price in enumerate(prices[:10]):
                try:
                    products.append({
                        "name": f"Product {i+1} - {query}",
                        "price": float(price),
                        "platform": "shein"
                    })
                except ValueError:
                    continue
            return products if products else [{"error": "no_prices_found", "platform": "shein"}]

        return [{"error": "no_prices_found", "platform": "shein"}]

    except requests.RequestException as e:
        return [{"error": str(e), "platform": "shein"}]


def compute_metrics(all_products: List[Dict[str, Any]], platforms_queried: List[str]) -> Dict[str, Any]:
    """Compute average prices and price gaps"""
    platform_prices = {}
    blocked_platforms = []
    error_platforms = []

    # Group prices by platform
    for product in all_products:
        platform = product.get("platform")
        if "error" in product:
            if product.get("status") == 403 or product.get("error") == "blocked":
                blocked_platforms.append(platform)
            else:
                error_platforms.append(platform)
        elif "price" in product:
            if platform not in platform_prices:
                platform_prices[platform] = []
            platform_prices[platform].append(product["price"])

    # Compute averages
    averages = {}
    for platform, prices in platform_prices.items():
        if prices:
            averages[platform] = sum(prices) / len(prices)

    # Find cheapest
    cheapest = None
    if averages:
        cheapest = min(averages, key=averages.get)

    # Compute price gaps
    gaps = {}
    if cheapest and len(averages) > 1:
        cheapest_price = averages[cheapest]
        for platform, avg_price in averages.items():
            if platform != cheapest:
                gap_pct = ((avg_price - cheapest_price) / cheapest_price) * 100
                gaps[platform] = round(gap_pct, 1)

    return {
        "averages": {k: round(v, 2) for k, v in averages.items()},
        "cheapest": cheapest,
        "price_gaps_pct": gaps,
        "blocked_platforms": blocked_platforms,
        "error_platforms": error_platforms,
        "total_products_found": len([p for p in all_products if "price" in p])
    }


def create_evidence_packet(query: str, platforms: List[str], all_products: List[Dict[str, Any]], metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Create standardized evidence packet"""
    packet_id = generate_packet_id(query)
    timestamp = datetime.now(timezone.utc).isoformat() + "Z"

    # Build extractions
    extractions = []

    # Add average price claims
    for platform, avg_price in metrics["averages"].items():
        extractions.append({
            "claim": f"Average price for '{query}' on {platform.upper()}: ${avg_price:.2f}",
            "evidence": f"Computed from {len([p for p in all_products if p.get('platform') == platform and 'price' in p])} products",
            "evidence_type": "computed_metric"
        })

    # Add cheapest platform claim
    if metrics["cheapest"]:
        gaps_text = ", ".join([f"{p}: +{g}%" for p, g in metrics["price_gaps_pct"].items()])
        extractions.append({
            "claim": f"Cheapest platform: {metrics['cheapest'].upper()} (${metrics['averages'][metrics['cheapest']]:.2f})",
            "evidence": f"Price gaps vs competitors: {gaps_text}" if gaps_text else "No competitors with valid data",
            "evidence_type": "computed_metric"
        })

    # Add verifier notes for blocked/error platforms
    verifier_notes = []
    if metrics["blocked_platforms"]:
        verifier_notes.append(f"Blocked by anti-bot (403): {', '.join(metrics['blocked_platforms'])}")
    if metrics["error_platforms"]:
        verifier_notes.append(f"Errors encountered: {', '.join(metrics['error_platforms'])}")

    if not extractions:
        extractions.append({
            "claim": "Unable to extract pricing data",
            "evidence": f"All platforms blocked or errored. Platforms queried: {', '.join(platforms)}",
            "evidence_type": "error"
        })

    # Determine company tags
    company_tags = []
    if "temu" in platforms:
        company_tags.append("TEMU")
    if "amazon" in platforms:
        company_tags.append("AMZN")
    if "shein" in platforms:
        company_tags.append("SHEIN")

    packet = {
        "packet_id": packet_id,
        "source": {
            "type": "dataset",
            "url": f"cross-platform search: {query}",
            "title": f"Cross-platform price comparison: {query}",
            "retrieved_at": timestamp,
            "collector": "price-intel"
        },
        "extractions": extractions,
        "metadata": {
            "freshness": "real-time",
            "company_tags": company_tags,
            "topic_tags": ["pricing", "competitive-analysis"],
            "platforms_queried": platforms,
            "platforms_blocked": metrics["blocked_platforms"],
            "total_products": metrics["total_products_found"]
        }
    }

    if verifier_notes:
        packet["verifier_notes"] = verifier_notes

    return packet


def main():
    parser = argparse.ArgumentParser(description="Compare product prices across e-commerce platforms")
    parser.add_argument("--query", required=True, help="Product search query")
    parser.add_argument("--platforms", default="temu,amazon,shein",
                       help="Comma-separated platforms (default: temu,amazon,shein)")

    args = parser.parse_args()

    query = args.query
    platforms = [p.strip().lower() for p in args.platforms.split(",")]

    # Fetch prices from each platform
    all_products = []

    if "temu" in platforms:
        all_products.extend(fetch_temu_prices(query))

    if "amazon" in platforms:
        all_products.extend(fetch_amazon_prices(query))

    if "shein" in platforms:
        all_products.extend(fetch_shein_prices(query))

    # Compute metrics
    metrics = compute_metrics(all_products, platforms)

    # Create evidence packet
    packet = create_evidence_packet(query, platforms, all_products, metrics)

    # Output JSON
    print(json.dumps(packet, indent=2))


if __name__ == "__main__":
    main()

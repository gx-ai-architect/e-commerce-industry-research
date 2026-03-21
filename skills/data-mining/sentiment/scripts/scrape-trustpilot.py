#!/usr/bin/env python3
"""
Scrape Trustpilot reviews for a given domain.
Outputs evidence packets in JSON format.
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from urllib.parse import quote

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Missing dependencies. Install with: pip3 install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)


def scrape_trustpilot(domain):
    """Scrape Trustpilot page for domain."""
    url = f"https://www.trustpilot.com/review/{domain}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch Trustpilot page: {e}"}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract overall rating
    rating_elem = soup.select_one('[data-rating-typography="true"]')
    rating = rating_elem.text.strip() if rating_elem else "N/A"

    # Extract total reviews
    reviews_elem = soup.select_one('p[data-reviews-count-typography="true"]')
    total_reviews = reviews_elem.text.strip() if reviews_elem else "N/A"

    # Extract star distribution
    star_distribution = {}
    star_filters = soup.select('label[for^="review-filter-"]')
    for star_filter in star_filters[:5]:  # Only first 5 (5-star to 1-star)
        text = star_filter.text.strip()
        if text:
            star_distribution[text] = text

    # Extract recent review excerpts
    review_cards = soup.select('article[data-service-review-card-paper="true"]')[:5]
    review_excerpts = []

    for card in review_cards:
        title_elem = card.select_one('h2[data-service-review-title-typography="true"]')
        text_elem = card.select_one('p[data-service-review-text-typography="true"]')
        rating_elem = card.select_one('div[data-service-review-rating]')

        if title_elem or text_elem:
            excerpt = {
                "title": title_elem.text.strip() if title_elem else "",
                "text": text_elem.text.strip() if text_elem else "",
                "rating": rating_elem.get('data-service-review-rating', 'N/A') if rating_elem else 'N/A'
            }
            review_excerpts.append(excerpt)

    # Build evidence packet
    packet = {
        "packet_id": f"TP-{domain}-{int(time.time())}",
        "source": {
            "type": "article",
            "url": url,
            "title": f"Trustpilot Reviews for {domain}",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "collector": "sentiment"
        },
        "extractions": [
            {
                "claim": f"{domain} has {rating} rating on Trustpilot with {total_reviews}",
                "evidence": f"Rating: {rating}, Total Reviews: {total_reviews}",
                "evidence_type": "direct_quote"
            }
        ],
        "metadata": {
            "freshness": datetime.now(timezone.utc).strftime("%Y-%m"),
            "company_tags": ["domain:" + domain],
            "topic_tags": ["sentiment", "reviews", "trustpilot"]
        }
    }

    # Add star distribution if available
    if star_distribution:
        packet["extractions"].append({
            "claim": f"Star distribution for {domain}",
            "evidence": json.dumps(star_distribution),
            "evidence_type": "computed_metric"
        })

    # Add review excerpts
    for i, review in enumerate(review_excerpts, 1):
        if review["title"] or review["text"]:
            packet["extractions"].append({
                "claim": f"Review excerpt #{i}: {review['title'][:50]}...",
                "evidence": f"Rating: {review['rating']}, Title: {review['title']}, Text: {review['text'][:200]}",
                "evidence_type": "direct_quote"
            })

    return packet


def main():
    parser = argparse.ArgumentParser(description="Scrape Trustpilot reviews")
    parser.add_argument("--domain", required=True, help="Domain to scrape (e.g., temu.com)")
    args = parser.parse_args()

    result = scrape_trustpilot(args.domain)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

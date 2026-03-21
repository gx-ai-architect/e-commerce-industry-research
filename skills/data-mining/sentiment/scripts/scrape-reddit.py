#!/usr/bin/env python3
"""
Scrape Reddit posts using the JSON API.
Outputs evidence packets in JSON format.
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    print("ERROR: Missing dependencies. Install with: pip3 install requests", file=sys.stderr)
    sys.exit(1)


def scrape_reddit(subreddit, query=None, limit=25):
    """Scrape Reddit posts from subreddit."""
    headers = {
        'User-Agent': 'E-Commerce-Research/1.0 (data-mining; +https://github.com/gx-ai-architect)'
    }

    # Try subreddit first, fall back to search
    urls = [
        f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}",
        f"https://www.reddit.com/search.json?q={subreddit}&limit={limit}&sort=new"
    ]

    data = None
    used_url = None
    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                used_url = url
                break
        except (requests.RequestException, json.JSONDecodeError):
            continue

    if data is None:
        return {"error": f"Failed to fetch Reddit data for '{subreddit}' from both subreddit and search endpoints"}

    posts = data.get('data', {}).get('children', [])

    if not posts:
        return {"error": "No posts found"}

    # Build evidence packet
    packet = {
        "packet_id": f"REDDIT-{subreddit}-{int(time.time())}",
        "source": {
            "type": "dataset",
            "url": f"https://www.reddit.com/r/{subreddit}/",
            "title": f"Reddit r/{subreddit} Hot Posts",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "collector": "sentiment"
        },
        "extractions": [],
        "metadata": {
            "freshness": datetime.now(timezone.utc).strftime("%Y-%m"),
            "company_tags": [],
            "topic_tags": ["sentiment", "reddit", subreddit]
        }
    }

    # Extract top posts
    for i, post in enumerate(posts[:10], 1):
        post_data = post.get('data', {})
        title = post_data.get('title', '')
        score = post_data.get('score', 0)
        num_comments = post_data.get('num_comments', 0)
        permalink = post_data.get('permalink', '')

        # Filter by query if provided
        if query and query.lower() not in title.lower():
            continue

        # Simple sentiment keywords
        positive_words = ['great', 'good', 'love', 'amazing', 'excellent', 'best', 'awesome', 'happy']
        negative_words = ['bad', 'terrible', 'hate', 'worst', 'scam', 'fraud', 'poor', 'awful', 'disappointed']

        title_lower = title.lower()
        sentiment = "neutral"
        if any(word in title_lower for word in positive_words):
            sentiment = "positive"
        elif any(word in title_lower for word in negative_words):
            sentiment = "negative"

        packet["extractions"].append({
            "claim": f"Reddit post #{i}: {title[:60]}...",
            "evidence": f"Title: {title}, Score: {score}, Comments: {num_comments}, Sentiment: {sentiment}, URL: https://reddit.com{permalink}",
            "evidence_type": "direct_quote"
        })

    # Summary stats
    total_score = sum(p.get('data', {}).get('score', 0) for p in posts[:10])
    total_comments = sum(p.get('data', {}).get('num_comments', 0) for p in posts[:10])

    packet["extractions"].insert(0, {
        "claim": f"Top 10 posts on r/{subreddit} have {total_score} combined score and {total_comments} comments",
        "evidence": f"Total upvotes: {total_score}, Total comments: {total_comments}",
        "evidence_type": "computed_metric"
    })

    return packet


def main():
    parser = argparse.ArgumentParser(description="Scrape Reddit posts")
    parser.add_argument("--subreddit", required=True, help="Subreddit to scrape (e.g., Temu)")
    parser.add_argument("--query", help="Filter posts by query string")
    parser.add_argument("--limit", type=int, default=25, help="Number of posts to fetch (default: 25)")
    args = parser.parse_args()

    result = scrape_reddit(args.subreddit, args.query, args.limit)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

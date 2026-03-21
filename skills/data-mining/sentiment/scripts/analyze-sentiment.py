#!/usr/bin/env python3
"""
Simple keyword-based sentiment analysis.
Reads text from stdin or --text argument.
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone


def analyze_sentiment(text):
    """Perform simple keyword-based sentiment analysis."""

    # Keyword lists
    positive_words = [
        'great', 'good', 'love', 'amazing', 'excellent', 'best', 'awesome',
        'happy', 'fantastic', 'wonderful', 'perfect', 'satisfied', 'recommend',
        'fast', 'quality', 'impressed', 'pleased', 'glad', 'enjoy'
    ]

    negative_words = [
        'bad', 'terrible', 'hate', 'worst', 'scam', 'fraud', 'poor', 'awful',
        'disappointed', 'never', 'horrible', 'useless', 'waste', 'slow',
        'broken', 'defective', 'fake', 'counterfeit', 'cheap', 'garbage'
    ]

    text_lower = text.lower()
    words = text_lower.split()

    # Count occurrences
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    # Calculate sentiment score (-1 to 1)
    total_count = positive_count + negative_count
    if total_count == 0:
        sentiment_score = 0.0
        sentiment_label = "neutral"
    else:
        sentiment_score = (positive_count - negative_count) / total_count
        if sentiment_score > 0.2:
            sentiment_label = "positive"
        elif sentiment_score < -0.2:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"

    # Find key phrases
    key_positive = [word for word in positive_words if word in text_lower]
    key_negative = [word for word in negative_words if word in text_lower]

    # Build evidence packet
    packet = {
        "packet_id": f"SENTIMENT-{int(time.time())}",
        "source": {
            "type": "dataset",
            "url": "stdin",
            "title": "Sentiment Analysis Result",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "collector": "sentiment"
        },
        "extractions": [
            {
                "claim": f"Text sentiment is {sentiment_label} (score: {sentiment_score:.2f})",
                "evidence": f"Positive keywords: {', '.join(key_positive[:5]) if key_positive else 'none'}, Negative keywords: {', '.join(key_negative[:5]) if key_negative else 'none'}",
                "evidence_type": "computed_metric"
            },
            {
                "claim": f"Sentiment breakdown: {positive_count} positive, {negative_count} negative keywords",
                "evidence": f"Total sentiment keywords: {total_count}",
                "evidence_type": "computed_metric"
            }
        ],
        "metadata": {
            "freshness": datetime.now(timezone.utc).strftime("%Y-%m"),
            "company_tags": [],
            "topic_tags": ["sentiment", "analysis"]
        }
    }

    return packet


def main():
    parser = argparse.ArgumentParser(description="Analyze sentiment of text")
    parser.add_argument("--text", help="Text to analyze (or read from stdin)")
    args = parser.parse_args()

    if args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    if not text.strip():
        print(json.dumps({"error": "No text provided"}), file=sys.stderr)
        sys.exit(1)

    result = analyze_sentiment(text)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Extract structured claims from raw data sources.

Takes raw text/data and extracts key claims with supporting evidence.
Outputs evidence packet JSON to stdout.
"""

import argparse
import json
import sys
from datetime import datetime
import re


def extract_from_filing(raw_text, url, title, collector):
    """Extract claims from SEC filings or similar regulatory documents."""
    extractions = []

    # Simple pattern-based extraction for financial metrics
    # In production, this would use LLM-based extraction

    # Look for revenue statements
    revenue_patterns = [
        r'(?:total\s+)?revenues?\s+(?:were|was|of)\s+(?:RMB\s+)?[\d,.]+ (?:billion|million)',
        r'revenue\s+(?:increased|decreased|grew)\s+\d+%',
    ]

    for pattern in revenue_patterns:
        matches = re.finditer(pattern, raw_text, re.IGNORECASE)
        for match in matches:
            # Extract surrounding context (100 chars before and after)
            start = max(0, match.start() - 100)
            end = min(len(raw_text), match.end() + 100)
            context = raw_text[start:end].strip()

            extractions.append({
                "claim": match.group(0),
                "evidence": context,
                "evidence_type": "direct_quote"
            })

    # Limit to first 10 extractions to avoid overwhelming output
    return extractions[:10] if extractions else [{
        "claim": "No structured data extracted (placeholder)",
        "evidence": raw_text[:500] if len(raw_text) > 500 else raw_text,
        "evidence_type": "direct_quote"
    }]


def extract_from_article(raw_text, url, title, collector):
    """Extract claims from news articles."""
    # Simplified extraction - look for key statements
    sentences = raw_text.split('.')
    extractions = []

    for sentence in sentences[:5]:  # First 5 sentences
        if len(sentence.strip()) > 20:
            extractions.append({
                "claim": sentence.strip(),
                "evidence": sentence.strip(),
                "evidence_type": "direct_quote"
            })

    return extractions if extractions else [{
        "claim": "Article content",
        "evidence": raw_text[:500],
        "evidence_type": "direct_quote"
    }]


def extract_from_dataset(raw_text, url, title, collector):
    """Extract claims from structured datasets."""
    return [{
        "claim": "Dataset imported",
        "evidence": raw_text[:500],
        "evidence_type": "table_slice"
    }]


def extract_from_api(raw_text, url, title, collector):
    """Extract claims from API responses."""
    try:
        data = json.loads(raw_text)
        # Extract key metrics from JSON
        return [{
            "claim": f"API data: {json.dumps(data)[:100]}",
            "evidence": raw_text[:500],
            "evidence_type": "computed_metric"
        }]
    except json.JSONDecodeError:
        return [{
            "claim": "API response",
            "evidence": raw_text[:500],
            "evidence_type": "direct_quote"
        }]


def extract_from_table(raw_text, url, title, collector):
    """Extract claims from table data."""
    return [{
        "claim": "Table data extracted",
        "evidence": raw_text[:500],
        "evidence_type": "table_slice"
    }]


def extract_from_image(raw_text, url, title, collector):
    """Extract claims from image analysis (OCR, object detection, etc.)."""
    return [{
        "claim": "Image analysis result",
        "evidence": raw_text[:500],
        "evidence_type": "direct_quote"
    }]


EXTRACTORS = {
    'filing': extract_from_filing,
    'article': extract_from_article,
    'dataset': extract_from_dataset,
    'api': extract_from_api,
    'table': extract_from_table,
    'image': extract_from_image,
}


def main():
    parser = argparse.ArgumentParser(description='Extract claims from raw data')
    parser.add_argument('--source-type', required=True,
                        choices=EXTRACTORS.keys(),
                        help='Type of source data')
    parser.add_argument('--url', required=True, help='Source URL')
    parser.add_argument('--title', required=True, help='Source title')
    parser.add_argument('--collector', required=True, help='Collector skill name')
    parser.add_argument('--file', help='Input file (default: stdin)')
    parser.add_argument('--packet-id', help='Packet ID (default: auto-generate)')

    args = parser.parse_args()

    # Read input
    if args.file:
        with open(args.file, 'r') as f:
            raw_text = f.read()
    else:
        raw_text = sys.stdin.read()

    # Extract claims
    extractor = EXTRACTORS[args.source_type]
    extractions = extractor(raw_text, args.url, args.title, args.collector)

    # Build evidence packet
    packet_id = args.packet_id or f"PKT-{abs(hash(args.url)) % 1000000:06d}"

    packet = {
        "packet_id": packet_id,
        "source": {
            "type": args.source_type,
            "url": args.url,
            "title": args.title,
            "retrieved_at": datetime.utcnow().isoformat() + 'Z',
            "collector": args.collector
        },
        "extractions": extractions,
        "metadata": {
            "freshness": "Current as of " + datetime.utcnow().strftime('%Y-%m-%d'),
            "company_tags": [],
            "topic_tags": []
        }
    }

    # Output JSON
    print(json.dumps(packet, indent=2))


if __name__ == '__main__':
    main()

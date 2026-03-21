# Sentiment Analysis Mining Skill

## Overview
Scrapes sentiment data from Trustpilot and Reddit to gauge public opinion about e-commerce platforms.

## Scripts

### scrape-trustpilot.py
Scrapes Trustpilot review pages.

**Usage:**
```bash
./scripts/scrape-trustpilot.py --domain temu.com
```

**Output:** Evidence packet with ratings, review counts, star distribution, and recent review excerpts.

**Dependencies:** `pip3 install requests beautifulsoup4`

### scrape-reddit.py
Scrapes Reddit posts using the free JSON API.

**Usage:**
```bash
./scripts/scrape-reddit.py --subreddit Temu --limit 25
./scripts/scrape-reddit.py --subreddit Temu --query "shipping"
```

**Output:** Evidence packet with post titles, scores, comment counts, and basic sentiment labels.

**Dependencies:** `pip3 install requests`

### analyze-sentiment.py
Simple keyword-based sentiment analysis.

**Usage:**
```bash
echo "This product is amazing and fast shipping!" | ./scripts/analyze-sentiment.py
./scripts/analyze-sentiment.py --text "Terrible quality, total scam"
```

**Output:** Evidence packet with sentiment score (-1 to 1) and key phrases.

**Dependencies:** None (stdlib only)

## Tests

```bash
./test/test-reddit.sh
./test/test-trustpilot.sh
```

## Evidence Packet Schema
All scripts output standardized evidence packets:
```json
{
  "packet_id": "TP-temu.com-1234567890",
  "source": {
    "type": "article",
    "url": "https://...",
    "title": "...",
    "retrieved_at": "2026-03-19T14:30:00Z",
    "collector": "sentiment"
  },
  "extractions": [
    {
      "claim": "...",
      "evidence": "...",
      "evidence_type": "direct_quote | computed_metric"
    }
  ],
  "metadata": {
    "freshness": "2026-03",
    "company_tags": ["PDD"],
    "topic_tags": ["sentiment", "reviews"]
  }
}
```

## Tier
**Tier 2-3**: Basic web scraping with free APIs. May be blocked by anti-bot measures.

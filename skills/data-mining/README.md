# Data Mining Skills - Tier 2-3

Alternative data collection skills for e-commerce industry research. These skills mine non-traditional data sources to provide unique insights into company operations and market trends.

## Overview

This directory contains 5 data mining skills:

1. **Sentiment** - Public opinion analysis via Trustpilot and Reddit
2. **Vessel Tracking** - Shipping and logistics monitoring via AIS data
3. **Satellite** - Infrastructure monitoring via Sentinel-2 imagery
4. **Datacenter Monitor** - Datacenter construction tracking (composite skill)
5. **Web Scraper** - Generic web scraping utility

All skills output **standardized evidence packets** in JSON format.

## Evidence Packet Schema

Every skill outputs this format:

```json
{
  "packet_id": "UNIQUE-ID",
  "source": {
    "type": "table | article | filing | dataset | api | image",
    "url": "https://...",
    "title": "...",
    "retrieved_at": "2026-03-19T14:30:00Z",
    "collector": "skill-name"
  },
  "extractions": [
    {
      "claim": "...",
      "evidence": "...",
      "evidence_type": "direct_quote | table_slice | computed_metric"
    }
  ],
  "metadata": {
    "freshness": "2026-03",
    "company_tags": ["PDD"],
    "topic_tags": ["sentiment", "reviews"]
  }
}
```

## Skills Summary

### 1. Sentiment (READY)
**Status:** READY (may be blocked by anti-bot)

**Scripts:**
- `scrape-trustpilot.py` - Trustpilot reviews
- `scrape-reddit.py` - Reddit posts via JSON API
- `analyze-sentiment.py` - Keyword-based sentiment analysis

**Dependencies:** `requests`, `beautifulsoup4`

**Use Cases:**
- Monitor brand reputation
- Track customer satisfaction trends
- Identify product issues
- Gauge platform sentiment

### 2. Vessel Tracking (BLOCKED)
**Status:** BLOCKED (requires API keys)

**Scripts:**
- `fetch-ais.py` - AIS vessel tracking data

**Dependencies:** `requests`

**Limitations:**
- Free APIs require registration (AISHub)
- Most providers require paid subscriptions
- Web scraping would violate ToS

**Use Cases:**
- Monitor shipping volumes
- Track logistics routes
- Estimate transit times
- Identify supply chain bottlenecks

### 3. Satellite (READY)
**Status:** READY (catalog only, no image processing)

**Scripts:**
- `fetch-sentinel2.py` - Copernicus Sentinel-2 imagery metadata

**Dependencies:** `requests`

**Data Source:** Copernicus Data Space (FREE, open access, 10m resolution)

**Use Cases:**
- Monitor warehouse construction
- Track datacenter expansion
- Detect infrastructure changes
- Measure parking lot occupancy

**Note:** This queries imagery metadata, not actual images. Image processing requires specialized tools (GDAL, rasterio).

### 4. Datacenter Monitor (WIP)
**Status:** WIP (composite skill, needs integration)

**Scripts:**
- `monitor-datacenter.py` - Framework for datacenter monitoring

**Dependencies:** `requests` + satellite skill + FOIA skill

**Data Sources:**
- Building permit databases (manual, city-specific)
- Satellite imagery (via satellite skill)
- Power utility applications (via FOIA skill, currently BLOCKED)
- Public announcements

**Use Cases:**
- Track cloud infrastructure expansion
- Estimate regional capacity growth
- Identify new datacenter markets

### 5. Web Scraper (READY)
**Status:** READY (basic scraping with User-Agent rotation)

**Scripts:**
- `scrape-page.py` - Generic web scraping utility

**Dependencies:** `requests`, `beautifulsoup4`

**Features:**
- User-Agent rotation (4 browsers)
- Custom CSS selector support
- Automatic main content detection
- Text normalization

**Limitations:**
- No JavaScript rendering (requires Selenium/Playwright)
- Basic anti-bot bypass only
- No cookie/session handling

**Use Cases:**
- Scrape company announcements
- Extract blog content
- Monitor competitor websites
- Parse press releases

## Installation

### Install Dependencies

```bash
# For sentiment + web scraper
pip3 install requests beautifulsoup4

# For vessel tracking + satellite + datacenter monitor
pip3 install requests
```

### Run Tests

```bash
# Test all skills
cd sentiment/test && ./test-reddit.sh && ./test-trustpilot.sh
cd ../../vessel-tracking/test && ./test-ais.sh
cd ../../satellite/test && ./test-sentinel.sh
cd ../../datacenter-monitor/test && ./test-datacenter.sh
cd ../../web-scraper/test && ./test-scrape.sh
```

All tests should return PASS (either with data or noting missing dependencies).

## Usage Examples

### Sentiment Analysis

```bash
# Scrape Trustpilot reviews
cd sentiment
./scripts/scrape-trustpilot.py --domain temu.com > temu-reviews.json

# Scrape Reddit discussions
./scripts/scrape-reddit.py --subreddit Temu --limit 25 > reddit-temu.json

# Analyze text sentiment
echo "Great product, fast shipping!" | ./scripts/analyze-sentiment.py
```

### Satellite Imagery

```bash
# Query imagery for Amazon warehouse location
cd satellite
./scripts/fetch-sentinel2.py --lat 33.8303 --lon -117.9155 --date-range 2024-01-01/2024-12-31

# Query imagery for Shenzhen port
./scripts/fetch-sentinel2.py --lat 22.5431 --lon 114.0579 --max-results 20
```

### Web Scraping

```bash
# Scrape entire page
cd web-scraper
./scripts/scrape-page.py --url "https://company.com/press-releases"

# Extract specific elements
./scripts/scrape-page.py --url "https://company.com/about" --selectors "h1" "article" ".content"
```

## Skill Status Dashboard

| Skill | Status | Free Access | Tier |
|-------|--------|-------------|------|
| Sentiment | READY | Partial (may be blocked) | 2-3 |
| Vessel Tracking | BLOCKED | No (requires API keys) | 2-3 |
| Satellite | READY | Yes (Copernicus) | 2-3 |
| Datacenter Monitor | WIP | Partial (manual only) | 2-3 |
| Web Scraper | READY | Yes (basic scraping) | 2-3 |

## Tier Classification

**Tier 2-3**: Alternative data sources requiring:
- Free APIs with limitations
- Web scraping (anti-bot risk)
- Manual data collection
- Composite skill integration

## Integration with Deep Research

These skills integrate with the main deep-research SKILL:

1. **Source Collection Phase**: Each skill collects evidence packets
2. **Evidence Aggregation**: Packets merged into unified dataset
3. **Analysis Phase**: Evidence analyzed and synthesized
4. **Report Generation**: Insights incorporated into final report

## Future Enhancements

### Sentiment
- Add ML-based sentiment analysis
- Support more review platforms
- Implement proxy rotation

### Vessel Tracking
- Integrate AISHub API (with user API key)
- Add historical AIS datasets
- Build vessel movement analytics

### Satellite
- Download and process actual imagery
- Implement change detection algorithms
- Add parking lot occupancy estimation
- Support Planet Labs (commercial, 3m resolution)

### Datacenter Monitor
- Automate building permit searches
- Integrate satellite change detection
- Parse FOIA responses for power applications
- Build datacenter capacity database

### Web Scraper
- Add JavaScript rendering (Selenium/Playwright)
- Implement proxy pool
- Build retry logic with exponential backoff
- Support authenticated scraping

## License

See main project LICENSE.

## Contributing

Follow the evidence packet schema when adding new skills. All scripts must:
- Output standardized JSON evidence packets
- Include error handling
- Document data source limitations
- Provide test cases

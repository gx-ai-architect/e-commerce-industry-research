# Price Intelligence Skill

## Overview
Compares product prices across e-commerce platforms (Temu, Amazon, Shein, AliExpress) to prove/disprove the "Temu is cheapest" thesis and track price gap evolution post-tariff.

## Capabilities
- Cross-platform price scraping for specific product queries
- Average price computation per platform
- Price gap analysis and cheapest platform identification
- Historical price tracking for competitive intelligence

## Evidence Output
Returns standardized evidence packets with:
- Product query and timestamp
- Per-platform pricing data (name, price, platform)
- Computed metrics (average price, cheapest platform, price gaps)
- Graceful handling of platform blocks/errors

## Usage

### Compare prices across platforms
```bash
./scripts/compare-prices.py --query "wireless earbuds"
```

### Compare specific platforms only
```bash
./scripts/compare-prices.py --query "phone case" --platforms temu,amazon
```

## Output Format
See `../evidence-store/schema.json` for full evidence packet schema.

## Limitations
- Platforms may block automated requests (403 errors)
- Best used with manual verification via /browse skill
- Price data is point-in-time snapshot
- May require User-Agent rotation for high-volume usage

## Status
See STATUS.md for current implementation status and test results.

# Ad Intelligence Data Mining Skill

**Collector ID**: `ad-intelligence`

## Purpose

Track digital advertising spend, creative volume, and campaign targeting for e-commerce companies across Meta and Google platforms. Critical for understanding marketing strategy shifts, budget allocation changes, and geographic focus.

## Key Use Cases

- **Marketing Budget Shifts**: Detect dramatic changes in ad spend (e.g., Temu's 97% US reduction)
- **Geographic Targeting**: Track shifts between US and international markets
- **Competitive Intelligence**: Compare advertising volumes across competitors
- **Trend Detection**: Identify seasonal patterns, campaign launches, creative strategy changes

## Data Sources

### Meta Ad Library
- **URL**: https://www.facebook.com/ads/library/
- **Coverage**: Facebook, Instagram, Messenger, WhatsApp
- **API**: Requires Meta access token (free from developers.facebook.com)
- **Data**: Active/inactive ads, delivery dates, impressions, spend estimates

### Google Ads Transparency Center
- **URL**: https://adstransparency.google.com/
- **Coverage**: YouTube, Google Search, Google Display Network
- **API**: No public API (manual web access only)
- **Data**: Ad creatives, formats, regional targeting, date ranges

## Evidence Packet Schema

```json
{
  "packet_id": "PKT-ADS-{SOURCE}-{TIMESTAMP}",
  "source": {
    "type": "api",
    "url": "https://...",
    "title": "Meta Ad Library - {ADVERTISER} ({COUNTRY})",
    "retrieved_at": "ISO 8601 datetime",
    "collector": "ad-intelligence"
  },
  "extractions": [
    {
      "claim": "Temu reduced US advertising spend by 97% from 2023 to 2025",
      "evidence": "Baseline 2023: 10,000+ active ads; Current 2025: ~300 active ads",
      "evidence_type": "computed_metric"
    }
  ],
  "metadata": {
    "freshness": "2025-Q1 | real-time",
    "company_tags": ["TEMU", "SHEIN"],
    "topic_tags": ["advertising", "digital-marketing", "ad-spend", "meta-ads", "google-ads"]
  }
}
```

## Scripts

### `scripts/fetch-meta-ads.py`
Fetch advertising data from Meta Ad Library.

**Usage**:
```bash
# Using known data (no token required)
./fetch-meta-ads.py --advertiser temu --country US

# Using live API (requires token)
./fetch-meta-ads.py --advertiser temu --country US --token YOUR_META_TOKEN
```

**Getting a Meta Access Token**:
1. Visit https://developers.facebook.com/
2. Create app or use existing app
3. Go to Tools > Access Token Tool
4. Generate token with `ads_read` permission
5. Use token with `--token` parameter

**Arguments**:
- `--advertiser`: Company name to search (default: "temu")
- `--country`: Country code (US, GB, FR, DE, etc.)
- `--token`: Meta API access token (optional, uses known data if not provided)

**Output**: Evidence packet JSON

### `scripts/fetch-google-ads.py`
Fetch advertising data from Google Ads Transparency Center.

**Usage**:
```bash
./fetch-google-ads.py --advertiser temu
```

**Arguments**:
- `--advertiser`: Company name to search (default: "temu")

**Note**: Google Ads Transparency Center has no public API. This script provides documented stub implementation with known data points. For live data, manual web access is required.

**Output**: Evidence packet JSON

## Testing

```bash
cd test/
./test-meta-ads.sh
```

Tests validate:
- JSON output validity
- Evidence packet schema compliance
- Required fields presence
- Packet ID format
- Collector field accuracy

## Known Data Points

### Temu Advertising Patterns (2023-2025)

**Meta Ads**:
- 2023 baseline: 10,000+ active US ads
- Mid-2025: ~300 active US ads (97% reduction)
- Strategy shift: US → European markets

**Google Ads**:
- Heavy YouTube and Search presence (2023-2024)
- Significant US reduction in 2025
- Increased UK, Germany, France targeting
- Focus on app install campaigns

### SHEIN Advertising Patterns
- Sustained high-volume advertising across both platforms
- Multi-region targeting (US, Europe, Asia)
- Heavy influencer collaboration campaigns

## Authentication & Access

### Meta Ad Library API
- **Free Access**: Yes (with Meta developer account)
- **Rate Limits**: Standard API rate limits apply
- **Setup Time**: ~10 minutes to create app and get token
- **Documentation**: https://developers.facebook.com/docs/marketing-api/reference/ads_archive/

### Google Ads Transparency
- **API Access**: None (manual only)
- **Web Access**: Free, public
- **Rate Limits**: Standard web rate limiting
- **Alternative**: Use third-party ad intelligence platforms (Pathmatics, Sensor Tower)

## Limitations

1. **Spend Estimates**: Meta provides impression ranges, not exact spend
2. **Google API**: No programmatic access, manual web scraping required
3. **Historical Data**: Limited retention (typically 7 years for political ads, less for commercial)
4. **Granularity**: Cannot get exact daily spend or detailed targeting parameters
5. **Coverage**: Only covers ads that ran, not planned/rejected campaigns

## Integration with Deep Research

When analyzing e-commerce companies:

1. **Baseline Check**: Run both collectors for target company
2. **Competitor Comparison**: Compare ad volumes with competitors
3. **Trend Analysis**: Track changes quarter-over-quarter
4. **Strategy Validation**: Confirm reported marketing strategies with actual ad data
5. **Geographic Expansion**: Detect new market entries via ad targeting

Evidence packets from this skill directly support claims about:
- Marketing efficiency and ROI
- Customer acquisition costs
- Market expansion strategy
- Competitive positioning
- Brand awareness campaigns

## Future Enhancements

- [ ] TikTok Ads Library integration
- [ ] LinkedIn Ads transparency
- [ ] Twitter/X Ads Library
- [ ] Third-party ad intelligence API integration (Pathmatics, Apptopia)
- [ ] Automated spend estimation models
- [ ] Creative content analysis (image/video AI)
- [ ] Sentiment analysis on ad copy

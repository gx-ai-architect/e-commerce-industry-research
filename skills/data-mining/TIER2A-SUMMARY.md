# Tier 2A Data Mining Skills - Summary

Built: 2026-03-19

## Overview
Four alternative data mining skills that collect evidence packets for e-commerce research.

## Skills Built

### 1. App Intel
**Location:** `app-intel/`
**Purpose:** Mobile app store intelligence

**Scripts:**
- `scrape-appstore.py` - Apple App Store via iTunes Search API
- `scrape-playstore.py` - Google Play Store via web scraping

**Status:** ✅ WORKING (App Store), ⚠️ MAY BE BLOCKED (Play Store)

**Sample Data:**
- Temu iOS: 4.67★, 2.06M reviews, version 4.37.0
- Rankings, review counts, version tracking

---

### 2. Job Postings
**Location:** `job-postings/`
**Purpose:** Track hiring velocity and expansion signals

**Scripts:**
- `fetch-jobs.py` - Indeed RSS feed parser

**Status:** ⚠️ BLOCKED (403) - Returns valid error packet

**Signals:**
- Job posting counts
- Sample titles and locations
- Hiring velocity indicators

---

### 3. Web Traffic
**Location:** `web-traffic/`
**Purpose:** Domain traffic rankings

**Scripts:**
- `fetch-cloudflare-radar.py` - Tranco API + Cloudflare Radar fallback

**Status:** ✅ WORKING

**Sample Data:**
- temu.com: Rank #378 globally (Tranco, 2026-03-18)
- Rank history available
- Daily updates

---

### 4. Freight Rates
**Location:** `freight-rates/`
**Purpose:** Shipping cost indicators

**Scripts:**
- `fetch-freight-index.py` - Freightos FBX scraper

**Status:** ⚠️ PARSE_ERROR (page structure changed)

**Signals:**
- FBX index value (when parseable)
- Route-specific data requires premium API

---

## Evidence Packet Standard

All skills output the same schema:

```json
{
  "packet_id": "PKT-{SOURCE}-{ID}-{TIMESTAMP}",
  "source": {
    "type": "table | article | filing | dataset | api | image",
    "url": "https://...",
    "title": "...",
    "retrieved_at": "2026-03-19T...",
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
    "topic_tags": ["..."],
    "status": "ERROR | BLOCKED | PARSE_ERROR" // if applicable
  }
}
```

## Testing

All skills have passing tests:
- `app-intel/test/test-appstore.sh` ✅
- `job-postings/test/test-jobs.sh` ✅
- `web-traffic/test/test-traffic.sh` ✅
- `freight-rates/test/test-freight.sh` ✅

Tests validate:
- Valid JSON output
- Required fields present
- Error handling (produces valid packets even on failure)

## Known Limitations

1. **Anti-bot Protection**
   - Google Play Store may block scraping (403)
   - Indeed RSS may block high-frequency requests
   - All handle blocks gracefully with error packets

2. **Data Freshness**
   - Tranco: Updated daily
   - App Store: Real-time API
   - Freight rates: Depends on source page updates

3. **Premium Features Not Available**
   - Route-specific freight rates
   - Historical freight data
   - Detailed app ranking categories

## Dependencies

None! All skills use Python 3 standard library only:
- `urllib.request` for HTTP
- `json` for parsing
- `re` for regex extraction
- `argparse` for CLI

No `pip install` required.

## Next Steps

These skills can be integrated into:
1. Phase 2 (Alternative Data) of deep-research reports
2. Automated monitoring dashboards
3. Evidence collection pipelines for institutional research

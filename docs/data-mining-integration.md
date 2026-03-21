# Data Mining Integration Reference

How the 16 data mining skills connect to the deep-research report pipeline.

## Architecture

```
scripts/orchestrate.sh          # Runs all skills for a company
  └─ skills/data-mining/*/scripts/*  # Individual data collectors
       └─ reports/<company>/evidence-packets/*.json  # Evidence packets

scripts/bridge/packets_to_evidence.py  # Converts packets → evidence.json
  └─ reports/<company>/evidence-auto.json  # Auto-collected evidence
  └─ reports/<company>/evidence.json       # Final merged evidence
```

## Phase-to-Skill Mapping

### Phase 1: Financial Data
| Skill | Script | Arguments | Notes |
|-------|--------|-----------|-------|
| sec-edgar | fetch-filings.sh | `<CIK>` | Fetches XBRL JSON from SEC EDGAR API |
| sec-edgar | extract-xbrl.py | `--cik <CIK> --ticker <TICKER>` | Extracts financial metrics from XBRL |
| sec-edgar | parse-earnings.py | `--cik <CIK> --ticker <TICKER>` | Parses earnings call data |

### Phase 2: Alternative & Real-Time Data
| Skill | Script | Arguments | Notes |
|-------|--------|-----------|-------|
| parcel-volume | fetch-carrier-volumes.py | `--carrier all` | UPS/FedEx/USPS volume data |
| parcel-volume | fetch-shipmatrix.py | (none) | Stub — limited public data |
| parcel-volume | fetch-pitney-bowes.py | (none) | Stub — limited public data |
| customs-data | fetch-cbp-stats.py | (none) | Section 321 de minimis entry volumes |
| customs-data | fetch-tariff-rates.py | (none) | Current tariff schedules |
| air-freight | fetch-tac-index.py | `--route all` | Air cargo rate indices |
| air-freight | fetch-iata-stats.py | (none) | IATA air freight statistics |
| freight-rates | fetch-freight-index.py | (none) | Container/freight rate indices |
| app-intel | scrape-appstore.py | (none) | App Store rankings |
| app-intel | scrape-playstore.py | (none) | Play Store rankings |
| web-traffic | fetch-cloudflare-radar.py | (none) | Web traffic estimates |
| google-trends | fetch-trends.py | (none) | Search interest trends |
| sentiment | scrape-trustpilot.py | (none) | Consumer review sentiment |
| sentiment | scrape-reddit.py | (none) | Reddit discussion sentiment |
| job-postings | fetch-jobs.py | (none) | Job posting signals |
| ad-intelligence | fetch-meta-ads.py | `--advertiser temu` | Meta ad library data |
| ad-intelligence | fetch-google-ads.py | `--advertiser temu` | Google ads transparency |
| consumer-complaints | fetch-cpsc.py | `--query temu` | US CPSC product safety data |
| consumer-complaints | fetch-rapex.py | `--query temu` | EU RAPEX safety alerts |

### Phase 3: China Data
| Skill | Script | Arguments | Notes |
|-------|--------|-----------|-------|
| china-regulatory | fetch-samr.py | (none) | SAMR antitrust actions |
| china-regulatory | fetch-ndrc.py | (none) | NDRC policy announcements |

### Phase 4: Competitive & Regulatory
| Skill | Script | Arguments | Notes |
|-------|--------|-----------|-------|
| eu-regulatory | fetch-ec-press.py | (none) | EC press releases |
| eu-regulatory | fetch-rapex.py | (none) | EU RAPEX safety data |
| price-intel | compare-prices.py | `--query "wireless earbuds"` | Cross-platform price comparison |

## Known Limitations

| Skill | Issue |
|-------|-------|
| trade-data | BLOCKED — UN Comtrade requires API key (register at comtradeplus.un.org) |
| parcel-volume/fetch-shipmatrix.py | Stub — ShipMatrix does not offer public API |
| parcel-volume/fetch-pitney-bowes.py | Stub — Pitney Bowes index requires subscription |
| app-intel | May hit anti-bot protections on App Store/Play Store |
| sentiment/scrape-trustpilot.py | Rate-limited; Trustpilot blocks aggressive scraping |
| sentiment/scrape-reddit.py | Reddit API requires OAuth credentials for high volume |

## Evidence Packet Schema

Each script outputs JSON matching `skills/evidence-store/schema.json`:

```json
{
  "packet_id": "PKT-20260319120000",
  "source": {
    "type": "dataset|article|filing|api",
    "url": "https://...",
    "title": "...",
    "retrieved_at": "2026-03-19T12:00:00Z",
    "collector": "skill-name"
  },
  "extractions": [
    {
      "claim": "What the data says",
      "evidence": "The raw data or quote",
      "evidence_type": "direct_quote|table_slice|computed_metric",
      "verification": {
        "status": "supported|extrapolated|unsupported",
        "verifier_notes": "...",
        "verified_at": "2026-03-19T12:00:00Z"
      }
    }
  ],
  "metadata": {
    "freshness": "2026-03",
    "company_tags": ["PDD"],
    "topic_tags": ["customs", "de-minimis"]
  }
}
```

## Bridge Transformation

The bridge script (`scripts/bridge/packets_to_evidence.py`) converts packets to evidence.json:

| Packet Field | Evidence Field | Rule |
|-------------|----------------|------|
| (sequential) | `id` | E1, E2, ... (configurable `--start-id`) |
| `source.url` | `url` | Direct copy |
| `extraction.claim` + `extraction.evidence` | `quote` | Combined unless `evidence_type == "direct_quote"` |
| `metadata.freshness` or `source.retrieved_at` | `date` | Prefer freshness if date-like |
| `source.collector` | `provenance` | `"auto:<collector-name>"` |

Filtering: only `verification.status` of `"supported"` or `"extrapolated"` pass through.

## Troubleshooting

**Script fails with "file not found"**: Check that the skill directory exists and contains a `scripts/` subdirectory. Run `ls skills/data-mining/<skill>/scripts/` to verify.

**Empty output**: The script ran but produced no data. Check `reports/<company>/evidence-packets/errors.log` for stderr output. Common causes: API rate limits, network errors, missing credentials.

**Bridge produces 0 entries**: All extractions may have `verification.status: "unsupported"`. Check the raw packets in `evidence-packets/` to see what was collected.

**Merge duplicates**: The bridge deduplicates by exact URL match. If the same data appears under different URLs, both entries will be included.

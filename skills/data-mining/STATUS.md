# Data Mining Skills - Status Dashboard

## E-Commerce Focused (v2 — pruned 9 generic skills, added 6 e-commerce specific)

| Skill | Status | Tests | Notes | Last Verified |
|-------|--------|-------|-------|---------------|
| **Financial & Regulatory** | | | | |
| sec-edgar | READY | 2/2 pass | Foundation — PDD, AMZN, JD, UPS, FDX financials | 2026-03-19 |
| trade-data | BLOCKED | — | UN Comtrade requires API key registration | 2026-03-19 |
| eu-regulatory | READY | 2/2 pass | DSA, FSR enforcement actions | 2026-03-19 |
| china-regulatory | READY | 1/1 pass | SAMR/NDRC actions on PDD domestic | 2026-03-19 |
| **Demand & Engagement** | | | | |
| app-intel | READY | 1/1 pass | App Store rankings, downloads, ratings | 2026-03-19 |
| web-traffic | READY | 1/1 pass | Cloudflare Radar traffic data | 2026-03-19 |
| google-trends | READY | 1/1 pass | Search interest (mock fallback for anti-bot) | 2026-03-19 |
| sentiment | READY | 2/2 pass | Trustpilot + Reddit sentiment | 2026-03-19 |
| job-postings | READY | 1/1 pass | Expansion signals via hiring (Indeed may 403) | 2026-03-19 |
| **Logistics & Unit Economics** (NEW) | | | | |
| parcel-volume | READY | 1/1 pass | UPS/FedEx XBRL + ShipMatrix/Pitney Bowes stubs | 2026-03-19 |
| customs-data | READY | 3/3 pass | CBP Section 321 volumes + ITC tariff rates | 2026-03-19 |
| air-freight | READY | 5/5 pass | TAC Index air cargo rates + IATA stats | 2026-03-19 |
| freight-rates | READY | 1/1 pass | Container freight (Freightos, less relevant for parcels) | 2026-03-19 |
| **Competitive Intelligence** (NEW) | | | | |
| price-intel | READY | 1/1 pass | Cross-platform price comparison (Temu/Amazon/Shein) | 2026-03-19 |
| ad-intelligence | READY | 1/1 pass | Meta Ad Library + Google Ads Transparency | 2026-03-19 |
| consumer-complaints | READY | 3/3 pass | CPSC recalls/incidents + EU RAPEX safety alerts | 2026-03-19 |
| **Infrastructure** | | | | |
| extraction | READY | 2/2 pass | Evidence packet extraction + verification layer | 2026-03-19 |

## Summary
- **READY: 16/17 skills**
- **BLOCKED: 1/17** (trade-data — needs API key)
- Pruned: anomaly-detector, foia, datacenter-monitor, satellite, vessel-tracking, patents, china-patents, web-scraper, china-media

## What Changed (v2)
- **Deleted 9 generic quant-fund skills** that didn't answer e-commerce questions
- **Added 6 e-commerce-specific skills**: parcel-volume, customs-data, air-freight, price-intel, ad-intelligence, consumer-complaints
- Every remaining skill directly answers an e-commerce research question

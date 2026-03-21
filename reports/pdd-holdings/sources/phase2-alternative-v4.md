# Phase 2: Alternative Data — PDD Holdings (v4)

**Date**: 2026-03-20
**Sources**: PKT-qimai-*, PKT-TRUSTPILOT-*, PKT-APPSTORE-*, PKT-CPSC-*, PKT-PEER-COMPARISON-001, PKT-TEMU-COMPLAINTS-001, PKT-LOG-*, PKT-INV-003, PKT-CS-TRAFFIC-003, PKT-CS-APPSTORE-006, PKT-CS-BROWSE-008

---

## 1. App Store Ratings (iTunes API, March 2026)

### Temu iOS App (v4.37.0)

| Market | Rating | Rating Count |
|--------|--------|-------------|
| US | 4.67/5 | 2,064,730 |
| UK | 4.71/5 | 367,810 |
| DE | 4.67/5 | 193,975 |
| JP | 4.25/5 | 176,739 |
| BR | 4.39/5 | 60,555 |

[DATE: 2026-03-20] From iTunes Lookup API. Temu maintains 4.2-4.7 across all major markets. UK (4.71) slightly higher than US (4.67) -- consistent with US-focused tariff friction. (PKT-qimai-temu-20260319, PKT-CS-APPSTORE-006)

### Pinduoduo iOS App (v7.99.0)

| Market | Rating | Rating Count |
|--------|--------|-------------|
| CN | 2.9/5 | 3,380,424 |
| US | 2.4/5 | 7,004 |
| UK | 2.5/5 | 371 |
| DE | 2.3/5 | 133 |
| JP | 2.4/5 | 1,497 |
| BR | 3.6/5 | 35 |

[DATE: 2026-03-20] From iTunes Lookup API. Pinduoduo iOS rating is the lowest among major Chinese e-commerce apps. (PKT-qimai-pinduoduo-20260319)

### Peer Comparison

| App | Market | Rating | Ratings Count |
|-----|--------|--------|--------------|
| Amazon | US | 4.83/5 | 8,344,524 |
| Temu | US | 4.67/5 | 2,064,730 |
| Taobao | US | 3.66/5 | 9,556 |
| Pinduoduo | US | 2.37/5 | 7,004 |
| Taobao | CN | 4.14/5 | 1,679,186 |
| Pinduoduo | CN | 2.93/5 | 3,380,562 |

[DATE: 2026-03-20] Pinduoduo CN rating is 1.21 points lower than Taobao despite 2x more ratings. Temu trails Amazon by only 0.16 points. (PKT-APPSTORE-COMPARISON-001, PKT-PEER-COMPARISON-001)

**Stark divergence**: Temu iOS App Store 4.67/5 vs Trustpilot 2.0/5. This 2.67-point gap is the largest among shopping apps. App Store ratings are prompted after positive in-app experiences; Trustpilot is self-selected and complaint-driven. 10.9% of Temu Trustpilot reviews likely AI-generated. (PKT-APPSTORE-COMPARISON-001)

---

## 2. Trustpilot / BBB / Review Platforms

### Temu Review Scores

| Platform | Rating | Review Count |
|----------|--------|-------------|
| Trustpilot | 2.0/5 | 48,750 |
| Sitejabber | 2.0/5 | 1,760 |
| PissedConsumer | 2.6/5 | 62,683 |
| BBB | B- (improved from C+ in Jan 2024) | -- |

[DATE: 2026-03-20] Trustpilot scraper output. BBB rose from C+ (Jan 2024) to B- (Dec 2025). Not BBB accredited. (PKT-TRUSTPILOT-TEMU-001)

34% of Trustpilot users rated Temu 5 stars despite 2.0 average -- polarized distribution. (PKT-TRUSTPILOT-TEMU-001)

10.9% of Temu Trustpilot reviews are likely AI-generated, up 1,361% from 0.75% in 2022 (Originality.AI analysis). (PKT-TRUSTPILOT-TEMU-001)

### Top Complaint Themes (International)

1. **Product quality** (most common): "poorly made, not as described", coats "shrunken and misshapen", items "nothing like product shown" (PKT-TEMU-COMPLAINTS-001)
2. **Bot customer service**: "all very bad bots, you can't reason with them", different agents give different answers (PKT-TEMU-COMPLAINTS-001)
3. **Deceptive pricing**: extra charges at checkout, shipping costs exceeding product cost, fake discounts, "bait and switch on everything" (PKT-TEMU-COMPLAINTS-001)
4. **Refund delays**: "can take weeks or months" (PKT-TRUSTPILOT-TEMU-001)

Complaint velocity trend: worsening quality perception alongside rising prices. Long-time customers report "a decline in quality, deceptive images" and "Prices creeping up to levels where other sites are cheaper with far better quality." (PKT-TEMU-COMPLAINTS-001)

0% complaint resolution rate on complaintsboard.com (0/150 resolved). (PKT-TEMU-COMPLAINTS-001)

US state attorneys general filed lawsuits against Temu in 2025 alleging data privacy breaches, deceptive trade practices, and forced labor products. (PKT-TEMU-COMPLAINTS-001)

---

## 3. Temu Traffic & Users

### Web Traffic

- **Tranco global rank**: #377 (Mar 19, 2026), improving from #383 (Mar 15). (PKT-CS-TRAFFIC-003)
- **SemRush**: 1.2 billion visits in Feb 2026, down 25.66% from Jan 2026. Average session duration: 08:38. (PKT-CS-TRAFFIC-003)

### Monthly Active Users (Sensor Tower)

| Metric | Value | Date |
|--------|-------|------|
| Global MAU peak | 530M | Aug 2025 |
| Cumulative downloads | 1.2B+ | Oct 2025 |
| US MAU | 133.6M | Oct 2025 (down 28% YoY) |
| EU MAU | 141.6M | Oct 2025 (up 74% YoY) |
| EU share of global users | 34% | 2025 |

[DATE: 2025-10] US DAU plunged 58% after de minimis ended. EU now surpasses US in user count. (PKT-CS-TRAFFIC-003)

More severe US collapse data: Sensor Tower reported US MAU dropped from ~34M (May 2024) to <8M (May 2025), a 54% decline. App Store ranking fell from top 10 to #73. (PKT-PRICE-003)

Customer retention: only 24% of first-time buyers likely to return. (PKT-CS-TRAFFIC-003)

### Consumer Engagement Comparison

- Amazon: 64% of consumers plan increased spending (highest). (PKT-PEER-COMPARISON-001)
- Temu: 28% shop monthly. (PKT-PEER-COMPARISON-001)
- Shein: 23% shop monthly. (PKT-PEER-COMPARISON-001)
- Amazon Haul: only 16% shop monthly despite 24% trying it. (PKT-PEER-COMPARISON-001)

---

## 4. CPSC Recalls

10 CPSC recalls matching "temu" out of 9,700 total in database, all products sold exclusively on Temu.com:

| Date | Product | Hazard |
|------|---------|--------|
| 2025-02-13 | 6-in-1 Pounding Games | Magnet ingestion |
| 2025-02-06 | Sling Carriers | Fall hazard |
| 2024-11-07 | Baofali Crib Bumpers | Suffocation |
| 2024-07-25 | Toy Guns | Eye injury |
| 2024-07-11 | Children's Nightgowns | Burn/flammability |
| 2024-07-11 | Fashion Online Pajama Sets | Burn/flammability |
| 2024-07-11 | JUVENNO KIDS Pajama Sets | Burn/flammability |
| 2024-06-13 | Magnetic Chess Games | Magnet ingestion |
| 2024-04-25 | Chau River Kids' Bike Helmets | Head injury |
| 2024-04-18 | Gasaciods Children's Helmets | Head injury |

[DATE: 2025-02-13] From CPSC API via fetch-cpsc.py. All children's safety products. (PKT-CPSC-TEMU-001, PKT-REG-US-002)

CPSC launched targeted examination of Temu and Shein in September 2024 for "deadly products marketed for babies and toddlers." 7 CPSC-warned products still listed on Temu 6 months after warnings (vs 0 on Amazon). CPSC set record of 28 recalls/warnings in single week on May 15, 2025. (PKT-REG-US-002)

EU Safety Gate: 67% of Temu products failed EU safety tests (2 out of 3, small sample). BEUC found toys with toxic chemicals, strangulation/choking hazards, electrocution risk, non-protective helmets. (PKT-CPSC-TEMU-001, PKT-REG-COMP-001)

Consumer Reports: Temu removed unsafe listings and committed to additional safety changes by end of March 2026. New CPSC Certificates of Compliance rule effective July 8, 2026. (PKT-REG-US-002)

---

## 5. Logistics & Parcel Volumes

### China Industry-Wide

| Metric | Value | Date |
|--------|-------|------|
| Total postal parcels (2025) | 216.51B, +11.8% YoY | [DATE: 2026-01-07] |
| Express delivery parcels (2025) | ~199B | [DATE: 2026-01-07] |
| Express revenue (2025) | RMB 1.5T ($215B), +6.5% YoY | [DATE: 2026-01-07] |
| 2026 projection | 214B items, +8% YoY | [DATE: 2026-01] |
| Processing speed | 6,200+ parcels/second avg | [DATE: 2025-12] |
| Per capita (2025) | 141 parcels/year | [DATE: 2025] |
| Market value (2025) | $131.84B | [DATE: 2025] |

[DATE: 2026-01-07] From State Post Bureau official data via People's Daily. During 14th Five-Year Plan (2021-25), volume grew from 80B to ~200B parcels. (PKT-LOG-CHINA-INDUSTRY-001)

### ZTO Express (Market Leader)

| Metric | FY2025 | YoY |
|--------|--------|-----|
| Parcel volume | 38.52B | +13.3% |
| Q4 2025 volume | 10.56B | +9.2% |
| Revenue | RMB 49.1B | +10.9% |
| Adjusted net income | RMB 9.5B | -- |
| Gross margin | 25.0% (down from 31.0%) | -600bps |
| Operating margin | 21.3% (down from 26.6%) | -530bps |
| Market share | ~19.4% (expanding 0.8pp in Q4) | -- |
| 2026 guidance | 42.37-43.52B (+10-13%) | -- |

[DATE: 2026-03-18] From ZTO Q4/FY2025 earnings release. ZTO approved $1.5B share repurchase program over 24 months. (PKT-LOG-ZTO-VOLUME-001)

### Other Major Carriers (2024)

- YTO Express: ~26.6B parcels, +25.33% YoY, #2 behind ZTO (PKT-LOG-YTO-YUNDA-VOLUME-001)
- Yunda Express: ~23.8B parcels, +26.14% YoY, #3 (PKT-LOG-YTO-YUNDA-VOLUME-001)
- Top 6 private carriers: ~80-82% of China parcel volume (Q3 2025, Morningstar) (PKT-LOG-YTO-YUNDA-VOLUME-001)
- YTO narrowing market share gap with ZTO; STO leads revenue growth while Yunda lags. (PKT-LOG-YTO-YUNDA-VOLUME-001)

### Pinduoduo Domestic Logistics

- PDD parcel volume surpassed Taobao/Tmall in 2023, becoming largest single e-commerce source of express parcels in China. The 150 billionth parcel delivered in China in 2024 was ordered via Pinduoduo. (PKT-LOG-PDD-DOMESTIC-001)
- Estimated PDD-attributable parcels: 50-60B/year (~25-30% of industry). (PKT-GMV-003)
- Subsidizes remote delivery at RMB 0.05-0.12/parcel; Duoduo Stations handle 25%+ of rural parcel volume. (PKT-LOG-PDD-DOMESTIC-001)
- Investing RMB 10B in instant retail (Duoduo Station) Sept 2025 - Sept 2026, targeting 20M daily transactions. (PKT-LOG-PDD-DOMESTIC-001)
- Domestic express delivery cost: ~RMB 2-5/parcel ($0.30-0.70). PDD often absorbs/subsidizes this. (PKT-LOG-PDD-DOMESTIC-001)

### Temu US Package Volume

| Period | Daily Packages (US) | Source |
|--------|-------------------|--------|
| Late 2023 holiday | ~1M/day | ShipMatrix |
| July 2024 | ~900K/day | ShipMatrix |
| 2025 (post-de minimis) | 250-300K/day | Estimated |

[DATE: 2025-07] 70%+ decline from peak. De minimis changes reduced Section 321 volumes by 30-35%. (PKT-LOG-TEMU-US-VOLUME-001)

US total domestic parcel market: 23.9B packages in 2025, $196B revenue (+4.1%), ~91M weekday average. 3.9% CAGR to 26.8B by 2028. (PKT-LOG-TEMU-US-VOLUME-001)

### Temu Warehouse Network

**Global**: 13 self-owned warehouses as of Oct 2025 -- 10 in Europe, 2 in US, 1 near US-Mexico border (120,000 sqm "Jitu Warehouse"). (PKT-LOG-TEMU-US-WAREHOUSE-001, PKT-CS-WAREHOUSE-004)

**US locations**: California (Rowland Heights, WINIT America 18501 Arenth Ave), Dallas TX, Georgia. 3PL partners: WINIT and Easy Export. Also "family warehouses" (fulfillment from residences). Pre-shipped 3 months inventory before May 2 de minimis deadline. (PKT-LOG-TEMU-US-WAREHOUSE-001)

**European locations**: Rotterdam (NL) and Frankfurt (DE) as main hubs. Active in UK, DE, FR, ES, IT, AT. Target: 80% of EU orders from local warehouses. UK target: 50% local by end 2025. (PKT-LOG-TEMU-EU-WAREHOUSE-001)

**South Korea**: 165,000 sqm logistics center in Gimpo. **Brazil**: 14th warehouse planned in Rio de Janeiro. (PKT-INV-002)

US self-operated warehouses: 15-20% of US volume (2025), projected 20-25% by 2026. (PKT-CS-WAREHOUSE-004)

### Delivery Times Comparison

| Platform | Standard | Express | On-Time Rate |
|----------|----------|---------|-------------|
| Temu | 7-15 biz days (free) | 3-7 days (~$12.90, waived >$129) | 82% |
| Amazon Prime | 1-2 biz days | Same-day (expanding) | -- |
| Shein | 8-11 biz days | -- | 94% |

[DATE: 2025-2026] Cross-border parcels taking 15+ days declined from 29% (2020) to 7% (2025). (PKT-LOG-DELIVERY-TIMES-001)

Temu matched Amazon in cross-border e-commerce market share: 24% each in 2025, up from 1% in 2022. (PKT-LOG-DELIVERY-TIMES-001)

---

## 6. Air Freight Rates

| Period | China-US Rate (per kg) |
|--------|----------------------|
| Mid-Oct 2025 | $5.00 (TAC Index, +2.5% WoW) |
| Late Dec 2025 | $6.25 (-16% from peak) |
| 2025 general range | $3.10-$4.70 |
| 2025 spot rates | $4-7 |
| Express/door-to-door | $8-12 |

[DATE: 2025-12] Typical e-commerce parcel (0.5-2kg): $3-8 per parcel by air. (PKT-LOG-AIRFREIGHT-001)

Global air cargo demand (CTK) grew 13.6% in 2024; load factor 48.3% (IATA). Bulk shipping to UK 3PL warehouses reduced per-item logistics costs 40-60% vs air freight. (PKT-LOG-AIRFREIGHT-001, PKT-LOG-TEMU-EU-WAREHOUSE-001)

---

## 7. Ad Intelligence

### Meta Ad Library

- 2023 baseline: 10,000+ active ads in US (PKT-INV-003)
- 2025: ~300 active ads in US -- **97% reduction** (PKT-INV-003)
- Shifted focus to European markets (PKT-INV-003)

### Google Ads Transparency

- US Google Shopping ad impressions: fell from 19% share to 0% after tariffs (PKT-INV-003)
- Temu halted Google Shopping ads in US on April 9, 2025 (PKT-CS-GMV-005)
- March 31 - April 13: daily US ad spend on FB/IG/TikTok/Snap/X/YT decreased 31% (PKT-CS-GMV-005)

### Ad Spend Trajectory

| Period | Daily New US Ads |
|--------|-----------------|
| Pre-tariff peak (2023-2024) | >20,000/day |
| Q2 2025 (post-tariff) | "a few dozen" |
| September 2025 (comeback) | "thousands or 10,000+" |

[DATE: 2025-09] Appgrowing Global tracking data. PDD reallocated 20-30% of ad budget to Europe. (PKT-PRICE-005, PKT-CS-GMV-005)

### Browsed Observations (temu.com, March 2026)

- temu.com US now requires login/registration to browse products (login gate). Footer: "2022-2026 WhaleCo Inc." (PKT-CS-BROWSE-008)
- Shipping page: price adjustment within 30 days, free shipping (excludes local items), free returns up to 90 days, delivery guarantee with refund. (PKT-CS-BROWSE-008)
- "Local Warehouse" items ship from within US, no import taxes. Imported items show separate import charges at checkout. (PKT-CS-BROWSE-008)
- Click & Collect option now available, suggesting physical pickup points. (PKT-CS-BROWSE-008)
- temu.com/uk also requires login gate. (PKT-CS-BROWSE-008)

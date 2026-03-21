# Evidence Audit Report: PDD Holdings v4

*Audit Date: March 20, 2026*

---

## Executive Summary

The PDD Holdings v4 report contains **65 unique evidence references** across **162 citation instances**. This audit found:

- **9 MISSING_ENTRY** citations: Evidence IDs referenced in the report that do not exist in evidence-v4.json
- **11 OVERCLAIMED** citations: Claims that go beyond what the evidence actually states
- **7 MISATTRIBUTED** citations: Evidence URLs that do not match the data in the quote field
- **4 BAD_URL** entries: Evidence entries with generic/non-clickable URLs
- **28+ UNCITED** quantitative claims in body text (excluding tables)
- **5 tables** lacking source attribution rows
- **2 contradictory** data points across different evidence entries

Overall severity: **MODERATE-HIGH**. The report's core claims are directionally supported, but many citations are sloppy -- wrong URLs, missing time periods, analyst estimates presented as facts, and evidence entries that bundle multiple unrelated data points under a single URL.

---

## Category 1: MISSING_ENTRY (9 citations)

These evidence IDs appear in the report but have NO corresponding entry in evidence-v4.json.

| ID | Report Line | Claim Context | Verdict |
|----|-------------|---------------|---------|
| E60 | L239 | "Semi-managed...70% of US search traffic reallocated overnight" | MISSING_ENTRY -- data exists in PKT-CS-SEMIMANAGED-002 but not curated |
| E73 | L241 | "Pre-shipped 3 months of US inventory by sea before May 2 deadline" | MISSING_ENTRY -- data exists in PKT-CS-WAREHOUSE-004 but not curated |
| E74 | L243, L279, L316 | "80% EU local fulfillment" target, EU warehouse strategy | MISSING_ENTRY -- data exists in PKT-CS-WAREHOUSE-004 but not curated |
| E75 | L300 | "US self-operated warehouses handle only 15-20% of volume; rest via 3PL WINIT/Easy Export" | MISSING_ENTRY -- data exists in PKT-CS-WAREHOUSE-004 but not curated |
| E119 | L219, L259 | "Complaintsboard.com 0% resolution rate (0/150)" | MISSING_ENTRY -- no raw packet found |
| E121 | L259 | "BBB rating improved from C+ to B-" | MISSING_ENTRY -- no raw packet found |
| E122 | L257 | "Sitejabber 2.0/5" rating | MISSING_ENTRY -- no raw packet found |
| E123 | L259 | "10.9% of Trustpilot reviews likely AI-generated, up 1,361% from 2022" | MISSING_ENTRY -- no raw packet found |
| E125 | L259 | "34% of Trustpilot users gave 5 stars despite 2.0 average" | MISSING_ENTRY -- no raw packet found |

**Impact**: 9 claims in the report cite non-existent evidence. E60/E73/E74/E75 have supporting data in raw packets that was never promoted to the curated evidence file. E119/E121/E122/E123/E125 appear to be from customer-happiness research that was never captured.

---

## Category 2: OVERCLAIMED (11 citations)

Claims that go beyond what the cited evidence actually states.

### OC-1: "EU is now 40% of Temu GMV" (L77, Geographic table)
- **Cited**: Implicitly from E43
- **E43 actually says**: "European GMV on track to surpass $15B in 2025, could top $20B by end of 2026. US accounts for 29% of Temu revenue in 2025."
- **Issue**: The "40%" figure comes from analyst estimates in PKT-INV-007 (TechBuzz China), which states this is "extrapolated" from industry data. PDD does not disclose geographic GMV breakdown. The report presents it as fact in a table without qualifying it as an estimate or specifying the time period.
- **Verdict**: OVERCLAIMED. Should say "approximately 40% per analyst estimates (Q3 2025)"

### OC-2: "US MAU collapsed 54%: ~34M to <8M" vs "US MAU declined 28% to 133.6M" (L60, L239)
- **E42**: "US MAU collapsed 54%: ~34M (May 2024) to <8M (May 2025)"
- **E68**: "US MAU declined 28% YoY to 133.6 million (Oct 2025)"
- **Issue**: These are contradictory. E42 appears to reference web unique visitors (SimilarWeb); E68 references app MAU (Sensor Tower). The report uses "US MAU plunged from ~34M to <8M" in line 60 citing E42, but this may be web visits, not app MAU. The distinction is critical and unstated.
- **Verdict**: OVERCLAIMED. The 54% decline and the 28% decline measure different things. Report conflates them.

### OC-3: "most profitable marketplace per unit of GMV in global e-commerce" (L9)
- **Cited**: E7, E10
- **E7**: Compares PDD to Alibaba and JD only for Q1 2024
- **Issue**: "Global e-commerce" includes Amazon, Mercado Libre, Coupang, etc. Evidence only covers Chinese peers. Also uses a single quarter (Q1 2024).
- **Verdict**: OVERCLAIMED. Should say "most profitable among major Chinese e-commerce platforms in Q1 2024"

### OC-4: "revenue growth collapsed from 108% to 1%" (L11)
- **Cited**: E18, E17
- **E18**: States FY2024 transaction services growth was +108%, Q2 2025 was "flat"
- **Issue**: The 108% is FY2024 full-year; the "1%" (from E295) is Q2 2025 quarter. The report implies a sequential collapse within the same metric frame, but these are different comparison periods.
- **Verdict**: OVERCLAIMED. Should specify "FY2024 full-year transaction services growth of +108% decelerated to +1% YoY in Q2 2025"

### OC-5: "RMB 80-100B in annual operating profit at 35-45% segment margins" (L9)
- **Cited**: E7, E10
- **E7/E10**: Report consolidated figures only (no segment disclosure)
- **Issue**: PDD does not disclose Pinduoduo segment margins. This is a back-calculation (consolidated minus estimated Temu losses). Should be clearly labeled as an estimate.
- **Verdict**: OVERCLAIMED. Should say "an estimated RMB 80-100B based on backing out estimated Temu losses from consolidated results"

### OC-6: "Pinduoduo surpassed Taobao/Tmall in 2023" as parcel source (L32)
- **Cited**: E22
- **E22**: "PDD estimated 25-30% of industry" and "likely 40%+ segment operating margin"
- **Issue**: E22 is an estimate. The report states this as established fact. No third-party source confirming Pinduoduo surpassed Taobao.
- **Verdict**: OVERCLAIMED. Should say "estimated to have surpassed" with source attribution

### OC-7: "150 billionth parcel delivered in China in 2024 was ordered through Pinduoduo" (L32)
- **Cited**: E22
- **E22 quote**: Does not contain this claim
- **Issue**: This specific factoid (150B parcel milestone) does not appear in E22's quote text. Likely sourced from Chinese media but not captured in evidence.
- **Verdict**: UNSUPPORTED by cited evidence

### OC-8: "$59.5B cash pile" used throughout (L9, L11, L106, L243, L249, L308, L312, L351)
- **Cited**: E5
- **E5**: States RMB 423.8B as of September 2025
- **Issue**: $59.5B implies RMB 423.8B / ~7.12 exchange rate. The exchange rate is not specified, and converting RMB to USD without stating the rate is imprecise. Moreover, this is Q3 2025 data, not current.
- **Verdict**: OVERCLAIMED (minor). Should specify "RMB 423.8B ($59.5B at ~7.12 RMB/USD) as of September 30, 2025"

### OC-9: "the September 2025 comeback already demonstrated model resilience" (L11)
- **Cited**: E18, E17
- **E17**: Q3 2025 revenue +9% YoY, operating profit +3% YoY
- **Issue**: Q3 2025 data shows modest recovery, not necessarily "resilience." +3% operating profit growth after -38% in Q1 and -21% in Q2 is stabilization, not a comeback that proves resilience.
- **Verdict**: OVERCLAIMED. Should say "Q3 2025 showed stabilization with revenue growth recovering to +9% YoY"

### OC-10: "cross-border e-commerce market share (tied with Amazon at 24%)" (L251, L312)
- **Not clearly cited** in the international table (L199)
- **Issue**: No evidence entry contains this specific market share claim with source attribution. It appears in the competitive table without citation.
- **Verdict**: OVERCLAIMED/UNCITED. Needs source attribution (which research firm, which methodology, which time period)

### OC-11: "Alibaba's $53B capex commitment" (L34, L231)
- **Cited**: E8
- **E8 quote**: "PDD has NO fintech business unlike Alibaba... PDD's RMB 20.55B investment income provides fintech-equivalent profit"
- **Issue**: E8 does not mention Alibaba's $53B cloud capex. This is a well-known figure from Alibaba's March 2025 announcement but is unsupported by the cited evidence.
- **Verdict**: UNSUPPORTED by cited evidence

---

## Category 3: MISATTRIBUTED URLs (7 entries)

Evidence entries where the URL does not match the data in the quote.

| ID | URL | Quote Content | Actual Source |
|----|-----|---------------|---------------|
| E294 | congress.gov/bill/119th-congress/house-bill/805 | Temu import charges, revenue growth, gross margin | Should be PDD earnings + CNBC reporting |
| E295 | congress.gov/bill/119th-congress/house-bill/805 | Transaction services revenue growth 1%, margin 55.9% | Should be PDD earnings release |
| E67 | tranco-list.eu/api/ranks/domain/temu.com | Temu global MAU peaked at 530M (Sensor Tower data) | Should be Sensor Tower or data.ai |
| E68 | tranco-list.eu/api/ranks/domain/temu.com | US MAU declined 28% to 133.6M (Sensor Tower data) | Should be Sensor Tower or data.ai |
| E69 | tranco-list.eu/api/ranks/domain/temu.com | EU MAU grew 74% to 141.6M (Sensor Tower data) | Should be Sensor Tower or data.ai |
| E42 | investor.pddholdings.com/news-releases/... | GMV estimates, MAU data, trust % (multi-source) | Should be separated: ECDB, SimilarWeb, Omnisend |
| E43 | investor.pddholdings.com/news-releases/... | EU GMV projections, geographic mix (analyst est.) | Should be Cross-Border Magazine / TechBuzz China |

**Root Cause**: The auto-collection process bundled data from multiple sources into single evidence entries and assigned the collector's primary URL rather than the actual source URL.

---

## Category 4: BAD/GENERIC URLs (4 entries)

| ID | URL | Issue |
|----|-----|-------|
| E89 | https://itunes.apple.com/lookup | No parameters -- not a clickable link to specific data |
| E90 | https://itunes.apple.com/lookup | Same issue |
| E92 | https://itunes.apple.com/lookup | Same issue. Contains Trustpilot AI-generation claim, not iTunes data |
| E109 | multiple | Literal "multiple" as URL -- completely useless for verification |

---

## Category 5: WRONG CITATION TARGET (3 instances)

Report cites an evidence entry for a claim that entry does not contain.

### WC-1: E30 cited for CPSC recalls (L117, L134)
- **Report**: "10 CPSC recalls, all children's products [E30]"
- **E30**: "Temu US iOS: 4.67/5 (2,064,730 ratings)..." -- App Store ratings only
- **Should cite**: E94 ("10 CPSC recalls involve products sold exclusively on Temu.com. All children's safety products.")

### WC-2: E30 cited for Trustpilot (L118)
- **Report**: "Trustpilot 2.0/5 (48,750 reviews), 34% gave 5 stars [E30]"
- **E30**: App Store ratings only
- **Should cite**: E120 for Trustpilot rating

### WC-3: E33 cited for Tranco rank and SemRush (L114-115)
- **Report**: "Tranco global rank #377 [E33]" and "SemRush visits 1.2B [E33]"
- **E33**: "Temu.com US requires login/registration..." -- temu.com shipping page observations
- **Should cite**: E65 for Tranco, and a SemRush-specific entry (not in curated set)

### WC-4: E23 cited for Meta ads (L116)
- **Report**: "Meta ads (US) ~300 active (97% reduction from 2023) [E23]"
- **E23**: "Online marketing services represented 50.3% of FY2024 revenue" -- PDD's OMS revenue
- **Should cite**: An ad-intelligence entry (not in curated set)

---

## Category 6: UNCITED TABLES (5 tables)

### Table 1: "The Numbers That Matter" (L15-24)
- Contains FY2022-9M2025 financial data across 8 metrics
- Source note on L26 references [E10, E11, E13, E14, E15, E16, E17, E5] but is a footnote, not per-row attribution
- **Verdict**: PARTIALLY CITED. The footnote exists but individual numbers cannot be traced to specific evidence entries.

### Table 2: "Geographic Shift" (L75-79)
- EU 40% share, US 31% share, MAU data
- No per-row source. "40%" is unattributed analyst estimate.
- **Verdict**: UNCITED. Needs source row with time period and methodology.

### Table 3: "Regulatory Timeline" (L151-160)
- 8 future regulatory events with cost estimates
- Zero citations. "$1.2B annual cost" and "$3.2B fine" are uncited.
- **Verdict**: UNCITED. Each row should cite the regulatory source.

### Table 4: "Domestic: PDD vs Alibaba vs JD.com" (L168-184)
- Dense competitive comparison. Source note on L185 references [E6-E10, E22] but does not cover Alibaba/JD data.
- JD revenue "RMB 1,159B" -- source unclear. Alibaba operating income "RMB 135.1B" -- source unclear.
- **Verdict**: PARTIALLY CITED. PDD data sourced; competitor data unsourced.

### Table 5: "International: Temu vs Amazon vs Shein" (L197-214)
- Source note on L215 references 8 evidence entries, but many rows have data not in any evidence entry.
- "Cross-Border Market Share 24%" -- no evidence entry contains this.
- "On-Time Rate 82%" -- no evidence entry contains this.
- "Delivery 7-15 days" -- no evidence entry contains this.
- **Verdict**: PARTIALLY CITED. Several rows uncited.

---

## Category 7: UNCITED QUANTITATIVE CLAIMS (key examples)

| Line | Claim | Issue |
|------|-------|-------|
| L40 | "1,004,841 cumulative complaints, 20% reply rate, JD 100% reply rate" | Data matches E98/E99/E100 but not cited inline |
| L44 | iPhone 16 Pro Max pricing: RMB 7,899 vs 7,499 vs 7,408 | From price-intelligence packets but uncited |
| L44 | "RMB 81B ($11B) national trade-in subsidy program" | No evidence entry |
| L50 | "malicious refund-only orders dropped 62%, resolution rates 18% to 75%" | Matches E111 but uncited inline |
| L52 | "RMB 100B/3yr cost (~RMB 33B/year)" math | Derived from E115 but uncited inline |
| L142 | "Poland $1.7M fine" and "France eco-tax up to EUR 5/item" | No evidence entry |
| L147 | "Alibaba RMB 18.23B ($2.78B) SAMR antitrust fine in 2021" | No evidence entry |
| L191 | "Douyin e-commerce reached estimated $648B GMV in 2025" | E128 cited elsewhere but not here |

---

## Category 8: CONTRADICTORY DATA

### Contradiction 1: US MAU figures
- E42: "US MAU collapsed 54%: ~34M (May 2024) to <8M (May 2025)"
- E68: "US MAU declined 28% YoY to 133.6 million (Oct 2025)"
- Report L60 uses E42's figures: "US MAU plunged from ~34M to <8M"
- Report L206 table uses E68's figure: "US MAU (Oct 2025) 133.6M"
- **Resolution**: E42 likely refers to web unique visitors (SimilarWeb); E68 to mobile app MAU (Sensor Tower). Report must distinguish between these metrics.

### Contradiction 2: Transaction services growth
- Report L60: "Transaction services revenue growth collapsed from 234% YoY (Q2 2024) to 1% (Q2 2025)"
- E295 confirms the Q2 2025 figure (1%) and Q2 2024 comparator (234%)
- E16: "Q2 2025 TS RMB 48,281.6M (~flat)"
- "~flat" and "1% growth" are consistent but the 234% comparator needs verification -- E18 says "108% (FY2024)" not Q2 2024 specifically
- **Resolution**: The 234% appears to be Q2 2024 quarter-specific (from PKT-REG-US-001), while E18's 108% is FY2024 full year. Both can be true. The report should specify "Q2 2024 quarter" for the 234% figure.

---

## Recommendations

1. **Promote missing entries**: Add E60, E73, E74, E75 from raw packets to evidence-v4.json
2. **Source E119-E125**: These customer satisfaction entries need to be sourced or removed
3. **Fix misattributed URLs**: E294/295 should point to PDD earnings + CNBC, not congress.gov. E67-69 should point to Sensor Tower, not Tranco.
4. **Qualify all analyst estimates**: Every "40% of GMV" type claim needs "(per [firm name], [time period])"
5. **Add source rows to tables**: Every table needs a bottom row with source attributions
6. **Fix wrong citations**: E30 is not CPSC data; E33 is not Tranco data; E23 is not ad intelligence
7. **Distinguish web vs app MAU**: The E42 vs E68 contradiction must be resolved
8. **Add time periods**: Every percentage change needs a from-date and to-date

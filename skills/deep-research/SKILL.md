# Deep Research: E-Commerce Company Analysis

A Claude SKILL that produces institutional-quality deep research reports on e-commerce companies, starting with PDD Holdings (Pinduoduo/Temu).

## Prerequisites

- Claude Code with `/browse` skill (gstack)
- Octagon AI MCP server (for SEC filings, earnings transcripts, financial metrics)
- Internet access for live data fetching

## How to Run

```
Run the /deep-research skill targeting PDD Holdings
```

The SKILL runs in 6 phases (including Phase 4.5: Mosaic Analysis), saving checkpoints after each phase so you can resume if anything fails.

## V2 Rules (apply to all phases)

### Date Awareness
- All WebSearch queries MUST include "2025 OR 2026" to ensure fresh results
- Prefer sources from the current year; flag any data older than 12 months

### Freshness Enforcement
- Every data point in checkpoint files must have an explicit date: `[DATE: 2026-03-15]` or `[DATE: unknown]`
- Every evidence.json entry must have a `date` field: `{"id": "E1", "url": "...", "quote": "...", "date": "2026-03-15"}`
- If publication date cannot be determined, use `"date": "unknown"`

### Freshness Report Card (end of Phase 5)
- Tally all sources by year
- Flag if <30% of sources are from the current year
- Include the report card at the end of the generated report

---

## Phase 1: Source Collection — Financial Data

**Tool: Octagon MCP (primary), /browse + SEC EDGAR API (fallback)**

Collect and save the following to `reports/pdd-holdings/sources/phase1-financials.md`:

### 1.0 Automated Data Collection (Run First)
Run: `bash scripts/orchestrate.sh pdd-holdings PDD 0001737806 --phase 1`
Review output in `reports/pdd-holdings/evidence-packets/sec-edgar-*.json`.
Then proceed to /browse below to fill gaps (earnings transcripts, analyst quotes).

### 1.1 PDD Holdings SEC Filings
- Fetch the most recent 20-F annual report (PDD Holdings, CIK: 0001737806)
- Extract: revenue by segment, operating expenses, net income, cash position, GMV commentary, risk factors
- Fetch last 4 quarters of 6-K filings
- Extract: quarterly revenue, margins, YoY growth rates, management commentary on Temu and domestic business

### 1.2 Earnings Transcripts
- Fetch the 3 most recent earnings call transcripts
- Extract: key quotes from management on Temu expansion, domestic strategy, regulatory response, capital allocation
- Extract: analyst questions (these reveal what institutional investors care about)

### 1.3 Financial Metrics
- Revenue (quarterly, trailing 4Q)
- Net income and adjusted net income
- Operating margin trajectory
- Cash and equivalents
- Share count and buyback activity
- Stock price history (1 year)

### 1.4 Fallback
If Octagon MCP is unavailable:
1. Use `/browse` to fetch PDD's 20-F from https://investor.pddholdings.com/financial-information/sec-filings
2. Use `/browse` to fetch earnings transcripts from Seeking Alpha
3. Use `curl` to query SEC EDGAR XBRL API: `https://data.sec.gov/api/xbrl/companyfacts/CIK0001737806.json`

### Checkpoint
Save all collected financial data to `reports/pdd-holdings/sources/phase1-financials.md` with clear section headers. Include the source URL for every data point.

---

## Phase 2: Source Collection — Alternative & Real-Time Data

**Tool: /browse (primary), Freightos (freight rates)**

Collect and save to `reports/pdd-holdings/sources/phase2-alternative.md`:

### 2.0 Automated Data Collection (Run First)
Run: `bash scripts/orchestrate.sh pdd-holdings PDD 0001737806 --phase 2`
Runs 11 skills: parcel-volume, customs-data, air-freight, freight-rates, app-intel,
web-traffic, google-trends, sentiment, job-postings, ad-intelligence, consumer-complaints.
Review output in `reports/pdd-holdings/evidence-packets/`. Use /browse to supplement stubs and fill gaps.

### 2.1 App Store & Usage Data
- `/browse` → Apple App Store: Temu ranking in Shopping category (US, UK, Germany, France, Japan, Brazil)
- `/browse` → Google Play Store: same markets
- `/browse` → Search for latest Sensor Tower or data.ai public reports on Temu downloads/MAU
- Note: Temu cumulative downloads exceeded 1.2B globally, 530M MAU as of Aug 2025 (verify with latest data)

### 2.2 Google Trends
- `/browse` → https://trends.google.com/trends/explore?q=temu — capture search interest trend for "Temu" globally, last 12 months
- Compare with "Shein" and "AliExpress" in same view
- Note any geographic breakdowns (US, Europe, LatAm)

### 2.3 Shipping & Logistics Data
- `/browse` → Search for latest Freightos World Container Index (China→US, China→EU rates)
- `/browse` → Search for "Temu daily package volume" or "Temu shipping volume" — ShipMatrix and Supply Chain Dive have reported ~900K packages/day in US
- `/browse` → Search for latest de minimis shipment data from US CBP — ~4M parcels/day enter US under Section 321
- `/browse` → Search for Temu warehouse expansion news (local warehouses handling 15-20% of US volume)

### 2.4 Job Posting Signals
- `/browse` → Indeed.com or LinkedIn: search "Temu warehouse" jobs — new locations = expansion signals
- Note cities/countries with new job postings

### 2.5 Consumer Sentiment
- `/browse` → Trustpilot Temu page: current rating, trend, common complaints
- `/browse` → Reddit r/Temu: recent top posts for qualitative sentiment

### 2.6 Regulatory Timeline
- `/browse` → US Trade Representative: latest on de minimis policy changes, Section 321 reform
- `/browse` → EU Commission: latest DSA enforcement actions on Temu, foreign subsidies investigation (Dec 2025 Dublin HQ raid)
- `/browse` → Search for "Temu tariff impact 2025 2026" — 145% tariff on sub-$800 imports caused 23% initial sales drop

### Checkpoint
Save all collected data to `reports/pdd-holdings/sources/phase2-alternative.md`. Include source URLs.

---

## Phase 3: Source Collection — China-Specific Data

**Tool: /browse**

Collect and save to `reports/pdd-holdings/sources/phase3-china.md`:

### 3.0 Automated Data Collection (Run First)
Run: `bash scripts/orchestrate.sh pdd-holdings PDD 0001737806 --phase 3`
Runs china-regulatory skill (SAMR, NDRC). Review output, then use /browse for remaining China data.

### 3.1 China App/Market Data
- `/browse` → QuestMobile English research reports: https://www.questmobile.com.cn/en/research/reports/
- Look for: Pinduoduo DAU/MAU, China e-commerce market share reports
- `/browse` → Business of Apps China e-commerce: https://www.businessofapps.com/data/china-ecommerce-market/
- `/browse` → CNNIC latest China internet statistics

### 3.2 Domestic Competitive Landscape
- `/browse` → Search for "China e-commerce market share 2025 Pinduoduo Alibaba JD Douyin"
- `/browse` → Search for "Douyin e-commerce growth 2025" — key competitive threat to PDD domestically
- `/browse` → Search for "Pinduoduo agricultural e-commerce" — unique positioning

### 3.3 Regulatory (China)
- `/browse` → Search for "China SAMR PDD Pinduoduo antitrust 2025"
- `/browse` → Search for "China common prosperity tech regulation 2025 update"

### 3.4 C2M and Factory Ecosystem
- `/browse` → Search for "Pinduoduo C2M consumer to manufacturer model"
- `/browse` → Search for "China factory capacity utilization 2025" — if domestic demand recovers, factories may deprioritize Temu

### Checkpoint
Save to `reports/pdd-holdings/sources/phase3-china.md`. Note if any Chinese-language sources were inaccessible and what was used as alternatives.

---

## Phase 4: Source Collection — Competitive Intelligence

**Tool: Octagon MCP (primary) + /browse**

Collect and save to `reports/pdd-holdings/sources/phase4-competitive.md`:

### 4.0 Automated Data Collection (Run First)
Run: `bash scripts/orchestrate.sh pdd-holdings PDD 0001737806 --phase 4`
Runs eu-regulatory and price-intel skills. Review output, then use /browse and Octagon for competitor filings.

### 4.1 Alibaba (BABA)
- Octagon MCP: latest 20-F, recent earnings transcript
- Extract: Taobao/Tmall GMV trends, international (AliExpress/Lazada) performance, ad monetization rates
- Compare take rates, active buyer trends, merchant count vs. PDD

### 4.2 JD.com (JD)
- Octagon MCP: latest 20-F, recent earnings transcript
- Extract: revenue growth, logistics investment, market share trends
- Compare delivery speed, customer demographics vs. PDD

### 4.3 Shein
- `/browse` → Search for "Shein revenue 2025", "Shein IPO", "Shein vs Temu"
- Extract: revenue estimates, geographic expansion, business model differences
- Key comparison: vertically integrated (Shein) vs. marketplace (Temu)

### 4.4 Amazon (AMZN)
- Octagon MCP: latest international segment data
- Focus on: how Amazon is responding to Temu (price matching, Haul feature)

### 4.5 Douyin/TikTok Shop
- `/browse` → Search for "Douyin e-commerce GMV 2025", "TikTok Shop growth"
- Key threat: live commerce eating into PDD's domestic market share

### Checkpoint
Save to `reports/pdd-holdings/sources/phase4-competitive.md`. Include comparison tables where possible.

---

## Phase 4.5: Mosaic Analysis

**Prerequisites:** All 4 phase checkpoint files (phase1-4) exist in `reports/pdd-holdings/sources/`.

**Tool: Analysis (no external tools needed)**

Read all 4 phase checkpoint files and produce `reports/pdd-holdings/sources/mosaic-analysis.md`:

### 4.5.1 Identify Converging Signals
- Cross-reference data points from different phases that independently point to the same conclusion
- Look for patterns that no single data source reveals alone
- Identify 2-3 "mosaics" — each connecting 3-7 data points from different phases into one original insight
- Each mosaic must have: a thesis statement, the contributing data points (with phase references), why these signals converge, and what the mosaic reveals that individual data points don't

### 4.5.2 Build Prediction Models
- From the mosaics, derive 3-5 falsifiable predictions
- Each prediction must have:
  - A specific, testable claim (e.g., "Temu European GMV will exceed $25B by Q4 2026")
  - Conviction level: High (>70%), Medium (40-70%), or Low (<40%)
  - Time horizon: when this prediction can be verified
  - Supporting evidence: which mosaic(s) and data points support it
  - "What would change our mind": specific data that would falsify the prediction
  - Leading indicators: what to watch in the next 3-6 months

### Checkpoint
Save to `reports/pdd-holdings/sources/mosaic-analysis.md` with clear sections for each mosaic and each prediction.

---

## Phase 5: Analysis & Report Generation

**Prerequisites:** All 4 phase checkpoint files AND `mosaic-analysis.md` exist in `reports/pdd-holdings/sources/`.

### 5.1 Read Reference Docs
Before writing, read these docs for quality standards and analytical framework:
1. `docs/reference-standard-analysis.md` — writing style, density requirements, quality checklist
2. `docs/institutional-research-standards.md` — evidence chain rules, anti-hallucination principles
3. `docs/pdd-analytical-framework.md` — valuation frameworks, KPIs, competitive dimensions, non-obvious angles

### 5.2 Read All Source Checkpoints
Read all 4 phase checkpoint files. Identify:
- Key data points for each section of the report
- Gaps where data was not available (note these honestly in the report)
- Contradictions between sources (address these explicitly)

### 5.3 Generate evidence.json FIRST

**Step 1:** Run the bridge to get auto-collected evidence:
```bash
python3 scripts/bridge/packets_to_evidence.py \
  --packets-dir reports/pdd-holdings/evidence-packets/ \
  --output reports/pdd-holdings/evidence-auto.json
```

**Step 2:** Review `evidence-auto.json` — these have machine-verified provenance (`provenance: "auto:<skill-name>"`). URLs came directly from API calls, not LLM memory.

**Step 3:** Manually add entries from /browse research (earnings quotes, news articles, analyst reports). Merge into final `evidence.json`:
```bash
python3 scripts/bridge/packets_to_evidence.py \
  --packets-dir reports/pdd-holdings/evidence-packets/ \
  --merge-with reports/pdd-holdings/evidence-manual.json \
  --output reports/pdd-holdings/evidence.json
```
Auto entries appear first, then manual entries. Every entry has a `provenance` field:
- `"auto:<skill-name>"` — URL from a script calling an API directly. Highest confidence.
- No provenance field — manually added from /browse research. Still verified, but spot-check recommended.

The final `evidence.json` format:
```json
[
  {
    "id": "E1",
    "url": "https://...",
    "quote": "exact quote or data point from the source",
    "date": "2026-03-15",
    "provenance": "auto:sec-edgar"
  },
  {
    "id": "E2",
    "url": "https://...",
    "quote": "...",
    "date": "unknown"
  }
]
```

Rules:
- Every entry must have a real, verifiable URL from the source collection phases
- The quote must be an actual excerpt or data point, not a paraphrase
- NEVER fabricate a URL or citation — if you're not sure of the exact source, omit the entry and note the gap
- Aim for 30-50 evidence entries covering all major claims in the report

### 5.4 Write the Report
Write `reports/pdd-holdings/report.md` following this structure:

#### Writing Rules (from reference docs)
- **Information density:** Every paragraph must contain at least one specific number, date, or verifiable fact. No filler paragraphs.
- **Take positions:** After presenting evidence, state your conclusion clearly. Use "we believe" for inference. Do NOT hedge with "however, there are also arguments to the contrary" unless you explain why those arguments are wrong.
- **No AI slop:** No "it's important to consider...", no "going forward...", no "significant growth." Use precise language.
- **Evidence-first:** Reference evidence.json entries using footnote markers [E1], [E2], etc. Every quantitative claim must have a corresponding evidence entry.
- **Vary sentence structure:** Mix short punchy statements after dense analytical paragraphs. Don't use uniform paragraph lengths.
- **Insight over information:** Don't just report what happened. Explain what it means and why it matters for investment decisions.

#### Report Structure

```markdown
# PDD Holdings: [Thesis Title — e.g., "Two Companies, One Price"]

*Published [date] | Deep Research Report*

## Executive Thesis
[1-2 paragraphs: the bold, specific claim about PDD. Not "PDD is a large e-commerce company" — something opinionated and evidence-based.]

## The Numbers That Matter
[Data-dense overview: key financial metrics, growth trajectory, cash position, valuation vs. peers. Include comparison table.]

## Pinduoduo: The Domestic Cash Machine
[Deep dive: social commerce model, C2M, agricultural focus, competitive position vs. Alibaba/JD/Douyin, ad monetization trajectory, regulatory landscape.]

## Temu: The International Bet
[Deep dive: full-managed model economics, geographic expansion (Europe >40% GMV), US tariff impact and adaptation, de minimis elimination implications, logistics network evolution, unit economics by geography.]

## The Evidence: What the Data Shows
[Quantitative analysis: Temu daily package volume, app ranking trends, Google Trends data, freight rate trajectory, job posting signals. Show the alternative data.]

## Regulatory Risk Map
[Specific and dated: EU FSR investigation, US de minimis changes, SAMR actions. Timelines and quantified impact for each.]

## Competitive Positioning
[Head-to-head: PDD vs Alibaba vs JD (domestic), Temu vs Shein vs Amazon (international). Use comparison tables with specific metrics.]

## The Mosaic
[2-3 mosaic insights from Phase 4.5. Each connects 3-7 data points from different phases into one original, non-obvious conclusion. Show the individual threads and how they weave together.]

## Predictions
[3-5 falsifiable predictions from Phase 4.5. Each must have: specific testable claim, conviction level (High/Medium/Low), time horizon, supporting evidence, "what would change our mind", and leading indicators to watch.]

## What the Market Is Missing
[2-3 non-consensus views, supported by evidence from the report. This is the highest-value section — it should tell the reader something they didn't know.]

## What's Different Since V1
[Summarize key changes from V1: new data, revised conclusions, updated metrics. Be specific about what moved and why.]

## Key Risks
[Bull case, base case, bear case with specific scenarios. Include the "what would have to be true for this to fail?" inversion.]

## Freshness Report Card
[Tally sources by year. Show percentage from current year. Flag any staleness concerns.]

## Sources
[List all evidence entries with URLs. This is the trust mechanism.]
```

### 5.5 Quality Check
After writing, verify the report against the quality checklist in `docs/reference-standard-analysis.md` Section 7:
- [ ] Every paragraph has a specific number, date, or fact
- [ ] No filler paragraphs
- [ ] Every quantitative claim links to evidence.json
- [ ] No fabricated citations
- [ ] Report takes clear positions
- [ ] At least 3 non-obvious insights
- [ ] Competitive comparisons use specific metrics
- [ ] Writing tone: confident, direct, slightly informal

If any check fails, revise the relevant section before finalizing.

---

## Output Files

After running all 5 phases, the following files should exist:

```
reports/pdd-holdings/
├── sources/
│   ├── phase1-financials.md      (SEC filings, transcripts, metrics)
│   ├── phase2-alternative.md     (app data, trends, shipping, sentiment)
│   ├── phase3-china.md           (QuestMobile, iResearch, CNNIC, SAMR)
│   └── phase4-competitive.md     (BABA, JD, Shein, AMZN, Douyin)
├── report.md                     (the final research report)
└── evidence.json                 (structured citations)
```

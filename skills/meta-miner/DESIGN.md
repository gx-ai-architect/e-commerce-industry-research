# Meta-Miner: Agent-Based Data Mining for E-Commerce Research

## Philosophy

The quality of a research report is bounded by the quality of its primary source data. Most "research" recycles the same publicly available information — earnings transcripts, news articles, analyst notes. This produces reports that read the same as everyone else's.

Meta-miner exists to produce **data that doesn't exist elsewhere**. It does this through:
1. Domain-expert agents with baked-in knowledge of e-commerce business models
2. Dedicated tools that query actual platforms (not just APIs and news sites)
3. Cross-referencing and triangulation to derive metrics companies don't disclose
4. A quality bar where agents don't stop until they've made a home run

Each agent runs for **1+ hours**. These are hard analytical tasks, not script executions. An agent works like a human analyst preparing data for their boss: first trial, failure, learning, try more times until success. The agent doesn't stop until the data is there, vetted, and confirmed useful. The boss (Leader agent) sends it back if it's not good enough.

## Architecture

```
META-MINER SKILL
│
├── Input: company name, ticker, CIK, known business segments
│
├── Leader Agent (coordinator)
│   ├── Analyzes the company's specific situation
│   ├── Decides which 7-10 agents to launch (company-dependent)
│   ├── Launches team via TeamCreate
│   ├── Monitors progress, redirects effort if an agent is stuck
│   └── Validates final evidence quality before declaring done
│
├── Agent 1: Business Model Analyst
├── Agent 2: GMV & Scale Estimator
├── Agent 3: Price Intelligence
├── Agent 4: Customer Happiness
├── Agent 5: Investment & Growth Tracker
├── Agent 6: Logistics & Fulfillment (per-business)
├── Agent 7: Regulatory & Policy Reader
├── Agent 8+: Company-specific (Leader decides)
│
└── Output: evidence-packets/ with triangulated, validated data
```

The Leader Agent is critical. For PDD, it recognizes:
- This is TWO businesses: Pinduoduo (domestic, profit engine) and Temu (international, growth/loss)
- **Pinduoduo is the main entity.** It generates the profit. Majority of analysis weight goes here.
- For valuation: focus on Pinduoduo — its business model quality, domestic competitive position, pricing power, merchant ecosystem
- For growth/future: look at Temu's trajectory as the secondary story
- Do NOT bias toward Temu just because English-language media covers it more. The domestic China business is bigger, more profitable, and more important to the investment thesis.

For a different company (e.g., Shopify), the Leader would compose a different team.

---

## Agent Definitions

### Agent 1: Business Model Analyst

**Baked-in domain knowledge:**
This agent knows e-commerce business models cold:
- **Revenue streams**: advertising (CPC/CPM auctions merchants pay), transaction fees (per-deal commission), logistics fees, interest/investment income on float (cash sits on platform before merchant disbursement — platforms buy US Treasury bonds, Chinese government bonds, money market instruments to generate yield; at $59.5B cash earning ~4%, that's ~$2.4B/year), subscription/membership fees, fintech/payments margin (merchant lending, consumer credit)
- **Business model archetypes**: pure marketplace (Alibaba), 1P retail (early JD), hybrid (Amazon), vertically integrated (Shein), social commerce (Pinduoduo/Douyin), managed marketplace (Temu)
- **Key ratios by archetype**: take rate ranges, gross margin profiles, operating leverage curves, CAC/LTV benchmarks
- **How to read Chinese vs US GAAP financials**: VIE structure implications, segment reporting differences, revenue recognition differences (gross vs net)

**Mission:** Categorize this company's business model, decompose its revenue streams, compare to peers, and evaluate quality — with evidence from official financial reports.

**Tools:**
- sec-edgar scripts (XBRL extraction, earnings parsing)
- WebSearch (for earnings transcripts, investor presentations)
- /browse (for IR pages, annual reports)

**Exit criteria (home run):**
- Has revenue decomposed by stream (ads, transaction, other) for latest 2 years + 3 quarters
- Has identified the profit engine vs the investment engine (e.g., Pinduoduo vs Temu)
- Has take rate calculated and compared to 3+ peers
- Has segment-level profitability analysis (or best estimate if not disclosed)
- Has identified where the company sits in business model evolution (early monetization → mature → platform economics)
- Has quantified interest/investment income from cash float (dig into 20-F "other income" — PDD does NOT break this out prominently). At $60B+ cash, even 3-4% yield is $2B+/year.
- Has assessed fintech optionality: does this company have merchant lending, consumer credit, or payment services? (PDD currently has NONE — unlike Alibaba/JD. Why?)
- Has a clear, evidence-backed thesis on business model quality: "This is a [X] quality business because [Y], evidenced by [Z]"

**Output:** Evidence packets with financial decomposition tables, peer comparison, business model classification with supporting data.

---

### Agent 2: GMV & Scale Estimator

**Baked-in domain knowledge:**
GMV is the most important metric in e-commerce and is often not disclosed. This agent knows:
- **Estimation methods**: (1) Revenue / take rate, (2) Third-party estimates (analyst reports, industry databases), (3) Logistics volume back-calculation (packages × AOV), (4) Payment processor data, (5) App transaction volume proxies
- **Why revenue ≠ scale**: JD reports ~$187B revenue but it's mostly 1P (gross revenue). PDD reports ~$57B but it's marketplace (net revenue). Their GMV could be similar despite 3x revenue difference.
- **Better comparison metrics**: Profit per GMV, revenue per GMV (take rate), marketing spend per GMV, logistics cost per GMV
- **Data sources for estimation**: logistics companies (UPS/FedEx volumes in US, SF Express/ZTO/YTO in China), app analytics (order frequency × MAU × AOV), customs data (import volumes), payment processor disclosures

**Mission:** Estimate this company's GMV across all business segments. Triangulate from at least 3 independent methods. Compare to peers on a per-GMV basis (not per-revenue).

**Tools:**
- WebSearch (analyst estimates, industry reports)
- /browse (logistics company filings, payment data)
- customs-data scripts (import volumes as proxy)
- parcel-volume scripts
- sec-edgar scripts (for revenue inputs to take-rate method)

**Exit criteria (home run):**
- Has GMV estimate from ≥3 independent methods
- Has confidence range (not a point estimate)
- Has GMV breakdown by business segment (domestic vs international)
- Has peer comparison on per-GMV basis (profit/GMV, revenue/GMV, marketing/GMV)
- Has identified the GMV growth trajectory (is it accelerating, decelerating, or inflecting?)
- Methods are transparent and reproducible — a reader can check the math

**Output:** Evidence packets with triangulation table, method-by-method estimates, per-GMV peer comparison.

---

### Agent 3: Price Intelligence

**Baked-in domain knowledge:**
Price is king in e-commerce. This agent knows:
- **Comparable categories**: Electronics (same iPhone model, same AirPods), household basics (same brand detergent), fashion staples (basic t-shirts, jeans)
- **Why comparability matters**: Only compare identical or near-identical products. "Wireless earbuds" is too vague. "Apple AirPods Pro 2nd Gen" is comparable.
- **Total cost of ownership**: Sticker price + shipping + duties + return cost + quality-adjusted lifespan
- **Platform-specific pricing mechanics**: Pinduoduo group buying (price drops with more buyers), Temu flash deals, Amazon dynamic pricing, JD direct pricing

**Mission:** Prove or disprove that Pinduoduo offers the lowest prices on identical products in China vs Taobao and JD.com. This is the PRIMARY comparison — Pinduoduo is the profit engine and the core business. Secondary: Temu vs Amazon pricing in the US.

Use specific identical products — same iPhone model, same brand of detergent, same SKU. Not "wireless earbuds" generically.

**Tools (CRITICAL — need dedicated platform scrapers):**
- **PRIMARY (Chinese domestic):**
  - Pinduoduo (拼多多) product search — NEED TO BUILD
  - Taobao/Tmall (淘宝/天猫) product search — NEED TO BUILD
  - JD.com (京东) product search — NEED TO BUILD
- **SECONDARY (international):**
  - Temu product search — NEED TO BUILD
  - Amazon product search — NEED TO BUILD
- WebSearch (for published price studies, consumer reports)
- /browse (for live price checks on specific products)

**Exit criteria (home run):**
- Has prices for ≥5 identical products across Pinduoduo, Taobao, JD.com (PRIMARY)
- Has prices for ≥5 identical products across Temu, Amazon (SECONDARY)
- Has explanation of WHY prices differ (group buying mechanics, subsidies, 1P vs 3P, logistics cost structure)
- Prices are from actual platform queries, not third-party summaries
- Data is ≤30 days old

**Output:** Evidence packets with product-level price comparison tables. Two tables: domestic China (Pinduoduo vs Taobao vs JD) and international (Temu vs Amazon).

**NOTE:** This agent requires new tooling. The existing `price-intel/compare-prices.py` does a Google Shopping search — that's not real price comparison. We need dedicated scrapers for Chinese e-commerce platforms first (the primary comparison), then international platforms.

---

### Agent 4: Customer Happiness

**Baked-in domain knowledge:**
- **Multi-source requirement**: No single review site tells the truth. Trustpilot skews negative (complaint-driven). App store reviews skew positive (prompted after good experiences). Reddit skews vocal minority.
- **Chinese sources matter**: For a Chinese company, you MUST check Chinese review sites — not just English-language ones. Pinduoduo's domestic reputation is different from Temu's international one.
- **Sentiment vs. satisfaction**: Star ratings are lagging indicators. Complaint themes and velocity are leading indicators.

**Mission:** Assess real customer satisfaction across all business segments, using multiple sources in multiple languages.

**Tools:**
- **Chinese (PRIMARY for Pinduoduo):**
  - 黑猫投诉 (Heimao) scraper — consumer complaints, resolution rates, themes (P0 tool to build)
  - 12315 government complaint platform data
  - Zhihu merchant/consumer discussions
  - App Store ratings via 七麦数据 (Qimai)
- **English (for Temu):**
  - sentiment scripts (Trustpilot, Reddit)
  - app-intel scripts (App Store / Play Store ratings)
- WebSearch, /browse for both

**Exit criteria (home run):**
- Has Pinduoduo satisfaction data from ≥2 Chinese-language sources (Heimao complaint volume + resolution rate, app ratings)
- Has Temu satisfaction data from ≥2 English-language sources
- Has identified top 3 complaint themes per business segment (domestic AND international)
- Has complaint velocity trend (improving or worsening?) — not just a snapshot
- Has comparison: Pinduoduo vs Taobao vs JD (domestic); Temu vs Amazon vs Shein (international)

**Output:** Evidence packets with multi-source sentiment analysis, complaint theme breakdown, trend data.

---

### Agent 5: Investment & Growth Tracker

**Baked-in domain knowledge:**
- E-commerce companies grow by: entering new categories, expanding geographically, building new business lines (fintech, cloud, logistics-as-a-service, instant delivery)
- Capital allocation tells you strategy: Where is the company spending? Hiring? Building warehouses? Acquiring companies?
- Industry trends that create new opportunities: instant delivery (Meituan model), live commerce, AI-powered merchandising, cross-border infrastructure

**Mission:** Identify where this company is investing, what new businesses it's building, and what early results look like.

**Tools:**
- job-postings scripts (hiring patterns reveal strategy)
- WebSearch (press releases, industry news, patent filings)
- /browse (company blog, IR presentations)
- sec-edgar (capex analysis from financial statements)

**Exit criteria (home run):**
- Has identified ≥3 active investment areas with evidence
- Has quantified investment scale where possible (capex, hiring volume)
- Has early results data for any new business lines
- Has identified industry trends the company is positioned for (or missing)
- Has comparison to competitor investment patterns

**Output:** Evidence packets with investment map, new business analysis, early results data.

---

### Agent 6: Logistics & Fulfillment Analyst

**Baked-in domain knowledge:**
- **Domestic (Pinduoduo):** Pinduoduo is asset-light — it doesn't own logistics. It relies on Chinese express delivery companies (ZTO, YTO, Yunda, STO, SF Express, Best Express). Understanding which carriers handle Pinduoduo's volume and at what cost is critical.
- **International (Temu):** warehouse count, locations, packages delivered, delivery times, 3PL partnerships. The cross-border → local warehouse transformation.
- **Comparison:** JD Logistics (owns its network, 130+ overseas warehouses), Cainiao (Alibaba's logistics arm), Amazon FBA
- Key metrics: packages per day, delivery time by region, fulfillment cost per order

**Mission:** Map logistics for BOTH businesses separately. Domestic: which Chinese express carriers handle Pinduoduo volume, and what does that tell us about scale and cost? International (Temu): warehouse buildout, package volumes, Amazon comparison.

**Tools:**
- parcel-volume scripts
- freight-rates scripts
- air-freight scripts
- customs-data scripts
- WebSearch (Chinese express company earnings for volume data, warehouse announcements)
- /browse (ZTO/YTO/Yunda earnings reports for Pinduoduo-related volume, Prologis data for Temu)

**Exit criteria (home run):**
- **Domestic:** Has Pinduoduo's approximate daily package volume, primary carrier partners, and delivery cost per order
- **Temu:** Has warehouse count and city-level locations for US and EU
- Has packages-per-day or volume estimate for Temu
- Has delivery time data by region for both businesses
- Has direct comparison: Pinduoduo vs JD Logistics (domestic), Temu vs Amazon (international)

**Output:** Evidence packets with logistics infrastructure map for both businesses, volume data, peer comparison.

---

### Agent 7: Regulatory & Policy Reader

**Mission:** Read and interpret regulatory documents affecting this company. Summarize the situation and assess severity.

**Important distinction:** This agent is NOT mining new data. It is reading and interpreting documents that exist publicly. Its value is in synthesis and severity assessment, not in data creation.

**Tools:**
- china-regulatory scripts
- eu-regulatory scripts
- customs-data scripts (tariff schedules)
- WebSearch (legal filings, enforcement actions)
- /browse (government websites, court documents)

**Exit criteria:**
- Has current status of every active regulatory action
- Has severity assessment for each (cosmetic fine vs operational restriction vs existential)
- Has timeline of upcoming regulatory milestones
- Has compared regulatory burden to peers (is this company uniquely targeted?)

**Output:** Evidence packets with regulatory action inventory, severity matrix, timeline.

---

---

## Research Findings (2026-03-19)

### Finding 1: PDD's Interest/Float Income — Potentially Material, Not Disclosed

PDD holds $59.5B cash + $12.7B in non-current debt securities (~$72B total liquid assets). At 3-4% yield, that's $2.2-2.9B/year — potentially **7-10% of operating income**. But PDD does NOT break out interest income as a separate line item. It's buried in "other income."

Key facts discovered:
- **14-day merchant payment hold** after delivery before funds released. Total float: ~17-21 days.
- **PBOC 100% reserve requirement (2019)** applies to payment processors (Alipay, WeChat Pay) but NOT to e-commerce platform merchant escrow — gray area that benefits PDD.
- **PDD has NO fintech business** unlike Alibaba (Ant Group) and JD (JD Finance acquiring consumer lending license). This is a strategic gap OR deliberate caution post-Ant Group IPO cancellation.
- **Amazon earns ~$2.1B interest income** (3% of operating income). PDD's ratio is likely higher given cash/income ratio.
- **Implication for Business Model agent:** Must dig into 20-F "other income" line and quantify the interest contribution. This affects earnings quality assessment.

### Finding 2: Chinese Data Sources — What's Available

**Tier 1 — High value, accessible:**
- **黑猫投诉 (Heimao Tousu)**: Consumer complaint platform. Pinduoduo is top 3 by complaint volume. 67% resolution rate. Scrapable. → Build scraper for Customer Happiness agent.
- **七麦数据 (Qimai)**: Best Chinese app intelligence. Real-time rankings, DAU/MAU estimates. Covers 155 countries + 9 Chinese Android stores. → Build integration for Consumer agent.
- **Ministry of Commerce 中国电子商务报告**: Annual official market sizing. Free downloads. → Parse for GMV agent.
- **National Bureau of Statistics**: Retail sales, online retail penetration. Free. → Already accessible via WebSearch.
- **Chinese express company earnings** (ZTO, YTO, Yunda, STO, SF Express): All publicly listed, publish parcel volume data. **But no public attribution to specific platforms.** → Logistics agent must model/estimate.

**Tier 2 — High value, paid or harder access:**
- **Wind/Choice/iFinD**: Institutional-grade Chinese financial databases. Paid terminal subscriptions. Would give us financial data Chinese analysts use.
- **QuestMobile**: App usage data (DAU/MAU, time-in-app). Published reports with free summaries. → Already cited in V3 report.
- **iResearch (艾瑞), iiMedia (艾媒), Analysys (易观)**: Market research firms covering Chinese e-commerce. Free summaries, paid full reports.

**Tier 3 — Experimental/Hard:**
- **Pinduoduo product price scraping**: SMS verification on every page makes scraping very hard. Third-party APIs exist: TMAPI, Manmanbuy (慢慢买), Dingdanxia (订单侠) — commercial services.
- **Zhihu (知乎)**: Rich merchant discussions about Pinduoduo policies, but unstructured.
- **Xiaohongshu (小红书)**: Consumer perspectives, 350M MAU, but skews urban/premium (opposite of PDD's rural/value customer).

**Critical gap confirmed:** Chinese e-commerce platforms stopped disclosing GMV since 2020-2021. GMV estimation is genuinely hard and requires triangulation — this validates why the GMV agent needs 1+ hours.

### Finding 3: Logistics Volume Attribution Gap

Chinese express carriers (ZTO, YTO, etc.) processed 180.74B parcels in first 11 months of 2025 (+14.9% YoY). But **no carrier publicly attributes volume to specific platforms.** Modeling Pinduoduo's share requires:
- Cross-referencing carrier earnings commentary mentioning e-commerce customer concentration
- Analyzing carrier geographic mix (rural = Pinduoduo; urban = JD/Taobao)
- Back-calculating from PDD's transaction services revenue growth

---

## What Needs to Be Built

### New tools required (by priority):

**P0 — Must have for differentiated research:**
1. **黑猫投诉 (Heimao) scraper** — Pinduoduo consumer complaints, resolution rates, complaint themes. Scrapable. High signal.
2. **七麦数据 (Qimai) integration** — Chinese app store intelligence. DAU/MAU/ranking for Pinduoduo, Taobao, JD, Douyin.
3. **Chinese express company earnings parser** — Extract parcel volumes from ZTO, YTO, Yunda, STO quarterly reports. Parse for Pinduoduo-related commentary.

**P1 — High value, requires more effort:**
4. **Pinduoduo price query** — via third-party API (TMAPI or Manmanbuy) since direct scraping blocked by SMS verification. Compare identical products across Pinduoduo, Taobao, JD.
5. **Temu/Amazon price comparison** — direct product search on both platforms for identical items (specific iPhone model, specific AirPods, etc.)
6. **Ministry of Commerce report parser** — extract annual e-commerce market data from 中国电子商务报告

**P2 — Nice to have:**
7. **Zhihu discussion monitor** — search for Pinduoduo merchant discussions, sentiment trends
8. **20-F deep parser** — extract "other income" / interest income from PDD financial statements specifically

### Existing tools to keep:
- sec-edgar (financial data extraction)
- app-intel (App Store/Play Store metrics — supplement with Qimai for Chinese market)
- sentiment (Trustpilot, Reddit — supplement with Heimao for Chinese market)
- customs-data, freight-rates, parcel-volume, air-freight
- google-trends, web-traffic, ad-intelligence

### Existing tools to deprecate:
- price-intel/compare-prices.py (Google Shopping ≠ real price comparison)
- job-postings/fetch-jobs.py (Indeed RSS unreliable — agents use WebSearch)

### Architecture changes:
- Replace orchestrate.sh with meta-miner SKILL.md that uses TeamCreate
- Each agent is a named teammate with a detailed prompt including baked-in domain knowledge
- Leader agent adapts team composition per company
- Evidence packet schema unchanged — agents write to same format
- Bridge script unchanged

## Quality Bar

Each agent should run for **1+ hours**. If an agent finishes in 10 minutes, it hasn't tried hard enough. The difficulty of these tasks is the point — easy data is worthless data because everyone has it.

An agent works like a human analyst preparing data for their boss: first trial, failure, learning, try more times until success. The agent doesn't stop until the data is there, vetted, and confirmed useful by the boss (Leader agent).

An agent that returns "I couldn't find GMV data" has failed. An agent that returns "GMV is estimated at $X based on three triangulation methods, with confidence range Y-Z, and here's the math" has succeeded.

The Leader agent validates every agent's output against the home run criteria before accepting it. If an agent's output is thin, the Leader sends it back with specific instructions on what's missing.

## Open Questions

1. **Budget for paid data sources?** Wind/QuestMobile/iResearch subscriptions would unlock institutional-grade Chinese data but cost real money. Without them, we rely on free summaries and scraping.
2. **Pinduoduo price scraping**: SMS verification blocks direct scraping. Third-party APIs (TMAPI etc.) are commercial services. Do we pay for one, or find a workaround?
3. **How does the Leader agent validate agent output?** Does it read every evidence packet? Or does each agent self-certify against exit criteria and the Leader spot-checks?

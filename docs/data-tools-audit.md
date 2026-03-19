# Data Tools Audit: What's Available for Institutional-Quality Research

Generated: 2026-03-18
Purpose: Map all available tools, APIs, and MCP servers that can feed the research SKILL, to determine the optimal tool stack for PDD Holdings analysis.

---

## The Problem

`/browse` alone cannot produce institutional-quality research because:
- It can't parse structured financial data (XBRL) from SEC filings
- It can't query APIs with parameters
- It gets limited/blocked content from paywalled sources
- It's inefficient for structured data that has dedicated APIs

## Available MCP Servers for Claude Code

### Tier 1: High-Value, Free, Ready to Use

| MCP Server | What It Provides | Cost | Install |
|------------|-----------------|------|---------|
| **[Octagon AI](https://github.com/OctagonAI/octagon-mcp-server)** | SEC filings (8000+ companies, 10-K/10-Q/8-K/20-F), **10 years of earnings transcripts**, financial metrics, stock data for 10,000+ tickers, private market data | Free | `claude mcp add` |
| **[EdgarTools](https://lobehub.com/mcp/sareegpt-edgartools-mcp)** | SEC EDGAR filings as structured data, XBRL parsing, financial statements as DataFrames, insider trades, fund holdings, multi-company comparison | Free, no API key | `pip install edgartools` + MCP config |
| **[Financial Datasets](https://docs.financialdatasets.ai/mcp-server)** | Income statements, balance sheets, cash flow, stock prices, market news | Free (OAuth) | `claude mcp add` with OAuth |
| **[Alpha Vantage](https://mcp.alphavantage.co/)** | Real-time/historical stock prices, forex, fundamentals | Free (25 calls/day) | `claude mcp add -t http alphavantage URL` |

### Tier 2: Valuable, Free or Freemium

| MCP Server / API | What It Provides | Cost | Notes |
|------------------|-----------------|------|-------|
| **[Beat & Raise SEC](https://beatandraise.com/mcp)** | SEC EDGAR filings as clean markdown, 13F holdings, insider transactions | Free | Good for reading full filing text |
| **[FMP (Financial Modeling Prep)](https://site.financialmodelingprep.com/)** | Fundamentals, SEC EDGAR data, 30+ years historical, financial ratios | Freemium (250 req/day free) | Has MCP server; good for competitor comparisons |
| **SEC EDGAR REST API** | Official XBRL data, company concepts, filing frames | Free, no auth | Direct curl calls, no MCP needed |
| **[Finnhub](https://finnhub.io/)** | Real-time quotes, company fundamentals, ESG scores, alternative data | Freemium (60 calls/min free) | No MCP server; use via curl |

### Tier 3: Premium / Institutional

| Tool | What It Provides | Cost | Notes |
|------|-----------------|------|-------|
| **[LSEG](https://www.lseg.com/)** | Institutional-grade: yield curves, bond data, FX rates, real-time news | Paid (enterprise) | Has MCP server; institutional-grade but expensive |
| **Bloomberg Terminal** | Everything | $24K/year | No MCP; not accessible to this project |
| **Sensor Tower / data.ai** | App downloads, MAU, retention | Paid API | Critical for Temu app data; no free alternative at quality |

---

## Non-MCP Data Sources (Use via /browse or curl)

### China-Specific Data (Biggest Gap)

| Source | What It Provides | Access | Language |
|--------|-----------------|--------|----------|
| **[QuestMobile](https://www.questmobile.com.cn/en/research/reports/)** | China mobile internet data, app DAU/MAU, user behavior | Free reports section | Chinese (some English) |
| **[iResearch](https://www.iresearch.com.cn/)** | China e-commerce market reports, industry analysis | Free reports (high quality) | Chinese |
| **[CNNIC](https://www.cnnic.net.cn/)** | China Internet statistics, e-commerce penetration | Free | Chinese (English summaries) |
| **China NBS** | National statistics, retail data, GDP | Free | Chinese/English |
| **[Business of Apps](https://www.businessofapps.com/data/china-ecommerce-market/)** | Aggregated China e-commerce statistics | Free | English |

### Global E-Commerce Data

| Source | What It Provides | Access |
|--------|-----------------|--------|
| **Google Trends** | Search interest over time | Free, via /browse |
| **Statista** | Market sizing, industry stats | Freemium (limited free) |
| **US Census Bureau** | E-commerce penetration, retail data | Free |
| **SimilarWeb** | Web traffic estimates | Freemium |
| **Google Patents / USPTO** | Patent filings | Free |

### Regulatory / Legal

| Source | What It Provides | Access |
|--------|-----------------|--------|
| **EU Commission** | DSA enforcement, foreign subsidies investigation | Free, via /browse |
| **US CBP / USTR** | Tariff policy, de minimis changes | Free, via /browse |
| **China SAMR** | Antitrust enforcement | Free, Chinese language |

---

## Recommended Tool Stack for PDD Holdings Report

### Must-Have (install before running SKILL)

| Tool | Role | Why |
|------|------|-----|
| **Octagon AI MCP** | SEC filings + earnings transcripts | Single MCP gives us 20-F filings, 10 years of earnings transcripts, financial metrics, AND stock data. Covers PDD + all competitors (BABA, JD, AMZN, SHOP). This is the biggest quality multiplier. |
| **`/browse`** | News, regulatory, industry pages, Chinese sources | Handles everything that's a web page — earnings analysis, regulatory actions, iResearch/QuestMobile free reports, Google Trends |

### Nice-to-Have (adds depth)

| Tool | Role | Why |
|------|------|-----|
| **Financial Datasets MCP** | Structured income statements, balance sheets | Complements Octagon with clean financial data via OAuth |
| **Alpha Vantage MCP** | Stock price history, basic fundamentals | Useful for price charts and historical comparisons |
| **EdgarTools (Python)** | XBRL parsing, custom financial queries | More flexible than Octagon for custom analysis, but requires Python |

### Not Needed for v1

| Tool | Why Skip |
|------|----------|
| LSEG / Bloomberg | Enterprise-grade, expensive, overkill for v1 |
| Sensor Tower / data.ai | Paid; use /browse to scrape free app ranking data instead |
| FMP | Overlaps with Octagon + Financial Datasets |
| Custom scrapers | Premature; /browse covers web scraping needs |

---

## Tool Stack Decision Matrix

| Data Need | Primary Tool | Fallback |
|-----------|-------------|----------|
| PDD 20-F annual report | Octagon MCP | /browse → SEC EDGAR |
| Quarterly earnings data | Octagon MCP | /browse → IR page |
| Earnings call transcripts | Octagon MCP (10 years) | /browse → Seeking Alpha |
| Financial metrics & ratios | Octagon MCP | Financial Datasets MCP |
| Competitor filings (BABA, JD) | Octagon MCP | EdgarTools |
| Stock price history | Alpha Vantage MCP | /browse → Yahoo Finance |
| China app DAU/MAU data | /browse → QuestMobile reports | /browse → Business of Apps |
| China e-commerce market data | /browse → iResearch free reports | /browse → CNNIC |
| Temu app rankings | /browse → app store pages | /browse → data.ai free tier |
| EU regulatory actions | /browse → EU Commission | — |
| US tariff / de minimis | /browse → USTR, CBP | — |
| China SAMR antitrust | /browse → SAMR (Chinese) | — |
| Google Trends | /browse → trends.google.com | — |
| Patent filings | /browse → Google Patents | — |
| Academic papers | /browse → Google Scholar, SSRN | — |
| News / deep reporting | /browse → FT, Bloomberg (free previews) | — |

---

## Gaps That Cannot Be Closed (Honest Assessment)

1. **Paywalled journalism** (Bloomberg, FT, The Information) — cannot access full articles. Mitigation: use free previews, cross-reference with free sources.

2. **Premium app analytics** (data.ai, Sensor Tower full data) — need paid subscription for granular Temu download/retention data. Mitigation: use free tier + public app store rankings.

3. **Chinese proprietary data** (QuestMobile full dataset, iResearch premium) — most granular China data requires enterprise subscriptions. Mitigation: use their free published reports + government statistics.

4. **Expert network insights** (GLG, AlphaSights calls) — institutional analysts get exclusive expert interviews. Cannot replicate. Mitigation: use earnings call Q&A as a proxy for management access.

5. **Supply chain intelligence** (the kind SemiAnalysis has for semiconductors) — no equivalent free source for e-commerce supply chain. Mitigation: use job postings, logistics partner filings, satellite imagery references from public reports.

---

---

## Alternative Data: What a SemiAnalysis-Tier E-Commerce Analyst Actually Uses

Financial filings tell you what happened last quarter. Alternative data tells you what's happening RIGHT NOW. This is where the gap between "good" and "brilliant" research lives.

### The Alternative Data Stack for E-Commerce

| Data Type | What It Reveals | Free/Accessible Options | Premium (Paid) |
|-----------|----------------|------------------------|----------------|
| **App Store Rankings** | Real-time Temu adoption by country | [Apify App Rankings Scraper](https://apify.com/slothtechlabs/ios-android-app-rankings-scraper) (cheap), [SearchAPI](https://www.searchapi.io/docs/apple-app-store-top-charts-api), /browse → app store pages | Sensor Tower, data.ai, Apptopia |
| **Web Traffic** | Temu.com visits, conversion signals | [SimilarWeb](https://www.similarweb.com/) free tier, /browse | SimilarWeb Pro |
| **Shipping/Freight Rates** | Cross-border logistics cost trends | [Freightos](https://ship.freightos.com/api/shippingCalculator) (free rate estimates, no API key), [Karrio](https://www.karrio.io/) (open source) | FreightWaves SONAR, Xeneta |
| **Package Volume** | Temu's actual shipping scale | /browse → ShipMatrix reports, Supply Chain Dive, de minimis data from US CBP | ShipMatrix, Pitney Bowes |
| **Credit Card / Transaction Data** | Real GMV estimation, market share | Not freely available | YipitData, Earnest Research, Second Measure |
| **Job Postings** | Hiring signals = expansion plans | /browse → LinkedIn, Indeed, Glassdoor | Thinknum, LinkUp |
| **Satellite Imagery** | Warehouse expansion, parking lot traffic | Not freely available for analysis | Planet Labs, Maxar, RS Metrics |
| **Google Trends** | Search interest = consumer demand | /browse → trends.google.com | — |
| **Social Sentiment** | Brand perception, complaints | /browse → Reddit, Twitter/X, Trustpilot | Brandwatch, M Science |
| **App Reviews** | User satisfaction, product quality signals | /browse → App Store / Google Play reviews, [Appbot API](https://appbot.co/features/api/) | AppFollow, Apptopia |
| **Customs/Trade Data** | Import volumes by company | /browse → US Census Foreign Trade, USITC DataWeb | ImportGenius, Panjiva (S&P Global) |

### Specific Data Points for a Brilliant PDD Report

These are the "connect the dots" data points that separate an institutional report from a summary:

1. **Temu daily package volume** — ~900K packages/day in US (ShipMatrix data, available via /browse). This is a proxy for GMV that doesn't require credit card data.

2. **De minimis shipment volume** — ~4M parcels/day enter US under Section 321. Temu + Shein account for ~600K/day combined. Available from US CBP data and reporting.

3. **Freight rate trends** — Freightos World Container Index tracks ocean shipping costs. Air freight rates available from TAC Index. Both indicate Temu's logistics cost trajectory.

4. **App store rankings by country** — Temu's rank in Shopping category across 50+ countries. Available via Apify scraper or /browse. Shows geographic expansion momentum.

5. **Temu cumulative downloads** — 1.2B+ global downloads, 530M MAU (Sensor Tower data cited in public reporting, fetchable via /browse).

6. **Warehouse expansion signals** — Job postings for warehouse workers in specific cities = new fulfillment centers. /browse → Indeed/LinkedIn.

7. **Temu local warehouse penetration** — 15-20% of US volume via local warehouses (2025). This is the key metric for de minimis risk mitigation.

8. **Google Trends: "Temu" search interest** — By country, over time. Free, instant, available via /browse.

9. **Trustpilot/BBB ratings** — Consumer satisfaction trends. Available via /browse.

10. **EU regulatory timeline** — DSA enforcement, foreign subsidies investigation, de minimis elimination schedule. Available via /browse → EU Commission.

### How This Changes the Tool Stack

The alternative data sources are mostly accessible via `/browse` + targeted scraping. The key additions:

| Tool | Role | Why Add It |
|------|------|-----------|
| **Freightos** (no API key needed) | Ocean/air freight rate estimates | Directly estimates Temu's shipping cost trajectory |
| **Apify App Rankings** | App store rankings scraper | Cheap alternative to Sensor Tower for Temu rank by country |
| **Google Trends** (via /browse) | Search interest trends | Free proxy for consumer demand |
| **US CBP / Census trade data** (via /browse) | Import volumes, de minimis stats | Quantifies Temu's actual shipping scale |

---

## Revised Tool Stack Recommendation

### The Stack (in priority order)

| # | Tool | Data It Unlocks | Access Method |
|---|------|----------------|---------------|
| 1 | **Octagon AI MCP** | SEC filings, earnings transcripts (10 years), financial metrics, stock data | MCP server |
| 2 | **`/browse`** | News, regulatory, Chinese sources, industry reports, Google Trends, app store pages, job postings, social sentiment, trade data | Web browsing |
| 3 | **Freightos** | Shipping rate estimates (air/ocean) for Temu logistics cost analysis | Free API (no key) or /browse |
| 4 | **SEC EDGAR REST API** | Structured XBRL financial data for custom queries | curl (no auth) |

### What the SKILL Should Do With Each Tool

The SKILL should specify a **source collection phase** that systematically gathers data from each tool:

```
PHASE 1: FINANCIAL DATA (Octagon MCP)
├── Fetch PDD 20-F (latest annual report)
├── Fetch last 4 quarters of 6-K filings
├── Fetch 3 years of earnings transcripts
├── Fetch comparable filings: BABA, JD, AMZN, SHOP
├── Extract: revenue, margins, cash, GMV estimates, segment data
└── Extract: management commentary on Temu, domestic business, regulatory risk

PHASE 2: ALTERNATIVE DATA (/browse + Freightos)
├── Google Trends: "Temu" search interest by country (last 12 months)
├── App Store: Temu ranking in Shopping category (US, UK, DE, FR, JP, BR)
├── Freightos: current China→US and China→EU ocean/air freight rates
├── US CBP: latest de minimis shipment volume data
├── ShipMatrix / Supply Chain Dive: Temu daily package volume estimates
├── LinkedIn/Indeed: Temu warehouse job postings (new locations = expansion)
├── Trustpilot: Temu rating trend (last 12 months)
└── EU Commission: latest DSA enforcement actions on Temu

PHASE 3: CHINA-SPECIFIC (/browse)
├── QuestMobile free reports: Pinduoduo app DAU/MAU
├── iResearch free reports: China e-commerce market share
├── CNNIC: China internet/e-commerce statistics
├── SAMR: recent antitrust actions
└── PDD IR page: latest press releases, presentations

PHASE 4: COMPETITIVE INTELLIGENCE (Octagon MCP + /browse)
├── Alibaba latest earnings + transcript (Octagon)
├── JD.com latest earnings + transcript (Octagon)
├── Shein: funding, valuation, expansion (news via /browse)
├── Amazon: marketplace seller data, international e-commerce (Octagon)
└── Douyin/TikTok Shop: China e-commerce disruption (news via /browse)
```

## Gaps That Cannot Be Closed (Updated)

1. **Credit card transaction data** (YipitData, Earnest Research) — the gold standard for GMV estimation. No free alternative. Mitigation: use package volume + ASP estimates as GMV proxy.
2. **Premium app analytics** (Sensor Tower full data) — granular retention, cohort analysis. Mitigation: use public download figures + app store rankings.
3. **Satellite imagery** (warehouse parking lot analysis) — too expensive. Mitigation: use job posting signals for expansion.
4. **Paywalled journalism** — Bloomberg, FT full articles. Mitigation: free previews + cross-reference.
5. **Chinese proprietary data** (QuestMobile/iResearch full datasets) — enterprise subscriptions. Mitigation: their free published reports.

## Conclusion

**The revised tool stack (Octagon MCP + /browse + Freightos + SEC EDGAR API) covers ~85% of what an institutional analyst would use.** The key insight from this audit: most "alternative data" for e-commerce is actually accessible via clever use of /browse — Google Trends, app store rankings, job postings, shipping volume reports, regulatory filings, and social sentiment are all on the public web. The SKILL needs to know WHERE to look, not just HOW to browse.

The 15% gap (credit card data, premium app analytics, satellite imagery) is what separates a $50K/year Bloomberg terminal subscription from a free tool. We can't close it, but we can be honest about it in the report — and that honesty itself builds trust.

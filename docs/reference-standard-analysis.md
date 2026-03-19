# Reference Standard Analysis: What Makes a Gold-Standard Research Report

Generated: 2026-03-18
Purpose: Establish the quality bar for the deep research agent by analyzing what makes institutional-quality research reports brilliant, trusted, and actionable.

---

## 1. The Gold Standard: SemiAnalysis

### Why SemiAnalysis Is the Reference

SemiAnalysis (founded by Dylan Patel) is the second-largest tech Substack with ~50,000 subscribers and is considered "the preeminent authority on all things AI and semiconductors." Institutional investors, VCs, and industry executives pay for it because it consistently delivers analysis they can't get anywhere else — not from sell-side research, not from consulting firms, not from journalism.

The TPUv7 report ("Google TPUv7: The 900lb Gorilla In the Room," Nov 2025) exemplifies every quality dimension we want to replicate.

### What Makes It Brilliant

#### 1.1 Information Density

Every paragraph introduces new information or analysis. There is zero filler. Compare:

**SemiAnalysis (dense):** "Anthropic ordering 1M+ TPUs total (400k TPUv7 Ironwood direct purchase at ~$10B from Broadcom, 600k via GCP at ~$1.60/TPU-hour, representing ~$42B in RPO)."

**Typical AI output (diluted):** "Anthropic has made significant investments in TPU infrastructure, demonstrating their commitment to leveraging Google's hardware ecosystem for their growing AI workloads."

The first sentence contains 5 distinct data points. The second contains zero. This is the core difference between institutional research and AI-generated content.

**Density technique:** Stack multiple quantitative facts into single sentences. Every clause should carry new information. If a sentence could be removed without losing a data point, remove it.

#### 1.2 Primary Source Access

The TPUv7 report draws from:
- **Supply chain intelligence:** Broadcom order volumes, fab-by-fab production data, datacenter tracking
- **Financial modeling:** Proprietary TCO models, tokenomics models, accelerator industry models
- **Technical specifications:** Hot Chips 2025 conference proceedings, architecture diagrams
- **Commercial terms:** GCP pricing structures, Anthropic deal terms, FluidStack deployment details
- **Competitive intelligence:** Nvidia earnings calls (Bernstein Research), Meta communications
- **Software ecosystem tracking:** GitHub commit activity on vLLM, SGLang, PyTorch/XLA
- **Conference presentations and industry events**

**Key insight for automation:** SemiAnalysis's advantage comes from industry contacts and leaked documents that an automated agent cannot access. However, a substantial portion of their analysis is built on *publicly available* primary sources — SEC filings, earnings transcripts, patent databases, GitHub repos, conference proceedings, and company press releases. The automated agent must maximize extraction from these public sources.

#### 1.3 Analytical Framework

The TPUv7 report follows a consistent analytical pattern:

1. **Provocative framing:** Opens with a bold claim ("Is this the end of Nvidia's dominance?")
2. **Historical context:** Establishes the trajectory (Google's TPU development 2006-2016)
3. **Thesis validation:** References prior analysis and checks it against new evidence
4. **Quantitative comparison:** Head-to-head metrics (TPUv7 vs GB200 TCO, MFU breakeven analysis)
5. **System-level analysis:** Goes beyond chip specs to evaluate the full stack (rack architecture, networking, software ecosystem)
6. **Commercial structure:** Maps the business relationships and deal economics
7. **Forward-looking implications:** What this means for the competitive landscape

**Key insight:** The framework is not "here's what happened." It's "here's what this means, and here's the evidence."

#### 1.4 Writing Style

- **Confident but calibrated:** Uses "we believe," "we estimate," "we hypothesize" to distinguish fact from inference — but the tone is assertive, not hedging
- **Colloquial authority:** "900lb Gorilla," "eye-watering," "threading the needle" — feels like a knowledgeable insider talking, not an academic writing
- **Skeptical of marketing:** Explicitly calls out Nvidia/AMD FLOP inflation through DVFS manipulation
- **Direct and opinionated:** Takes clear positions rather than presenting "on one hand... on the other hand"
- **Insider language:** References internal Google naming conventions, team dynamics — signals deep domain access

**Anti-pattern to avoid:** AI tends toward diplomatic, hedge-filled, both-sides writing. SemiAnalysis takes positions and defends them with data.

#### 1.5 Visual Elements

The TPUv7 report contains 14+ distinct visual elements:
- Peak FLOP comparison charts (timeline view)
- Architecture evolution diagrams (systolic array progression)
- Memory hierarchy comparison tables
- TCO comparison matrices (multiple scenarios)
- MFU vs. cost breakeven charts
- Rack architecture diagrams (component layout)
- 3D torus topology visualizations
- Optical circuit switch mechanics
- Multi-cube scaling diagrams
- DCN architecture diagrams
- GitHub contribution timelines
- API support matrices

**Key insight:** Visuals are not decorative. Every chart makes a specific analytical point. They are placed immediately after the claim they support. The reader never has to hunt for evidence — it's right there.

#### 1.6 Evidence Chain

SemiAnalysis uses a layered citation approach:
- **Hyperlinked references** embedded inline in the text
- **Self-referential authority:** "Our AI Cloud TCO Model," "Our Tokenomics Model" — proprietary models named and referenced
- **Gray literature as primary sources:** Earnings calls, conference presentations treated with the same weight as published papers
- **GitHub activity as evidence:** Commit timelines used as contemporaneous proof of software progress
- **Methodology transparency:** Explicitly states when something is an estimate vs. confirmed fact
- **Source attribution spectrum:** From named sources to anonymous ("we understand") — clearly distinguished

---

## 2. Institutional Research Taxonomy

### 2.1 Sell-Side Equity Research (Goldman Sachs, Morgan Stanley, JP Morgan)

**Standard structure:**
1. Executive Summary (single page — most investors read nothing else)
2. Investment Thesis (what the market is missing)
3. Company Overview
4. Industry & Competitive Analysis
5. Financial Model & Forecasts (revenue, margins, cash flow projections)
6. Valuation (DCF + comparable company analysis)
7. ESG Considerations
8. Risk Assessment (quantified, not just listed)
9. Appendix / Disclosures

**What makes them trusted:**
- Institutional backing and regulatory compliance (FINRA requirements)
- Named analysts with track records and accountability
- Quantitative rigor: specific price targets, explicit assumptions
- Comp tables: market cap, EV/EBITDA, P/E, revenue growth, margins for peer group
- Assumptions transparency: any reader can challenge the model inputs

**Primary sources:** Bloomberg terminal data, company filings, management access (earnings calls, NDRs), industry databases (FactSet, Capital IQ), proprietary surveys

**Weakness:** Often formulaic, consensus-driven, and constrained by compliance. Rarely takes truly contrarian positions. Updates can be stale by the time they publish.

### 2.2 Independent Research (SemiAnalysis, Stratechery, Livemore Partners)

**What gives them credibility without institutional backing:**
- **Domain depth:** Analysts who are practitioners, not generalists
- **Speed:** Publish faster than institutional research
- **Contrarian willingness:** No compliance department preventing bold claims
- **Transparency of methodology:** Show their work, invite challenge
- **Track record visibility:** Prior predictions are publicly verifiable
- **Direct audience relationship:** Subscribers pay for quality, not brand

**Key differentiator:** Independent research earns trust through demonstrated expertise and track record. Institutional research borrows trust from the brand. For an automated agent, trust must be earned — every claim needs visible evidence.

### 2.3 Consulting Research (McKinsey Global Institute, Bain, BCG)

**Analytical frameworks:**
- Market sizing (TAM/SAM/SOM with bottoms-up methodology)
- Competitive landscape mapping (strategic group analysis)
- Value chain analysis
- Porter's Five Forces variants
- Cost curve analysis
- Customer segmentation and willingness-to-pay analysis

**Presentation patterns:**
- Heavy use of 2x2 matrices and frameworks
- Synthesis-first: lead with the conclusion, then support
- Data visualization as primary communication medium
- "So what?" explicitly stated for every data point

**What makes them trusted:** Proprietary survey data, client access, large analyst teams, polished production quality

**Weakness:** Often generic, framework-heavy, and lacking the technical depth of specialist research. The frameworks can feel like templates applied to any industry.

### 2.4 Open-Source Research (ARK Invest Model)

**How ARK makes institutional research freely available:**
- Publishes research openly to "enlighten investors and seek feedback"
- Open-sources valuation models on GitHub (e.g., Roku model)
- Explicitly shares assumptions and invites public challenge
- Uses crowdsourced insights from external "Theme Developers"
- Daily portfolio holdings disclosure (unusual transparency)
- Regular public engagement via podcasts, webinars, social media

**Publishing format:**
- "Big Ideas" annual reports (free, comprehensive thematic analysis)
- White papers on specific technologies
- GitHub repositories with editable financial models
- Blog posts and research notes

**Key insight for our project:** ARK's model proves that giving research away for free can build enormous credibility and audience. The transparency of showing your models and assumptions is itself a trust mechanism.

---

## 3. Anti-Patterns: What Makes Research Untrustworthy

### 3.1 AI-Generated Research Red Flags

Harvard Business School research (Yuan Zou) found that **AI-generated stock analysis led to lower trading volumes** for covered stocks, with smaller average returns vs. human-written analysis. Investors found AI-produced information "inferior to insights from people."

**Specific anti-patterns investors detect and reject:**

1. **Hedge-filled writing:** "It's important to consider..." "There are several factors that could..." "While there are risks, there are also opportunities..." — this signals no actual position or insight.

2. **False balance:** Presenting "on one hand... on the other hand" when the evidence clearly supports one conclusion. Real analysts take positions.

3. **Phantom citations:** Referencing sources that don't exist or mischaracterizing what sources actually say. This is the #1 trust-destroyer. A single hallucinated citation invalidates the entire report.

4. **Generic frameworks applied without insight:** Using Porter's Five Forces or SWOT without adding any information the reader doesn't already know. The framework is visible but empty.

5. **Temporal vagueness:** "In recent years..." "Going forward..." "The market is expected to grow..." — no specific dates, quarters, or timeframes. Real research anchors claims to specific time periods.

6. **Verbal inflation:** "Revolutionary," "game-changing," "unprecedented" — superlatives without evidence. Real analysts use precise language.

7. **Missing the "so what?":** Presenting data without explaining why it matters. "Revenue grew 15% YoY" is information. "Revenue grew 15% YoY despite a 23% tariff-induced drop in US sales, meaning non-US revenue grew ~40% — signaling that geographic diversification is working faster than expected" is insight.

8. **Lack of specific numbers:** "Significant growth," "substantial market share," "considerable investment" — vague qualifiers instead of precise figures.

9. **Uniform paragraph structure:** AI tends to produce paragraphs of similar length and structure. Real writing varies rhythmically — short punchy sentences after dense analytical paragraphs.

10. **No surprises:** AI research tends to confirm conventional wisdom. The most valuable research tells you something you didn't already know or challenges something you believed.

### 3.2 The Information vs. Insight Distinction

| Information | Insight |
|-------------|---------|
| PDD revenue grew 9% YoY in Q3 2025 | PDD's revenue deceleration from 44% to 9% YoY in 4 quarters suggests Temu's subsidy-driven growth model is hitting natural limits |
| Temu expanded to 50+ countries | Europe now contributes ~40% of Temu GMV, surpassing the US (~30%), reflecting a deliberate geographic pivot away from US tariff risk |
| PDD has RMB 424B cash | PDD's $60B cash pile represents 40% of its market cap — either massive optionality or capital misallocation depending on deployment |
| EU plans to eliminate de minimis threshold | The de minimis elimination forces a structural business model change: Temu must shift from pure cross-border to local warehousing, fundamentally changing its unit economics |

**The pattern:** Information is what happened. Insight is what it means and why it matters. Every paragraph in a gold-standard report should contain insight, not just information.

---

## 4. The Quality Dimensions That Transfer to E-Commerce Research

### Dimensions That Transfer Directly from SemiAnalysis

| Dimension | Semiconductor Application | E-Commerce Application |
|-----------|--------------------------|----------------------|
| Supply chain intelligence | Fab-by-fab production, chip order volumes | Warehouse expansion, logistics partner deals, seller onboarding rates |
| TCO modeling | Chip cost vs. performance vs. system cost | Unit economics: CAC, LTV, take rate, fulfillment cost per order |
| Competitive benchmarking | TPU vs GPU performance/cost matrices | PDD vs Alibaba vs JD marketplace metrics, Temu vs Shein vs Amazon |
| Software ecosystem analysis | CUDA vs TPU compiler maturity | Platform tools, seller APIs, payment infrastructure, app ecosystem |
| Commercial deal structure | Cloud GPU pricing, Anthropic TPU deal terms | Seller fee structures, advertising economics, logistics pricing |
| Regulatory risk mapping | Export controls, CHIPS Act impact | De minimis changes, EU DSA, SAMR antitrust, US tariff policy |
| Quantitative forward modeling | MFU breakeven analysis, scaling projections | GMV growth modeling, margin trajectory, geographic mix shift |

### Dimensions Unique to E-Commerce

- **Consumer behavior analysis:** App download trends, DAU/MAU, session time, purchase frequency — available via data.ai, SimilarWeb
- **Seller ecosystem health:** Number of active sellers, seller churn, average seller revenue — partially available via company disclosures and third-party tools
- **Logistics network mapping:** Warehouse locations, shipping routes, fulfillment times — available via company filings, job postings, satellite imagery
- **Pricing intelligence:** Product pricing comparisons vs. Amazon, AliExpress — available via scraping tools
- **Regulatory timeline tracking:** De minimis elimination schedule, EU DSA compliance deadlines, tariff implementation dates

### Dimensions That Don't Transfer (Semiconductor-Specific)

- Technical architecture deep dives (systolic arrays, torus topologies) — e-commerce doesn't have hardware architecture analogues
- Fabrication process analysis — no equivalent in e-commerce
- Chip-level performance benchmarking — replaced by platform-level metrics

---

## 5. PDD Holdings: Available Primary Source Map

### Tier 1: Richest Sources (Free, Deep, Primary)

| Source | URL | Freshness | Depth |
|--------|-----|-----------|-------|
| SEC 20-F Annual Report | sec.gov/Archives/edgar/data/1737806/ | FY2024 filed Apr 2025 | Comprehensive: financials, risk factors, business description, VIE structure |
| SEC 6-K Interim Reports | investor.pddholdings.com/sec-filings | Quarterly | Earnings releases, material events |
| Earnings Call Transcripts | Seeking Alpha, Motley Fool (free) | Q3 2025 (latest) | Management commentary, Q&A with analysts |
| PDD Investor Relations | investor.pddholdings.com | Ongoing | Press releases, annual reports, presentations |

### Tier 2: Valuable Sources (Free or Partially Free)

| Source | What It Provides | Access |
|--------|-----------------|--------|
| Competitor 20-F filings (Alibaba, JD.com) | Comparable metrics, market commentary | Free via SEC EDGAR |
| data.ai / SimilarWeb | App rankings, download estimates, web traffic | Freemium (limited free tier) |
| Google Patents / USPTO | PDD patent filings (social commerce, logistics tech) | Free |
| GitHub (if any open source) | Technical infrastructure signals | Free |
| US Census Bureau | E-commerce penetration data | Free |
| China NBS | Domestic retail and e-commerce statistics | Free |

### Tier 3: News & Analysis (Quality Varies)

| Source | Quality Assessment |
|--------|-------------------|
| Financial Times / Bloomberg | Substantive reporting, especially on regulatory actions |
| The Information | Deep tech/business reporting, some behind paywall |
| Seeking Alpha | Mixed — ranges from excellent to retail speculation |
| CMBIGM, DBS, Gelonghui research | Institutional analyst reports, often behind terminals |

### Tier 4: Regulatory & Legal

| Source | What It Covers |
|--------|---------------|
| EU Commission (DSA enforcement) | December 2025 raid on Temu's Dublin HQ, foreign subsidies investigation |
| US CBP / USTR | De minimis exemption changes, 145% tariff on sub-$800 imports |
| China SAMR | Antitrust enforcement, platform economy regulations |

### Source Quality Assessment

**Sufficient for a brilliant report?** Yes — if maximally extracted. The 20-F alone is 200+ pages of detailed financials, risk disclosures, and business description. Combined with earnings transcripts, competitor filings, and industry data, there's enough raw material for a SemiAnalysis-quality report. The gap is not data availability — it's analytical judgment applied to the data.

---

## 6. Challenges for Automation

### Challenge 1: Source Access and Freshness
- **Problem:** The agent needs current data, not training cutoff data
- **Solution:** Use `/browse` to fetch SEC filings, earnings transcripts, and company IR pages in real-time. Build a source collection step into the SKILL that fetches primary sources before analysis begins.

### Challenge 2: Information Density Enforcement
- **Problem:** LLMs default to verbose, hedge-filled writing
- **Solution:** The SKILL must include explicit density constraints: "Every sentence must contain at least one specific data point, name, number, or verifiable claim. Remove any sentence that could be described as 'filler' or 'context-setting.'"

### Challenge 3: Evidence Chain Integrity
- **Problem:** LLMs hallucinate citations
- **Solution:** Two-phase approach: (1) Collect and verify sources first, (2) Write analysis referencing only collected sources. Never generate a citation — only use URLs and data points from the source collection phase.

### Challenge 4: Analytical Judgment
- **Problem:** Knowing what matters vs. what's noise requires domain expertise
- **Solution:** Encode the analytical framework (Section 4 above) into the SKILL. Specify which dimensions to analyze, which comparisons to make, and which metrics to prioritize.

### Challenge 5: Taking Positions
- **Problem:** AI defaults to diplomatic, both-sides analysis
- **Solution:** The SKILL must explicitly instruct: "After presenting evidence, state your conclusion clearly. Use 'we believe' to flag inference, but DO take a position. If the evidence supports a conclusion, state it directly. Do not hedge with 'however, there are also arguments to the contrary' unless you then explain why those arguments are wrong."

### Challenge 6: Visual Elements
- **Problem:** Text-only output lacks the charts and diagrams that make SemiAnalysis reports visually authoritative
- **Solution:** Generate structured data tables in markdown. For the website, use a charting library (e.g., Chart.js, Recharts) to render data as interactive visualizations. The SKILL should output both prose and structured data for charts.

---

## 7. Quality Checklist for Report Evaluation

Use this checklist to evaluate whether a generated report meets the gold standard:

### Information Density
- [ ] Every paragraph contains at least one specific number, date, or verifiable fact
- [ ] No paragraph exists solely to "set context" or "provide background"
- [ ] Removing any sentence would lose information

### Evidence Chain
- [ ] Every quantitative claim links to a specific source (filing, transcript, database)
- [ ] No citation is fabricated or refers to a non-existent source
- [ ] Source types are diverse (not all from one filing or one article)
- [ ] The distinction between fact and inference is explicit ("we believe" vs. stated fact)

### Analytical Depth
- [ ] The report contains at least 3 insights not available in a simple Google search
- [ ] Competitive comparisons use specific metrics, not vague characterizations
- [ ] Forward-looking claims are supported by quantitative modeling, not speculation
- [ ] The report takes clear positions and defends them

### Writing Quality
- [ ] No hedge-phrases: "it's important to consider," "going forward," "significant"
- [ ] Sentences vary in length and structure
- [ ] Technical terms are used precisely (not as jargon decoration)
- [ ] The tone is confident, direct, and slightly informal — like a knowledgeable insider talking

### Structure
- [ ] Opens with a bold, specific claim (not a generic overview)
- [ ] Each section builds toward a conclusion
- [ ] Data visualizations appear immediately after the claims they support
- [ ] The report could be read out of order (each section is self-contained enough)

### Trustworthiness
- [ ] An investor would forward this to a colleague
- [ ] A domain expert would not find obvious errors
- [ ] The report tells the reader something they didn't already know
- [ ] The evidence chain is strong enough that a skeptic could verify key claims

---

## 8. Recommended Report Structure for PDD Holdings

Based on this analysis, the PDD Holdings deep dive should follow this structure:

1. **Opening Thesis** (1 paragraph): Bold claim about PDD's position. Not "PDD is a large e-commerce company" — something like "PDD is running two fundamentally different businesses under one corporate structure, and the market is pricing them as one."

2. **The Numbers That Matter** (data-dense overview): Key financial metrics, growth trajectory, cash position, valuation vs. peers — all in one dense section with comparison tables.

3. **Pinduoduo Domestic** (deep dive): Social commerce model, C2M, agricultural focus, competitive position vs. Alibaba/JD, regulatory landscape. Focus on what's non-obvious.

4. **Temu International** (deep dive): Full-managed model economics, geographic expansion (Europe >40% GMV), US tariff impact and adaptation, de minimis elimination implications, logistics network evolution.

5. **The Evidence** (quantitative analysis): Unit economics modeling, GMV growth projections, margin trajectory, geographic mix shift analysis. Show the models.

6. **Regulatory Risk Map** (specific and dated): EU FSR investigation (Dec 2025 raid), US de minimis changes, SAMR actions — with specific timelines and quantified impact.

7. **Competitive Positioning** (head-to-head): PDD vs. Alibaba vs. JD (domestic), Temu vs. Shein vs. Amazon (international) — specific metrics, not vague comparisons.

8. **What the Market Is Missing** (the insight section): 2-3 non-consensus views, supported by evidence from the report.

9. **Evidence Appendix**: Full list of sources with URLs, access dates, and brief descriptions.

---

## Sources

- [SemiAnalysis TPUv7 Report](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the)
- [SemiAnalysis - Dylan Patel profile](https://semianalysis.com/dylan-patel/)
- [Dylan Patel and SemiAnalysis: Decoding the Semiconductor Revolution](https://eutechfuture.com/tech-thought-leaders/dylan-patel-and-semianalysis-decoding-the-semiconductor-revolution/)
- [CFA Institute - Equity Research Report Essentials](https://www.cfainstitute.org/sites/default/files/-/media/documents/support/research-challenge/challenge/rc-equity-research-report-essentials.pdf)
- [Wall Street Prep - Equity Research Report Format](https://www.wallstreetprep.com/knowledge/sample-equity-research-report/)
- [ARK Invest - Investment Process](https://www.ark-invest.com/investment-process)
- [ARK Invest - Open Source Models (GitHub)](https://github.com/ARKInvest)
- [PDD Holdings - Investor Relations](https://investor.pddholdings.com/)
- [PDD Holdings - SEC Filings](https://investor.pddholdings.com/financial-information/sec-filings)
- [PDD 20-F (FY2024)](https://www.sec.gov/Archives/edgar/data/1737806/000141057825000951/pdd-20241231x20f.htm)
- [Harvard Business School - AI Financial Advice Study](https://www.library.hbs.edu/working-knowledge/ai-can-churn-out-financial-advice-but-does-it-help-investors)
- [Bulletin of Atomic Scientists - AI in Scholarly Publishing](https://thebulletin.org/premium/2026-03/how-ai-use-in-scholarly-publishing-threatens-research-integrity-lessens-trust-and-invites-misinformation/)
- [CMBIGM - PDD Holdings Research](https://hk-official.cmbi.info/upload/c7cf65b8-a7e1-43e4-9e4d-d116b85b5925.pdf)
- [DBS - PDD Holdings Analysis](https://www.dbs.com/content/article/pdf/AXJ_Equities/PDD_US.pdf)
- [Rohan's Bytes - SemiAnalysis on Google TPU vs Nvidia GPU](https://www.rohan-paul.com/p/semianalysis-on-google-tpu-vs-nvidia)

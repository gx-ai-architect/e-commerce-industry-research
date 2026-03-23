# E-Commerce Industry Research

A deep-research agent/tool that writes Claude SKILLs to produce top institutional-level deep research reports. It also maintains a website that publishes these deep-research reports for public reading.

## Research Pipeline

The full pipeline has 3 stages: **Mine** → **Write** → **Publish**.

```
STAGE 1: MINE DATA (/meta-miner)                         ~1-2 hours
══════════════════════════════════
User invokes: /meta-miner for <Company> or <Industry Topic>
│
├── skills/meta-miner/SKILL.md        Parse inputs, setup
│   │
│   ├── CRITICAL: Main session IS the Leader (never spawn a leader agent)
│   │   Read .claude/agents/meta-miner-leader.md for protocol instructions
│   │
│   ├── COMPANY MODE: /meta-miner for PDD Holdings (PDD, CIK 0001737806)
│   │   ├── TRIAGE: WebSearch company, identify segments, set Agent 8 mission
│   │   ├── LAUNCH (all 8 agents in parallel as teammates):
│   │   │   ├── Agent 1: Business Model    → sec-edgar scripts + WebSearch
│   │   │   ├── Agent 2: GMV Estimator     → customs/parcel scripts + WebSearch
│   │   │   ├── Agent 3: Price Intel       → /browse platforms + WebSearch
│   │   │   ├── Agent 4: Customer Happy    → heimao + qimai scripts + /browse + WebSearch
│   │   │   ├── Agent 5: Investment        → sec-edgar + ad-intel scripts + WebSearch
│   │   │   ├── Agent 6: Logistics         → parcel/freight/customs scripts + WebSearch
│   │   │   ├── Agent 7: Regulatory        → eu-regulatory + customs scripts + WebSearch
│   │   │   └── Agent 8: Company-Specific  → mission from triage + WebSearch
│   │   ├── VALIDATE: Read every packet, check exit criteria, send back (up to 2x)
│   │   └── CONVERGE: Run bridge, produce coverage matrix
│   │
│   └── INDUSTRY MODE: /meta-miner for Chinese E-Commerce Industry
│       ├── QUESTION FORMATION: WebSearch topic, formulate 3-5 questions
│       ├── INITIAL COLLECTION: Spawn 3-5 thesis agents (one per question)
│       ├── EVIDENCE COURT: Read packets, evaluate if questions are answered
│       ├── TARGETED FOLLOW-UP: Re-dispatch agents for gaps (up to 3 rounds)
│       └── SYNTHESIS: Run bridge, write research board, produce coverage matrix
│
├── Agents write evidence packets ─────→ reports/$SLUG/evidence-packets/*.json
│   (schema: skills/evidence-store/schema.json)
│
└── Bridge script ─────────────────────→ reports/$SLUG/evidence-auto.json
    (scripts/bridge/packets_to_evidence.py)


STAGE 2: WRITE REPORT (/deep-research)                   ~30-60 min
═══════════════════════════════════════
User invokes: /deep-research for <Company>
│
├── skills/deep-research/SKILL.md
│   │
│   ├── Phase 1-4: Source collection (USES evidence-auto.json from Stage 1)
│   │   ├── Read evidence-packets/ from meta-miner
│   │   ├── Supplement with /browse (IR pages, news, live data)
│   │   └── Save checkpoints → reports/$COMPANY/sources/phase{1-4}-*.md
│   │
│   ├── Phase 4.5: Mosaic Analysis
│   │   ├── Cross-reference data from all phases
│   │   ├── Build 2-3 mosaic insights (3-7 data points → 1 non-obvious conclusion)
│   │   ├── Derive 3-5 falsifiable predictions
│   │   └── Save → reports/$COMPANY/sources/mosaic-analysis.md
│   │
│   └── Phase 5: Report Generation
│       ├── Read all checkpoints + reference docs
│       ├── Generate evidence.json (merge auto + manual entries)
│       ├── Generate charts.json
│       ├── Write report.md (institutional quality, evidence-linked)
│       └── Quality check against docs/reference-standard-analysis.md
│
├── Phase 5.5: Evidence Audit (.claude/agents/evidence-auditor.md)
│   ├── For EVERY [E_] citation: verify evidence supports the claim
│   ├── Verdicts: SUPPORTED / OVERCLAIMED / UNSUPPORTED / MISSING
│   ├── Tighten overclaims to match evidence (add time periods, sources)
│   ├── Add source notes to every table
│   ├── Flag uncited quantitative claims
│   ├── Output: evidence-audit-v{N}.md (audit report)
│   ├── Output: report-v{N}-audited.md (corrected report)
│   └── Output: evidence-v{N}-audited.json (corrected evidence)
│
├── Output:
│   ├── reports/$COMPANY/report-v{N}.md          The report (raw)
│   ├── reports/$COMPANY/report-v{N}-audited.md  The report (fact-checked)
│   ├── reports/$COMPANY/evidence-v{N}.json      Citations (raw)
│   ├── reports/$COMPANY/evidence-v{N}-audited.json  Citations (verified)
│   ├── reports/$COMPANY/evidence-audit-v{N}.md  Audit findings
│   ├── reports/$COMPANY/charts-v{N}.json        Chart data
│   └── reports/$COMPANY/sources/                Phase checkpoints


STAGE 3: PUBLISH TO SITE (manual)                        ~10 min
═════════════════════════════════
│
├── Create page: site/src/pages/reports/$COMPANY-v{N}/index.astro
│   ├── Reads report-v{N}.md, evidence-v{N}.json, charts-v{N}.json
│   ├── Renders markdown → HTML with chart injection (<!-- CHART:id -->)
│   ├── Charts: LineChart.astro + BarChart.astro (pure SVG, build-time)
│   └── Evidence sidebar: green = auto-collected, blue = manual
│
├── Build: npx astro build
│
└── Deploy: (hosting platform)
```

### Tool & Script Inventory

```
scripts/tools/                         P0 agent tools (new)
├── heimao-scraper.py                  黑猫投诉 consumer complaints
├── qimai-appdata.py                   七麦数据 app intelligence (via iTunes API)
└── cn-express-earnings.py             ZTO/YTO/Yunda parcel volumes (via SEC EDGAR)

skills/data-mining/*/scripts/          Existing scripts (used by agents as tools)
├── sec-edgar/   (3 scripts)           Financial data, XBRL, earnings
├── customs-data/ (2 scripts)          CBP stats, tariff rates
├── parcel-volume/ (3 scripts)         Carrier volumes, ShipMatrix, Pitney Bowes
├── air-freight/ (2 scripts)           TAC index, IATA stats
├── consumer-complaints/ (2 scripts)   CPSC, RAPEX
├── app-intel/ (2 scripts)             App Store, Play Store
├── ad-intelligence/ (2 scripts)       Meta ads, Google ads
├── eu-regulatory/ (4 scripts)         Eurostat, RAPEX, EUR-Lex, EC press
└── ...8 more categories               sentiment, web-traffic, google-trends, etc.

scripts/bridge/packets_to_evidence.py  Converts evidence packets → evidence.json
scripts/orchestrate.sh                 DEPRECATED — use /meta-miner instead
```

## gstack

Use the `/browse` skill from gstack for all web browsing. Never use `mcp__claude-in-chrome__*` tools.

Available gstack skills:
- `/office-hours`
- `/plan-ceo-review`
- `/plan-eng-review`
- `/plan-design-review`
- `/design-consultation`
- `/review`
- `/ship`
- `/browse`
- `/qa`
- `/qa-only`
- `/design-review`
- `/setup-browser-cookies`
- `/retro`
- `/debug`
- `/document-release`
- `/gstack-upgrade`

If gstack skills aren't working, run `cd .claude/skills/gstack && ./setup` to build the binary and register skills.

## Key Files

- `skills/meta-miner/SKILL.md` — Stage 1 entry point
- `skills/meta-miner/DESIGN.md` — Agent domain knowledge, research findings, architecture rationale
- `skills/deep-research/SKILL.md` — Stage 2 entry point
- `.claude/agents/` — 10 agent definitions (1 leader + 8 task agents + 1 evidence auditor)
- `skills/evidence-store/schema.json` — Evidence packet JSON schema
- `docs/reference-standard-analysis.md` — Report writing quality standards

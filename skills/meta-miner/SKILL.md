# Meta-Miner: Agent-Based Data Mining

An agent team that produces institutional-quality primary source data for e-commerce research. Supports two modes:

- **Company mode:** 8 domain-expert agents deep-dive a single company
- **Industry mode:** Question-driven research with thesis-organized agents that iterate until evidence is sufficient

## Prerequisites

- Claude Code with `/browse` skill (gstack)
- Internet access for WebSearch and tool scripts
- Python 3.10+ for tool scripts

## How to Run

### Company Mode (single company deep-dive)
```
Run the /meta-miner skill for PDD Holdings (PDD, CIK 0001737806)
```
Or for any company:
```
Run /meta-miner for <Company Name> (<TICKER>, CIK <CIK_NUMBER>)
```

### Industry Mode (cross-company thematic research)
```
Run /meta-miner for Chinese E-Commerce Industry
```
Or for any industry topic:
```
Run /meta-miner for <Topic Name>
```

## Mode Detection

- **Company mode:** Invocation includes a stock ticker and/or CIK number
- **Industry mode:** Invocation has no ticker/CIK — just a topic name

## Execution Protocol

### Step 1: Parse Inputs

**Company mode:**
- `COMPANY` — slug form (e.g., `pdd-holdings`)
- `TICKER` — stock ticker (e.g., `PDD`)
- `CIK` — SEC CIK number (e.g., `0001737806`)
- `MODE` = `company`

**Industry mode:**
- `TOPIC` — slug form (e.g., `china-ecommerce-industry`)
- `MODE` = `industry`

### Step 2: Setup

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)

# Company mode
if [ "$MODE" = "company" ]; then
  OUTDIR="$REPO_ROOT/reports/$COMPANY/evidence-packets"
else
  OUTDIR="$REPO_ROOT/reports/$TOPIC/evidence-packets"
fi

mkdir -p "$OUTDIR"
```

### Step 3: Create Team and Spawn Leader

Use TeamCreate to create a team named `meta-miner-$SLUG` (where SLUG is the company or topic slug).

Then spawn the Leader agent (`.claude/agents/meta-miner-leader.md`) with this message:

**Company mode:**
```
You are the Meta-Miner Leader for researching:
- Mode: company
- Company: $COMPANY_NAME
- Ticker: $TICKER
- CIK: $CIK
- Output directory: $OUTDIR
- Repo root: $REPO_ROOT

Execute your COMPANY MODE protocol: TRIAGE -> LAUNCH -> VALIDATE -> CONVERGE.
```

**Industry mode:**
```
You are the Meta-Miner Leader for researching:
- Mode: industry
- Topic: $TOPIC_NAME
- Output directory: $OUTDIR
- Repo root: $REPO_ROOT

Execute your INDUSTRY MODE protocol:
QUESTION FORMATION -> INITIAL COLLECTION -> EVIDENCE COURT -> TARGETED FOLLOW-UP (up to 3 rounds) -> SYNTHESIS.

Remember: formulate genuine QUESTIONS, not claims. Evaluate evidence INTELLECTUALLY — does it answer the question? — not just structurally. Iterate until you have real answers or have honestly determined a question is unanswerable.
```

### Step 4: Monitor

The Leader agent handles all coordination. Wait for it to complete, then report results to the user.

### Step 5: Bridge

After all agents complete, the Leader runs:
```bash
python3 $REPO_ROOT/scripts/bridge/packets_to_evidence.py \
  --packets-dir $OUTDIR \
  --output $REPO_ROOT/reports/$SLUG/evidence-auto.json
```

## Agent Teams

### Company Mode (8 domain experts)

| # | Agent | Definition | Domain |
|---|-------|-----------|--------|
| 0 | Leader | `.claude/agents/meta-miner-leader.md` | Coordination, quality gate |
| 1 | Business Model | `.claude/agents/business-model-analyst.md` | Revenue decomposition, take rates |
| 2 | GMV Estimator | `.claude/agents/gmv-scale-estimator.md` | GMV triangulation, scale metrics |
| 3 | Price Intelligence | `.claude/agents/price-intelligence.md` | Platform price comparison |
| 4 | Customer Happiness | `.claude/agents/customer-happiness.md` | Multi-source satisfaction data |
| 5 | Investment Tracker | `.claude/agents/investment-growth-tracker.md` | Capex, hiring, new businesses |
| 6 | Logistics | `.claude/agents/logistics-fulfillment.md` | Parcel volumes, warehouses |
| 7 | Regulatory | `.claude/agents/regulatory-policy-reader.md` | Legal actions, tariffs, policy |
| 8 | Company-Specific | `.claude/agents/company-specific.md` | Leader decides mission |

### Industry Mode (3-5 thesis agents)

| # | Agent | Definition | Domain |
|---|-------|-----------|--------|
| 0 | Leader | `.claude/agents/meta-miner-leader.md` | Question formation, evidence court, iteration |
| 1-5 | Thesis Agents | `.claude/agents/thesis-agent.md` | One agent per research question, cross-company |

In industry mode, the Leader dynamically creates each agent's mission during Phase 0 (Question Formation). The thesis-agent.md template provides the evidence standards and tool inventory; the Leader fills in the specific question, evidence requirements, and companies to investigate.

## Output

### Company Mode
```
reports/$COMPANY/
├── evidence-packets/          # Raw JSON packets from all agents
│   ├── business-model-*.json
│   ├── gmv-*.json
│   └── ...
└── evidence-auto.json         # Bridged evidence for report generation
```

### Industry Mode
```
reports/$TOPIC/
├── evidence-packets/          # Raw JSON packets from thesis agents
│   ├── Q1-merchant-profitability-*.json
│   ├── Q2-food-delivery-*.json
│   └── ...
├── research-board.md          # Questions, verdicts, evidence inventory, handoff notes
└── evidence-auto.json         # Bridged evidence for report generation
```

## Design Doc

See `skills/meta-miner/DESIGN.md` for architecture rationale, agent domain knowledge, and research findings.

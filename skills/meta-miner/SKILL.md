# Meta-Miner: Agent-Based Data Mining

An agent team that produces institutional-quality primary source data for e-commerce company research. Replaces the sequential `orchestrate.sh` with 8 mission-driven domain experts coordinated by a Leader agent.

## Prerequisites

- Claude Code with `/browse` skill (gstack)
- Internet access for WebSearch and tool scripts
- Python 3.10+ for tool scripts

## How to Run

```
Run the /meta-miner skill for PDD Holdings (PDD, CIK 0001737806)
```

Or for any company:
```
Run /meta-miner for <Company Name> (<TICKER>, CIK <CIK_NUMBER>)
```

## What It Does

1. Parses company inputs (name, ticker, CIK)
2. Creates the evidence-packets output directory
3. Creates a team of 8 domain-expert agents + 1 Leader
4. Leader triages the company, launches agents in batches, validates output
5. Each agent runs tool scripts + WebSearch + /browse to collect primary source data
6. All agents write evidence packets to `reports/$COMPANY/evidence-packets/`
7. Bridge script converts packets to `evidence-auto.json`

## Execution Protocol

### Step 1: Parse Inputs

Extract from the user's invocation:
- `COMPANY` — slug form (e.g., `pdd-holdings`)
- `TICKER` — stock ticker (e.g., `PDD`)
- `CIK` — SEC CIK number (e.g., `0001737806`)

### Step 2: Setup

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
OUTDIR="$REPO_ROOT/reports/$COMPANY/evidence-packets"
mkdir -p "$OUTDIR"
```

### Step 3: Create Team and Spawn Leader

Use TeamCreate to create a team named `meta-miner-$COMPANY`.

Then spawn the Leader agent (`.claude/agents/meta-miner-leader.md`) with this message:

```
You are the Meta-Miner Leader for researching:
- Company: $COMPANY_NAME
- Ticker: $TICKER
- CIK: $CIK
- Output directory: $OUTDIR
- Repo root: $REPO_ROOT

Execute your full protocol: TRIAGE -> LAUNCH -> VALIDATE -> CONVERGE.
```

### Step 4: Monitor

The Leader agent handles all coordination. Wait for it to complete, then report results to the user.

### Step 5: Bridge

After all agents complete, the Leader runs:
```bash
python3 $REPO_ROOT/scripts/bridge/packets_to_evidence.py \
  --packets-dir $OUTDIR \
  --output $REPO_ROOT/reports/$COMPANY/evidence-auto.json
```

## Agent Team

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

## Output

```
reports/$COMPANY/
├── evidence-packets/          # Raw JSON packets from all agents
│   ├── business-model-*.json
│   ├── gmv-*.json
│   ├── price-*.json
│   └── ...
└── evidence-auto.json         # Bridged evidence for report generation
```

## Design Doc

See `skills/meta-miner/DESIGN.md` for architecture rationale, agent domain knowledge, and research findings.

# Meta-Miner: Agent-Based Data Mining

An agent team that produces institutional-quality primary source data for e-commerce research. Supports two modes:

- **Company mode:** 8 domain-expert agents deep-dive a single company
- **Industry mode:** Question-driven research with thesis-organized agents that iterate until evidence is sufficient

## CRITICAL: YOU (the main session) ARE THE LEADER

**DO NOT spawn a separate "leader" agent.** You — the main Claude Code session running this skill — act as the Leader. You directly:
- Formulate research questions (industry mode) or run triage (company mode)
- Spawn research agents as teammates using the Agent tool
- Read their evidence packets from disk when they complete
- Evaluate evidence quality yourself
- Send agents back with targeted follow-up
- Write the research board and run the bridge

The `.claude/agents/meta-miner-leader.md` file contains your instructions for HOW to lead. Read it and follow its protocol — but execute it yourself, do not delegate leadership to a sub-agent.

**Why:** Sub-agents that are told to spawn their own sub-agents take shortcuts. They skip the multi-agent loop and do all the research themselves in a single pass. The main session must be the orchestrator to ensure agents are actually spawned, evidence is actually evaluated, and iteration actually happens.

## Prerequisites

- Claude Code with `/browse` skill (gstack)
- Internet access for WebSearch and tool scripts
- Python 3.10+ for tool scripts

## How to Run

### Company Mode (single company deep-dive)
```
Run the /meta-miner skill for PDD Holdings (PDD, CIK 0001737806)
```

### Industry Mode (cross-company thematic research)
```
Run /meta-miner for Chinese E-Commerce Industry
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

if [ "$MODE" = "company" ]; then
  OUTDIR="$REPO_ROOT/reports/$COMPANY/evidence-packets"
else
  OUTDIR="$REPO_ROOT/reports/$TOPIC/evidence-packets"
fi

mkdir -p "$OUTDIR"
```

### Step 3: Read Your Instructions

Read `.claude/agents/meta-miner-leader.md` — this contains your full protocol for both company and industry modes. Follow it step by step.

### Step 4: Execute the Protocol YOURSELF

**Industry mode — you do each phase:**

1. **Phase 0 (Question Formation):** YOU research the topic via WebSearch, formulate 3-5 questions, write the research board to disk.

2. **Phase 1 (Initial Collection):** YOU create a team with TeamCreate, then spawn 3-5 thesis agents using the Agent tool (one per question, `subagent_type: "thesis-agent"`). Each agent runs in parallel. Wait for all to complete.

3. **Phase 2 (Evidence Court):** YOU read every evidence packet the agents wrote to disk. YOU evaluate whether the evidence answers each question. YOU update the research board with verdicts and follow-up questions.

4. **Phase 3 (Targeted Follow-up):** YOU re-dispatch agents via SendMessage with specific follow-up instructions. Wait for completion.

5. **Repeat Phases 2-3** up to 3 rounds total.

6. **Phase 4 (Synthesis):** YOU run the bridge script, write final research board, produce coverage matrix.

**Company mode — you do each phase:**

1. **Phase A (Triage):** YOU WebSearch the company, identify segments, decide Agent 8's mission.

2. **Phase B (Launch):** YOU create a team with TeamCreate, spawn all 8 domain agents using the Agent tool. Each runs in parallel.

3. **Phase C (Validate):** YOU read every evidence packet from disk. YOU score each agent's output. YOU send agents back via SendMessage if output is THIN.

4. **Phase D (Converge):** YOU run the bridge script, produce coverage matrix.

### Step 5: Verify Your Own Work

Before reporting results to the user, confirm:
- [ ] Research agents were actually spawned (not just you doing the research)
- [ ] Evidence packets on disk show different agent names (not all "meta-miner-leader")
- [ ] At least one round of Evidence Court evaluation was performed (industry mode)
- [ ] Research board has verdicts per question (industry mode)

## Agent Definitions

### Company Mode (8 domain experts)

| # | Agent | Definition | Domain |
|---|-------|-----------|--------|
| 1 | Business Model | `.claude/agents/business-model-analyst.md` | Revenue decomposition, take rates |
| 2 | GMV Estimator | `.claude/agents/gmv-scale-estimator.md` | GMV triangulation, scale metrics |
| 3 | Price Intelligence | `.claude/agents/price-intelligence.md` | Platform price comparison |
| 4 | Customer Happiness | `.claude/agents/customer-happiness.md` | Multi-source satisfaction data |
| 5 | Investment Tracker | `.claude/agents/investment-growth-tracker.md` | Capex, hiring, new businesses |
| 6 | Logistics | `.claude/agents/logistics-fulfillment.md` | Parcel volumes, warehouses |
| 7 | Regulatory | `.claude/agents/regulatory-policy-reader.md` | Legal actions, tariffs, policy |
| 8 | Company-Specific | `.claude/agents/company-specific.md` | You decide mission during triage |

### Industry Mode (3-5 thesis agents)

| # | Agent | Definition | Domain |
|---|-------|-----------|--------|
| 1-5 | Thesis Agents | `.claude/agents/thesis-agent.md` | One agent per research question, cross-company |

In industry mode, you dynamically create each agent's mission during Phase 0 (Question Formation). The thesis-agent.md template provides evidence standards and tool inventory; you fill in the specific question, evidence requirements, and companies to investigate.

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

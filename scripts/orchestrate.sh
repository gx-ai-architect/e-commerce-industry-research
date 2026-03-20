#!/bin/bash
# DEPRECATED: Use /meta-miner skill instead (skills/meta-miner/SKILL.md).
# meta-miner replaces this sequential script runner with 8 mission-driven
# domain-expert agents that produce higher quality, more comprehensive data.
# This script is kept for backwards compatibility but is no longer maintained.
#
# Orchestrate data mining skills for a company research report.
# Runs all READY skills, saves evidence packets, then bridges to evidence.json.
#
# Usage: ./scripts/orchestrate.sh <company-slug> <ticker> <cik> [--phase N]
# Example: ./scripts/orchestrate.sh pdd-holdings PDD 0001737806
# Example: ./scripts/orchestrate.sh pdd-holdings PDD 0001737806 --phase 2

set -eo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills/data-mining"
BRIDGE="$REPO_ROOT/scripts/bridge/packets_to_evidence.py"

# --- Parse arguments ---
if [ $# -lt 3 ]; then
    echo "Usage: $0 <company-slug> <ticker> <cik> [--phase N]" >&2
    echo "Example: $0 pdd-holdings PDD 0001737806" >&2
    exit 1
fi

COMPANY="$1"
TICKER="$2"
CIK="$3"
PHASE_FILTER=""

shift 3
while [ $# -gt 0 ]; do
    case "$1" in
        --phase) PHASE_FILTER="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

OUTDIR="$REPO_ROOT/reports/$COMPANY/evidence-packets"
ERRLOG="$OUTDIR/errors.log"
mkdir -p "$OUTDIR"
: > "$ERRLOG"  # Clear error log

SUCCESS=0
FAIL=0

# --- Runner: execute a script and save output as evidence packet ---
run_skill() {
    local skill_name="$1"
    local script_name="$2"
    shift 2
    local script_path="$SKILLS_DIR/$skill_name/scripts/$script_name"
    local out_file="$OUTDIR/${skill_name}-${script_name%.*}.json"

    if [ ! -f "$script_path" ]; then
        echo "  SKIP: $script_path not found" >&2
        echo "[SKIP] $skill_name/$script_name — file not found" >> "$ERRLOG"
        FAIL=$((FAIL + 1))
        return 0
    fi

    echo "  Running $skill_name/$script_name $*..."

    local max_attempts=3
    local attempt=1
    local exit_code=0

    while [ $attempt -le $max_attempts ]; do
        exit_code=0
        if [[ "$script_name" == *.sh ]]; then
            bash "$script_path" "$@" > "$out_file" 2>> "$ERRLOG" || exit_code=$?
        elif [[ "$script_name" == *.py ]]; then
            python3 "$script_path" "$@" > "$out_file" 2>> "$ERRLOG" || exit_code=$?
        fi

        if [ $exit_code -eq 0 ] && [ -s "$out_file" ]; then
            break
        fi

        # Only retry on transient failures (exit code > 2 or empty output with success)
        # Exit code 1 = script error, 2 = argparse — both deterministic, don't retry
        if [ $exit_code -le 2 ] && [ $exit_code -ne 0 ]; then
            echo "  SKIP RETRY: deterministic failure (exit $exit_code)" >&2
            break
        fi

        if [ $attempt -lt $max_attempts ]; then
            echo "  RETRY ($attempt/$max_attempts): $skill_name/$script_name" >&2
            sleep 3
        fi
        attempt=$((attempt + 1))
    done

    if [ $exit_code -ne 0 ]; then
        echo "  FAIL: $skill_name/$script_name (exit $exit_code, $((attempt-1)) attempts)" >&2
        echo "[FAIL] $skill_name/$script_name — exit code $exit_code after $((attempt-1)) attempts" >> "$ERRLOG"
        rm -f "$out_file"
        FAIL=$((FAIL + 1))
    elif [ ! -s "$out_file" ]; then
        echo "  WARN: $skill_name/$script_name produced empty output ($((attempt-1)) attempts)" >&2
        echo "[EMPTY] $skill_name/$script_name — no output after $((attempt-1)) attempts" >> "$ERRLOG"
        rm -f "$out_file"
        FAIL=$((FAIL + 1))
    else
        echo "  OK: $out_file"
        SUCCESS=$((SUCCESS + 1))
    fi
}

# --- Phase 1: Financial Data (SEC EDGAR) ---
run_phase_1() {
    echo "=== Phase 1: Financial Data ==="
    run_skill sec-edgar fetch-filings.sh "$CIK"
    # Pipe fetch output into XBRL extractor if fetch succeeded
    local filings_out="$OUTDIR/sec-edgar-fetch-filings.json"
    if [ -f "$filings_out" ] && [ -s "$filings_out" ]; then
        echo "  Running sec-edgar/extract-xbrl.py from fetched filings..."
        python3 "$SKILLS_DIR/sec-edgar/scripts/extract-xbrl.py" \
            --cik "$CIK" --ticker "$TICKER" --input "$filings_out" \
            > "$OUTDIR/sec-edgar-xbrl-extract.json" 2>> "$ERRLOG" \
            && { echo "  OK: sec-edgar-xbrl-extract.json"; SUCCESS=$((SUCCESS + 1)); } \
            || { echo "  FAIL: extract-xbrl.py" >&2; echo "[FAIL] sec-edgar/extract-xbrl.py" >> "$ERRLOG"; FAIL=$((FAIL + 1)); }
    fi
    run_skill sec-edgar parse-earnings.py --cik "$CIK" --ticker "$TICKER"
}

# --- Phase 2: Alternative & Real-Time Data ---
run_phase_2() {
    echo "=== Phase 2: Alternative & Real-Time Data ==="
    # Parcel volume
    run_skill parcel-volume fetch-carrier-volumes.py --carrier all
    run_skill parcel-volume fetch-shipmatrix.py
    run_skill parcel-volume fetch-pitney-bowes.py

    # Customs data
    run_skill customs-data fetch-cbp-stats.py
    run_skill customs-data fetch-tariff-rates.py

    # Air freight
    run_skill air-freight fetch-tac-index.py --route all
    run_skill air-freight fetch-iata-stats.py

    # Freight rates
    run_skill freight-rates fetch-freight-index.py

    # App intel
    run_skill app-intel scrape-appstore.py --app-name temu
    run_skill app-intel scrape-playstore.py --package-id com.einnovation.temu

    # Web traffic
    run_skill web-traffic fetch-cloudflare-radar.py --domain temu.com

    # Google Trends
    run_skill google-trends fetch-trends.py --terms temu shein aliexpress

    # Sentiment
    run_skill sentiment scrape-trustpilot.py --domain temu.com
    run_skill sentiment scrape-reddit.py --subreddit temu

    # Job postings
    run_skill job-postings fetch-jobs.py --company temu

    # Ad intelligence
    run_skill ad-intelligence fetch-meta-ads.py --advertiser temu
    run_skill ad-intelligence fetch-google-ads.py --advertiser temu

    # Consumer complaints
    run_skill consumer-complaints fetch-cpsc.py --query temu
    run_skill consumer-complaints fetch-rapex.py --query temu
}

# --- Phase 3: China-Specific Data ---
run_phase_3() {
    echo "=== Phase 3: China Data ==="
    run_skill china-regulatory fetch-samr.py --query pinduoduo
    run_skill china-regulatory fetch-ndrc.py --query pinduoduo
}

# --- Phase 4: Competitive & Regulatory ---
run_phase_4() {
    echo "=== Phase 4: Competitive & Regulatory ==="
    run_skill eu-regulatory fetch-ec-press.py --query temu
    run_skill eu-regulatory fetch-rapex.py
    run_skill price-intel compare-prices.py --query "wireless earbuds"
}

# --- Run selected or all phases ---
echo "Orchestrating data mining for $COMPANY ($TICKER, CIK: $CIK)"
echo "Output: $OUTDIR"
echo ""

if [ -z "$PHASE_FILTER" ]; then
    run_phase_1
    run_phase_2
    run_phase_3
    run_phase_4
else
    case "$PHASE_FILTER" in
        1) run_phase_1 ;;
        2) run_phase_2 ;;
        3) run_phase_3 ;;
        4) run_phase_4 ;;
        *) echo "Error: unknown phase $PHASE_FILTER (expected 1-4)" >&2; exit 1 ;;
    esac
fi

# --- Summary ---
echo ""
echo "=== Summary ==="
echo "  Success: $SUCCESS"
echo "  Failed:  $FAIL"
echo "  Packets: $OUTDIR/"

if [ -s "$ERRLOG" ]; then
    echo "  Errors:  $ERRLOG"
fi

# --- Bridge to evidence.json ---
echo ""
echo "=== Bridging to evidence-auto.json ==="
python3 "$BRIDGE" \
    --packets-dir "$OUTDIR" \
    --output "$REPO_ROOT/reports/$COMPANY/evidence-auto.json"

echo "Done."

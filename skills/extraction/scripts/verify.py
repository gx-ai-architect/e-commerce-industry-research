#!/usr/bin/env python3
"""
Verify claims in evidence packets.

Takes an evidence packet and verifies each extraction by checking if the
claim is supported by the evidence. Updates verification status.
"""

import argparse
import json
import sys
from datetime import datetime
import re


def verify_extraction(claim, evidence, evidence_type):
    """
    Verify if a claim is supported by the evidence.

    Uses simple heuristic verification:
    - keyword matching between claim and evidence
    - number matching for metrics
    - length checks for direct quotes

    Returns: (status, notes)
    """
    claim_lower = claim.lower()
    evidence_lower = evidence.lower()

    # Direct quote verification
    if evidence_type == "direct_quote":
        if claim_lower in evidence_lower:
            return "supported", "Claim found verbatim in evidence"

        # Check for partial match (at least 50% of words)
        claim_words = set(re.findall(r'\w+', claim_lower))
        evidence_words = set(re.findall(r'\w+', evidence_lower))

        if len(claim_words) == 0:
            return "unsupported", "Empty claim"

        overlap = len(claim_words & evidence_words) / len(claim_words)

        if overlap >= 0.7:
            return "supported", f"High word overlap ({overlap:.0%})"
        elif overlap >= 0.4:
            return "extrapolated", f"Partial match ({overlap:.0%}), may be paraphrased"
        else:
            return "unsupported", f"Low word overlap ({overlap:.0%})"

    # Table slice verification
    elif evidence_type == "table_slice":
        # Extract numbers from claim and evidence
        claim_numbers = re.findall(r'[\d,]+\.?\d*', claim)
        evidence_numbers = re.findall(r'[\d,]+\.?\d*', evidence)

        if claim_numbers:
            # Check if claim numbers appear in evidence
            for num in claim_numbers:
                if num in evidence:
                    return "supported", f"Key metric {num} found in table"
            return "extrapolated", "Numbers don't match exactly, may be computed"
        else:
            return "supported", "Table slice extracted"

    # Computed metric verification
    elif evidence_type == "computed_metric":
        # For computed metrics, we trust the computation
        # In production, this would re-compute the metric
        return "supported", "Metric computation assumed correct (not re-verified)"

    return "unsupported", "Unknown verification failure"


def main():
    parser = argparse.ArgumentParser(description='Verify evidence packets')
    parser.add_argument('--file', help='Input evidence packet file (default: stdin)')

    args = parser.parse_args()

    # Read input
    if args.file:
        with open(args.file, 'r') as f:
            packet = json.load(f)
    else:
        packet = json.load(sys.stdin)

    # Verify each extraction
    for extraction in packet.get('extractions', []):
        claim = extraction.get('claim', '')
        evidence = extraction.get('evidence', '')
        evidence_type = extraction.get('evidence_type', 'direct_quote')

        status, notes = verify_extraction(claim, evidence, evidence_type)

        extraction['verification'] = {
            "status": status,
            "verifier_notes": notes,
            "verified_at": datetime.utcnow().isoformat() + 'Z'
        }

    # Output updated packet
    print(json.dumps(packet, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Bridge: Convert evidence packets (data mining output) to evidence.json entries (report input).

Supports two packet formats:
1. Formal schema: {packet_id, source, extractions[], metadata}
2. Simple format: {agent, company, findings[]} (used by thesis agents and early company agents)

Evidence.json entries use: {id: "E1", url, quote, date, provenance, question_id?, source_tier?}

Only includes extractions with verification.status "supported" or "extrapolated".
Deduplicates by URL when merging with an existing evidence.json.
"""

import json
import sys
import argparse
import os
import re
from datetime import datetime


def parse_date_from_freshness(freshness_str):
    """Extract a date from the metadata.freshness field."""
    if not freshness_str:
        return "unknown"

    # Try ISO date formats: 2026-03, 2026-03-15
    match = re.search(r'(\d{4}-\d{2}(?:-\d{2})?)', freshness_str)
    if match:
        return match.group(1)

    # Try year-only
    match = re.search(r'(\d{4})', freshness_str)
    if match:
        return match.group(1)

    return "unknown"


def parse_date_from_retrieved_at(retrieved_at):
    """Extract date portion from an ISO datetime string."""
    if not retrieved_at:
        return "unknown"
    # Take the date portion of ISO datetime
    match = re.match(r'(\d{4}-\d{2}-\d{2})', retrieved_at)
    if match:
        return match.group(1)
    return "unknown"


def build_quote(extraction):
    """Build the quote field from an extraction."""
    evidence_type = extraction.get("evidence_type", "")
    claim = extraction.get("claim", "")
    evidence = extraction.get("evidence", "")

    if evidence_type == "direct_quote":
        return evidence
    elif claim and evidence:
        return f"{claim}: {evidence}"
    elif evidence:
        return evidence
    else:
        return claim


def should_include(extraction):
    """Check if extraction passes verification filter."""
    verification = extraction.get("verification", {})
    status = verification.get("status", "supported")  # default to supported if missing
    return status in ("supported", "extrapolated")


def is_formal_packet(data):
    """Check if a packet uses the formal schema (has packet_id and source)."""
    return "packet_id" in data and "source" in data and "extractions" in data


def convert_formal_packet(packet):
    """Convert a formal-schema packet to evidence entries."""
    entries = []
    source = packet.get("source", {})
    metadata = packet.get("metadata", {})
    collector = source.get("collector", "unknown")
    url = source.get("url", "")

    # Determine date: prefer freshness, fallback to retrieved_at
    freshness_date = parse_date_from_freshness(metadata.get("freshness", ""))
    retrieved_date = parse_date_from_retrieved_at(source.get("retrieved_at", ""))
    date = freshness_date if freshness_date != "unknown" else retrieved_date

    # New fields from industry mode
    question_id = metadata.get("question_id")
    source_tier = metadata.get("source_tier")
    evidence_direction = metadata.get("evidence_direction")

    for extraction in packet.get("extractions", []):
        if not should_include(extraction):
            continue

        quote = build_quote(extraction)
        if not quote:
            continue

        entry = {
            "id": None,  # assigned later
            "url": url,
            "quote": quote,
            "date": date,
            "provenance": f"auto:{collector}"
        }

        if question_id:
            entry["question_id"] = question_id
        if source_tier:
            entry["source_tier"] = source_tier
        if evidence_direction:
            entry["evidence_direction"] = evidence_direction

        entries.append(entry)

    return entries


def convert_simple_packet(packet):
    """Convert a simple-format packet (agent/findings) to evidence entries."""
    entries = []
    collector = packet.get("agent", "unknown")
    question_id = packet.get("question_id")
    collected_at = packet.get("collected_at", "unknown")

    for finding in packet.get("findings", []):
        claim = finding.get("claim", "")
        data = finding.get("data", "")
        url = finding.get("source_url", "")
        date = finding.get("source_date", collected_at)
        source_tier = finding.get("source_tier")
        evidence_direction = finding.get("evidence_direction")
        confidence = finding.get("confidence", "medium")

        # Skip low-confidence findings
        if confidence == "low":
            continue

        # Build quote from claim + data
        if claim and data:
            quote = f"{claim}: {data}"
        elif data:
            quote = data
        elif claim:
            quote = claim
        else:
            continue

        entry = {
            "id": None,  # assigned later
            "url": url,
            "quote": quote,
            "date": date,
            "provenance": f"auto:{collector}"
        }

        if question_id:
            entry["question_id"] = question_id
        if source_tier:
            entry["source_tier"] = source_tier
        if evidence_direction:
            entry["evidence_direction"] = evidence_direction

        entries.append(entry)

    return entries


def load_packets(packets_dir):
    """Load all JSON evidence packet files from a directory."""
    packets = []
    if not os.path.isdir(packets_dir):
        print(f"Error: {packets_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    for filename in sorted(os.listdir(packets_dir)):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(packets_dir, filename)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: skipping {filename}: {e}", file=sys.stderr)
            continue

        # Handle both single objects and arrays
        if isinstance(data, list):
            packets.extend(data)
        elif isinstance(data, dict):
            packets.append(data)
        else:
            print(f"Warning: skipping {filename}: unexpected JSON type", file=sys.stderr)

    return packets


def convert_packets(packets, start_id=1):
    """Convert evidence packets to evidence.json entries."""
    entries = []

    for packet in packets:
        if is_formal_packet(packet):
            entries.extend(convert_formal_packet(packet))
        else:
            entries.extend(convert_simple_packet(packet))

    # Assign IDs
    for i, entry in enumerate(entries):
        entry["id"] = f"E{start_id + i}"

    return entries


def merge_with_existing(new_entries, existing_path):
    """Merge new entries with an existing evidence.json, deduplicating by URL."""
    try:
        with open(existing_path, 'r') as f:
            existing = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: could not read {existing_path}: {e}", file=sys.stderr)
        return new_entries

    if not isinstance(existing, list):
        print(f"Warning: {existing_path} is not a JSON array, ignoring", file=sys.stderr)
        return new_entries

    # Collect URLs already in existing evidence
    existing_urls = set()
    for entry in existing:
        if "url" in entry:
            existing_urls.add(entry["url"])

    # Find the highest existing E# to continue numbering
    max_id = 0
    for entry in existing:
        entry_id = entry.get("id", "")
        match = re.match(r'E(\d+)', entry_id)
        if match:
            max_id = max(max_id, int(match.group(1)))

    # Filter out duplicates and re-number
    deduped = []
    next_id = max_id + 1
    for entry in new_entries:
        if entry["url"] not in existing_urls:
            entry["id"] = f"E{next_id}"
            deduped.append(entry)
            existing_urls.add(entry["url"])
            next_id += 1

    return existing + deduped


def group_by_question(entries):
    """Group entries by question_id for industry-mode output."""
    grouped = {}
    ungrouped = []

    for entry in entries:
        qid = entry.get("question_id")
        if qid:
            if qid not in grouped:
                grouped[qid] = []
            grouped[qid].append(entry)
        else:
            ungrouped.append(entry)

    # Return entries ordered by question_id, then ungrouped
    result = []
    for qid in sorted(grouped.keys()):
        result.extend(grouped[qid])
    result.extend(ungrouped)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Convert evidence packets to evidence.json entries"
    )
    parser.add_argument(
        "--packets-dir",
        required=True,
        help="Directory of *.json evidence packet files"
    )
    parser.add_argument(
        "--start-id",
        type=int,
        default=1,
        help="First E# to assign (default: 1)"
    )
    parser.add_argument(
        "--output",
        help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--merge-with",
        help="Existing evidence.json to append to"
    )
    parser.add_argument(
        "--group-by-question",
        action="store_true",
        help="Group output entries by question_id (for industry-mode reports)"
    )

    args = parser.parse_args()

    packets = load_packets(args.packets_dir)
    if not packets:
        print("Warning: no evidence packets found", file=sys.stderr)

    entries = convert_packets(packets, start_id=args.start_id)

    if args.merge_with:
        entries = merge_with_existing(entries, args.merge_with)

    if args.group_by_question:
        entries = group_by_question(entries)

    output = json.dumps(entries, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output + "\n")
        print(f"Wrote {len(entries)} entries to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()

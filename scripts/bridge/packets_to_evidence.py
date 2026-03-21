#!/usr/bin/env python3
"""
Bridge: Convert evidence packets (data mining output) to evidence.json entries (report input).

Evidence packets use the schema: {packet_id, source, extractions[], metadata}
Evidence.json entries use: {id: "E1", url, quote, date, provenance}

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
    current_id = start_id

    for packet in packets:
        source = packet.get("source", {})
        metadata = packet.get("metadata", {})
        collector = source.get("collector", "unknown")
        url = source.get("url", "")

        # Determine date: prefer freshness, fallback to retrieved_at
        freshness_date = parse_date_from_freshness(metadata.get("freshness", ""))
        retrieved_date = parse_date_from_retrieved_at(source.get("retrieved_at", ""))
        date = freshness_date if freshness_date != "unknown" else retrieved_date

        for extraction in packet.get("extractions", []):
            if not should_include(extraction):
                continue

            quote = build_quote(extraction)
            if not quote:
                continue

            entry = {
                "id": f"E{current_id}",
                "url": url,
                "quote": quote,
                "date": date,
                "provenance": f"auto:{collector}"
            }
            entries.append(entry)
            current_id += 1

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

    args = parser.parse_args()

    packets = load_packets(args.packets_dir)
    if not packets:
        print("Warning: no evidence packets found", file=sys.stderr)

    entries = convert_packets(packets, start_id=args.start_id)

    if args.merge_with:
        entries = merge_with_existing(entries, args.merge_with)

    output = json.dumps(entries, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output + "\n")
        print(f"Wrote {len(entries)} entries to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()

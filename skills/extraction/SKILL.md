# SKILL: extraction

Extract structured claims from raw data and verify evidence.

## Purpose

Takes raw data from any collector (filings, articles, datasets, APIs, tables, images) and extracts structured claims with supporting evidence. Uses LLM-based extraction to identify key facts and verify that claims are supported by the evidence.

## Usage

```bash
# Extract claims from a filing
cat raw-10k.txt | /extraction --source-type filing \
  --url "https://sec.gov/..." \
  --title "PDD Holdings 10-K 2024" \
  --collector sec-edgar > packet.json

# Verify an evidence packet
cat packet.json | /extraction-verify > verified-packet.json
```

## Arguments

### Extract mode
- `--source-type`: One of [filing, article, dataset, api, table, image]
- `--url`: Source URL
- `--title`: Source title
- `--collector`: Name of the collecting skill
- Input: Raw data from stdin or `--file <path>`

### Verify mode
- Use `/extraction-verify` subcommand
- Input: Evidence packet JSON from stdin or `--file <path>`

## Output

Evidence packet JSON matching `../evidence-store/schema.json`.

## Implementation

Uses Python scripts:
- `scripts/extract.py`: Extracts claims from raw data
- `scripts/verify.py`: Verifies claims against evidence

## Tests

```bash
./test/test-extract.sh
./test/test-verify.sh
```

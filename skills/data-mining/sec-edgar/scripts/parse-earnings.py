#!/usr/bin/env python3
"""
Parse SEC EDGAR recent filings metadata and output evidence packet.
Fetches filing list for a company and extracts filing dates, types, accession numbers.
"""

import sys
import json
import argparse
from datetime import datetime, timezone
import urllib.request

def fetch_filings(cik):
    """Fetch recent filings from SEC EDGAR submissions API."""
    cik_padded = f"{int(cik):010d}"
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"

    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'E-Commerce-Research research@example.com'}
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def main():
    parser = argparse.ArgumentParser(description='Parse SEC filings metadata to evidence packet')
    parser.add_argument('--cik', required=True, help='Company CIK number')
    parser.add_argument('--ticker', help='Company ticker symbol (optional)')
    parser.add_argument('--limit', type=int, default=10, help='Max filings to include (default: 10)')

    args = parser.parse_args()

    # Fetch filings data
    data = fetch_filings(args.cik)

    # Extract company info
    entity_name = data.get('name', 'Unknown Company')
    ticker = args.ticker or data.get('tickers', ['UNKNOWN'])[0] if data.get('tickers') else 'UNKNOWN'

    # Build evidence packet
    packet = {
        "packet_id": f"PKT-SEC-FILINGS-{ticker}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "source": {
            "type": "api",
            "url": f"https://data.sec.gov/submissions/CIK{int(args.cik):010d}.json",
            "title": f"{entity_name} - SEC EDGAR Recent Filings",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "collector": "sec-edgar"
        },
        "extractions": [],
        "metadata": {
            "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
            "company_tags": [ticker],
            "topic_tags": ["sec-filings", "earnings"]
        }
    }

    # Extract recent filings
    recent_filings = data.get('filings', {}).get('recent', {})

    if not recent_filings:
        print(json.dumps(packet, indent=2))
        return

    # Get filings of interest (10-K, 20-F, 10-Q, 6-K)
    forms = recent_filings.get('form', [])
    filing_dates = recent_filings.get('filingDate', [])
    accession_numbers = recent_filings.get('accessionNumber', [])
    primary_docs = recent_filings.get('primaryDocument', [])

    count = 0
    for i in range(len(forms)):
        if count >= args.limit:
            break

        form = forms[i]
        if form not in ['10-K', '20-F', '10-Q', '6-K']:
            continue

        filing_date = filing_dates[i] if i < len(filing_dates) else 'unknown'
        accession = accession_numbers[i] if i < len(accession_numbers) else 'unknown'
        doc = primary_docs[i] if i < len(primary_docs) else 'unknown'

        # Build filing URL
        accession_clean = accession.replace('-', '')
        filing_url = f"https://www.sec.gov/Archives/edgar/data/{int(args.cik)}/{accession_clean}/{doc}"

        claim = f"Filed {form} on {filing_date} (Accession: {accession})"
        evidence = json.dumps({
            "form": form,
            "filing_date": filing_date,
            "accession_number": accession,
            "document_url": filing_url
        })

        packet['extractions'].append({
            "claim": claim,
            "evidence": evidence,
            "evidence_type": "direct_quote",
            "verification": {
                "status": "supported",
                "verifier_notes": "Extracted from SEC EDGAR submissions API",
                "verified_at": datetime.now(timezone.utc).isoformat()
            }
        })

        count += 1

    # Output JSON
    print(json.dumps(packet, indent=2))

if __name__ == '__main__':
    main()

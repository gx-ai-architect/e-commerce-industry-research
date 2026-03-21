#!/usr/bin/env python3
"""
CPSC SaferProducts.gov scraper - US consumer product safety complaints
Fetches recalls and incident reports from the US Consumer Product Safety Commission
"""

import argparse
import json
import sys
from datetime import datetime
import urllib.request
import urllib.parse
import urllib.error

def fetch_cpsc_recalls(query=None, limit=50):
    """
    Fetch CPSC product recalls
    Free API, no authentication required
    API docs: https://www.cpsc.gov/Recalls/CPSC-Recalls-Application-Program-Interface-API-Information
    """

    base_url = "https://www.saferproducts.gov/RestWebServices/Recall"

    params = ["format=json"]
    if limit:
        params.append(f"limit={limit}")

    url = base_url + "?" + "&".join(params)

    try:
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))

            extractions = []
            recall_count = 0
            query_matched = 0

            # Filter and extract recalls
            if isinstance(data, list):
                for recall in data:
                    recall_count += 1

                    # Apply query filter if specified
                    if query:
                        query_lower = query.lower()
                        description = (recall.get('Description') or '').lower()
                        title = (recall.get('Title') or '').lower()
                        manufacturer = (recall.get('Manufacturer') or '').lower()

                        if not (query_lower in description or query_lower in title or query_lower in manufacturer):
                            continue

                    query_matched += 1

                    # Extract key information
                    title = recall.get('Title', 'Unknown product')
                    hazard = recall.get('Hazard', 'Not specified')
                    description = recall.get('Description', '')
                    manufacturer = recall.get('Manufacturer', 'Unknown')
                    recall_date = recall.get('RecallDate', 'Unknown')

                    extractions.append({
                        "claim": f"CPSC recall: {title}",
                        "evidence": f"Hazard: {hazard} | Manufacturer: {manufacturer} | Date: {recall_date} | {description[:200]}",
                        "evidence_type": "direct_quote"
                    })

            # Summary extraction
            summary_claim = f"CPSC recalls database queried: {query_matched} recalls found"
            if query:
                summary_claim += f" matching '{query}'"

            packet = {
                "packet_id": f"PKT-COMPLAINTS-CPSC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "api",
                    "url": url,
                    "title": f"CPSC Product Recalls{': ' + query if query else ''}",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                    "collector": "consumer-complaints"
                },
                "extractions": extractions + [{
                    "claim": summary_claim,
                    "evidence": f"Total recalls in response: {recall_count}, matched: {query_matched}",
                    "evidence_type": "computed_metric"
                }],
                "metadata": {
                    "freshness": datetime.utcnow().strftime("%Y-%m"),
                    "company_tags": ["CPSC"] if not query else [query.upper()],
                    "topic_tags": ["consumer-safety", "recalls", "regulatory-risk", "cpsc"]
                }
            }

            return packet

    except urllib.error.HTTPError as e:
        error_msg = f"HTTP {e.code}: {e.reason}"
        return create_error_packet(url, query, error_msg)
    except Exception as e:
        return create_error_packet(url, query, str(e))

def fetch_cpsc_incidents(query=None, limit=50):
    """
    Fetch CPSC incident reports
    These are consumer-submitted complaints about product safety issues
    """

    base_url = "https://www.saferproducts.gov/RestWebServices/Incident"

    params = ["format=json"]
    if limit:
        params.append(f"limit={limit}")

    url = base_url + "?" + "&".join(params)

    try:
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))

            extractions = []
            incident_count = 0
            query_matched = 0

            # Filter and extract incidents
            if isinstance(data, list):
                for incident in data:
                    incident_count += 1

                    # Apply query filter if specified
                    if query:
                        query_lower = query.lower()
                        product = (incident.get('Product') or '').lower()
                        manufacturer = (incident.get('Manufacturer') or '').lower()
                        incident_desc = (incident.get('IncidentDescription') or '').lower()

                        if not (query_lower in product or query_lower in manufacturer or query_lower in incident_desc):
                            continue

                    query_matched += 1

                    # Extract key information
                    product = incident.get('Product', 'Unknown product')
                    manufacturer = incident.get('Manufacturer', 'Unknown')
                    incident_desc = incident.get('IncidentDescription', 'No description')
                    incident_date = incident.get('IncidentDate', 'Unknown')

                    extractions.append({
                        "claim": f"CPSC incident report: {product}",
                        "evidence": f"Manufacturer: {manufacturer} | Date: {incident_date} | {incident_desc[:200]}",
                        "evidence_type": "direct_quote"
                    })

            # Summary extraction
            summary_claim = f"CPSC incident database queried: {query_matched} incidents found"
            if query:
                summary_claim += f" matching '{query}'"

            packet = {
                "packet_id": f"PKT-COMPLAINTS-INCIDENTS-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "source": {
                    "type": "api",
                    "url": url,
                    "title": f"CPSC Consumer Incidents{': ' + query if query else ''}",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                    "collector": "consumer-complaints"
                },
                "extractions": extractions + [{
                    "claim": summary_claim,
                    "evidence": f"Total incidents in response: {incident_count}, matched: {query_matched}",
                    "evidence_type": "computed_metric"
                }],
                "metadata": {
                    "freshness": datetime.utcnow().strftime("%Y-%m"),
                    "company_tags": ["CPSC"] if not query else [query.upper()],
                    "topic_tags": ["consumer-safety", "complaints", "incidents", "cpsc"]
                }
            }

            return packet

    except urllib.error.HTTPError as e:
        error_msg = f"HTTP {e.code}: {e.reason}"
        return create_error_packet(url, query, error_msg, "incidents")
    except Exception as e:
        return create_error_packet(url, query, str(e), "incidents")

def create_error_packet(url, query, error_msg, packet_type="recalls"):
    """Create standardized error packet"""
    return {
        "packet_id": f"PKT-COMPLAINTS-ERROR-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "source": {
            "type": "api",
            "url": url,
            "title": f"CPSC {packet_type.title()} Error",
            "retrieved_at": datetime.utcnow().isoformat() + "Z",
            "collector": "consumer-complaints"
        },
        "extractions": [
            {
                "claim": f"CPSC {packet_type} API access failed",
                "evidence": f"Error: {error_msg}",
                "evidence_type": "computed_metric"
            }
        ],
        "metadata": {
            "freshness": datetime.utcnow().strftime("%Y-%m"),
            "company_tags": [query.upper()] if query else [],
            "topic_tags": ["consumer-safety", "error", "cpsc"]
        }
    }

def main():
    parser = argparse.ArgumentParser(description='Fetch CPSC product safety data')
    parser.add_argument('--query', help='Search keyword (e.g., "temu", "made in china")')
    parser.add_argument('--limit', type=int, default=50, help='Maximum number of results to fetch')
    parser.add_argument('--type', choices=['recalls', 'incidents', 'both'], default='recalls',
                        help='Type of data to fetch (default: recalls)')
    args = parser.parse_args()

    if args.type == 'recalls':
        packet = fetch_cpsc_recalls(args.query, args.limit)
        print(json.dumps(packet, indent=2, ensure_ascii=False))
    elif args.type == 'incidents':
        packet = fetch_cpsc_incidents(args.query, args.limit)
        print(json.dumps(packet, indent=2, ensure_ascii=False))
    elif args.type == 'both':
        recalls_packet = fetch_cpsc_recalls(args.query, args.limit)
        incidents_packet = fetch_cpsc_incidents(args.query, args.limit)
        print(json.dumps(recalls_packet, indent=2, ensure_ascii=False))
        print("---")
        print(json.dumps(incidents_packet, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()

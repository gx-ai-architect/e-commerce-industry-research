#!/usr/bin/env python3
"""
Fetches job postings data using free job search methods.
Outputs evidence packets in JSON format.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import re
from datetime import datetime, timezone

def fetch_jobs_indeed_rss(company, location='United States'):
    """Fetch jobs from Indeed RSS feed."""
    packets = []

    try:
        # Indeed RSS feed URL
        query = f"{company} jobs"
        location_param = urllib.parse.quote(location)
        query_param = urllib.parse.quote(query)

        # Indeed RSS feed
        url = f"https://www.indeed.com/rss?q={query_param}&l={location_param}"

        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            rss_content = response.read().decode('utf-8')

        # Parse RSS items (simple regex parsing)
        items = re.findall(r'<item>(.*?)</item>', rss_content, re.DOTALL)

        job_titles = []
        job_locations = []
        job_companies = []

        for item in items[:20]:  # Limit to first 20 items
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item, re.DOTALL)

            if title_match:
                title = title_match.group(1)
                job_titles.append(title)

                # Extract location from description if available
                if desc_match:
                    desc = desc_match.group(1)
                    location_pattern = re.search(r'<b>([^<]+)</b>', desc)
                    if location_pattern:
                        job_locations.append(location_pattern.group(1))

        packet = {
            "packet_id": f"PKT-JOBS-INDEED-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            "source": {
                "type": "dataset",
                "url": url,
                "title": f"Indeed RSS Feed - {company}",
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "collector": "job-postings"
            },
            "extractions": [
                {
                    "claim": f"Total job postings found: {len(job_titles)}",
                    "evidence": f"Found {len(job_titles)} job postings in RSS feed",
                    "evidence_type": "computed_metric"
                }
            ],
            "metadata": {
                "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
                "company_tags": [company],
                "topic_tags": ["hiring-velocity", "job-postings"],
                "job_titles_sample": job_titles[:5] if job_titles else [],
                "locations_sample": job_locations[:5] if job_locations else []
            }
        }

        # Add individual job title extractions
        for i, title in enumerate(job_titles[:5]):  # First 5 as samples
            packet["extractions"].append({
                "claim": f"Job posting: {title}",
                "evidence": title,
                "evidence_type": "direct_quote"
            })

        packets.append(packet)

    except Exception as e:
        # Error packet
        packet = {
            "packet_id": f"PKT-JOBS-ERROR-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            "source": {
                "type": "dataset",
                "url": url if 'url' in locals() else "N/A",
                "title": f"Indeed RSS Feed - {company} (ERROR)",
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "collector": "job-postings"
            },
            "extractions": [
                {
                    "claim": f"Error fetching job data: {str(e)}",
                    "evidence": str(e),
                    "evidence_type": "direct_quote"
                }
            ],
            "metadata": {
                "freshness": datetime.now(timezone.utc).strftime('%Y-%m'),
                "company_tags": [company],
                "status": "ERROR",
                "topic_tags": ["job-postings"]
            }
        }
        packets.append(packet)

    return packets

def main():
    parser = argparse.ArgumentParser(description='Fetch job postings data')
    parser.add_argument('--company', required=True, help='Company name to search for')
    parser.add_argument('--keywords', help='Additional keywords (optional)')
    parser.add_argument('--location', default='United States', help='Location to search in')

    args = parser.parse_args()

    # Use Indeed RSS feed
    packets = fetch_jobs_indeed_rss(args.company, args.location)

    # Output all packets as JSON array
    print(json.dumps(packets, indent=2))

if __name__ == '__main__':
    main()

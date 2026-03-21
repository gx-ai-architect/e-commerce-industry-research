# China Regulatory Data Mining

Scrapes Chinese government regulatory websites for antitrust enforcement actions, policy announcements, and trade statistics.

## Data Sources

- **SAMR** (State Administration for Market Regulation): Antitrust enforcement and penalties
- **NDRC** (National Development and Reform Commission): Economic policy and pricing regulations
- **China Customs**: Trade statistics and customs data

## Scripts

### `scripts/fetch-samr.py`
Fetches SAMR enforcement actions and penalty announcements.

```bash
python3 scripts/fetch-samr.py --query "拼多多"
python3 scripts/fetch-samr.py --query "PDD Holdings"
```

### `scripts/fetch-ndrc.py`
Fetches NDRC policy announcements.

```bash
python3 scripts/fetch-ndrc.py --query "电商"
```

### `scripts/fetch-china-customs.py`
Fetches China Customs trade data.

```bash
python3 scripts/fetch-china-customs.py --query "cross-border"
python3 scripts/fetch-china-customs.py --hs-code "8517"
```

## Output Format

All scripts output evidence packets in JSON format:

```json
{
  "packet_id": "PKT-SAMR-20260319143000",
  "source": {
    "type": "article",
    "url": "https://www.samr.gov.cn/...",
    "title": "SAMR Search Results: PDD",
    "retrieved_at": "2026-03-19T14:30:00Z",
    "collector": "china-regulatory"
  },
  "extractions": [...],
  "metadata": {
    "freshness": "2026-03",
    "company_tags": ["PDD"],
    "topic_tags": ["regulatory", "antitrust", "china"]
  }
}
```

## Testing

```bash
cd test
./test-samr.sh
```

## Known Limitations

- Chinese government websites may block foreign IP addresses
- Some sites require VPN access from outside China
- HTML parsing is basic - production use would need robust DOM parsing
- Rate limiting may apply

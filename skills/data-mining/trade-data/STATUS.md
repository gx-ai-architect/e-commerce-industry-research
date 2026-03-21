# Trade Data Skill Status

**Status:** BLOCKED (API auth required)

## Last Updated
2026-03-19

## Implementation Status

- [x] UN Comtrade API script (`fetch-comtrade.py`)
- [x] USITC DataWeb script (`fetch-usitc.py`)
- [x] US Census Trade script (`fetch-census-trade.py`)
- [x] Test suite (`test/test-fetch.sh`)
- [x] Documentation (SKILL.md)

## Test Results

**BLOCKED**: UN Comtrade API v2 now requires authentication (401 Access Denied).

Previously free tier (500 requests/day) now requires API key registration.

## Known Issues

1. **UN Comtrade API v2**: Requires authentication. Need to register at https://comtradeapi.un.org/ for API key. The free tier still exists but requires auth header.

2. **USITC API**: Limited public documentation. The endpoint structure in `fetch-usitc.py` is best-effort. If API returns 404/403, this is expected.

3. **US Census API**: Free tier works without API key for basic queries. Some advanced queries may require registration at https://api.census.gov/data/key_signup.html

## Blockers

**UN Comtrade**: Requires API key registration. Scripts are ready but need auth token to be added as environment variable or CLI arg.

## Solution

Add `--api-key` argument to `fetch-comtrade.py` and pass as header:
```python
req.add_header('Ocp-Apim-Subscription-Key', api_key)
```

## Future Enhancements

- Add API key support for UN Comtrade
- Add caching layer to avoid rate limits
- Support batch queries
- Add visualization tools (trade flow charts)
- Integrate with company shipping manifests (Panjiva, ImportGenius)

# EU Regulatory Data Mining

Scrapes European Union regulatory sources for legislation, trade data, safety alerts, and official announcements.

## Data Sources

- **EUR-Lex**: Official EU law database (legislation, regulations)
- **Eurostat**: EU trade statistics via SDMX API
- **RAPEX/Safety Gate**: Product safety alerts and recalls
- **EC Press Corner**: European Commission press releases

## Scripts

### `scripts/fetch-eurlex.py`
Searches EUR-Lex for EU legislation.

```bash
python3 scripts/fetch-eurlex.py --query "digital services act"
python3 scripts/fetch-eurlex.py --query "foreign subsidies regulation"
```

### `scripts/fetch-eurostat.py`
Fetches EU trade statistics via SDMX API (free, no auth required).

```bash
python3 scripts/fetch-eurostat.py --dataset "DS-016890"
python3 scripts/fetch-eurostat.py --dataset "DS-016890" --filter "M.CN.TOTAL"
```

### `scripts/fetch-rapex.py`
Fetches RAPEX product safety alerts (free, no auth required).

```bash
python3 scripts/fetch-rapex.py --country "China"
python3 scripts/fetch-rapex.py --category "Toys"
python3 scripts/fetch-rapex.py --query "electronics"
```

### `scripts/fetch-ec-press.py`
Fetches European Commission press releases.

```bash
python3 scripts/fetch-ec-press.py --query "digital markets"
python3 scripts/fetch-ec-press.py --query "Temu"
```

## Output Format

All scripts output evidence packets in JSON format.

## Testing

```bash
cd test
./test-eurlex.sh
./test-rapex.sh
```

## API Access

- **Eurostat SDMX API**: Free, no authentication required
- **RAPEX API**: Free, no authentication required
- **EUR-Lex**: Free, web scraping (no official API)
- **EC Press**: May have API endpoint or web scraping

## Known Limitations

- EUR-Lex and EC Press may require HTML parsing
- Eurostat SDMX format complex (nested JSON)
- RAPEX API endpoint may change

# Icelandic Taxi License Scraper

This repo automatically scrapes taxi license data from [island.is](https://island.is/listi-yfir-rekstrarleyfishafa-i-leigubilaakstri) daily using GitHub Actions.

- **output_data.csv**: Raw historical appends.
- **fixed_data.csv**: Processed summary with first/last appearances (download [here](fixed_data.csv)).

## How It Works
- Script: `scraper.py` (runs via Actions).
- Updates: Daily at midnight UTC.
- Source: Public website scrape.

Note: Web scraping may break if the site changes. Contributions welcome!

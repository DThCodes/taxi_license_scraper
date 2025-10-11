# Icelandic Taxi License Scraper

[![Daily Scrape Workflow](https://github.com/DThCodes/taxi_license_scraper/actions/workflows/scrape.yml/badge.svg)](https://github.com/DThCodes/taxi_license_scraper/actions/workflows/scrape.yml)

This repository automatically scrapes and processes the list of taxi operators with operating licenses in Iceland from the official [island.is website](https://island.is/listi-yfir-rekstrarleyfishafa-i-leigubilaakstri). It runs daily via GitHub Actions, appending new data to a historical log and generating a processed summary CSV.

The data includes operator names (Nafn), ID numbers (Kennitala), stations (Stöð), and more. This is public government data, scraped for transparency and ease of access.

**Note**: Web scraping may break if the source website changes its structure. Contributions to fix issues are welcome! Ensure compliance with the site's terms ( robots.txt allows general access).

## Generated Files
- **[taxi_licenses_historical.csv](taxi_licenses_historical.csv)**: Raw historical log of all scrapes over time. Each run appends the current snapshot with a timestamp. Useful for tracking changes or analyzing trends.
  - Columns: Nafn, Kennitala, Stöð, Stöðvarnúmer, Forráðamaður ef lögaðili, Uppfært af Samgöngustofu, Date, ID.
  - Download raw: [here](https://raw.githubusercontent.com/DThCodes/taxi_license_scraper/main/taxi_licenses_historical.csv).

- **[taxi_licenses_summary.csv](taxi_licenses_summary.csv)**: Processed summary view, deduplicated by unique ID, with first and last appearance dates. Sorted by name for easy reference—ideal for quick downloads and current overviews.
  - Columns: Nafn, Kennitala, Stöð, First appearance, Last appearance, ID.
  - Download raw: [here](https://raw.githubusercontent.com/DThCodes/taxi_license_scraper/main/taxi_licenses_summary.csv).

Files update daily at midnight UTC (or on manual trigger). Last update: Check the latest commit in the repo.

## How It Works
- **Scraper Script**: `scraper.py` fetches the page, extracts table data using BeautifulSoup, pads Kennitala if needed, builds unique IDs, and handles updates.
- **Automation**: GitHub Actions workflow (`.github/workflows/scrape.yml`) runs the script, commits changes if data is new, and pushes to the main branch.
- **Processing**: Uses pandas to group historical data into the summary, calculating date ranges for each unique operator/station combo.
- **Schedule**: Daily via cron, but can be triggered manually in the Actions tab.

## Local Setup (For Development)
1. Clone the repo: `git clone https://github.com/DThCodes/taxi_license_scraper.git`.
2. Install dependencies: `pip install requests beautifulsoup4 pandas`.
3. Run the script: `python scraper.py` (generates/updates CSVs locally).
4. Commit and push changes to trigger updates.

## Data Notes
- **Kennitala**: Icelandic ID numbers, padded to 10 digits if scraped as 9.
- **Dates**: In DD.MM.YYYY format. "First/Last appearance" track when entries first/last appeared in scrapes.
- **Potential Issues**: If the site uses dynamic content (JS-loaded), scraping might miss data—currently assumes static HTML.
- **License**: Data is public domain (from government site); code is MIT-licensed for reuse.

## Contributing
- Fork the repo and submit pull requests (e.g., to handle site changes or add features like email alerts).
- Report issues via GitHub Issues, especially if scrapes fail (include workflow logs).

For questions, open an issue or contact the maintainer.

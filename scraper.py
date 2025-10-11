import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
import pandas as pd

# Column indices from scraped data (0-based)
ORIGINAL_NAFN_COL = 0
ORIGINAL_KENNITALA_COL = 1
ORIGINAL_STOD_COL = 2
ORIGINAL_STODVARNUMER_COL = 3
ORIGINAL_FORRADAMADUR_COL = 4

# URL to scrape
url = "https://island.is/listi-yfir-rekstrarleyfishafa-i-leigubilaakstri"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract truncated update value
    target_element = soup.find('div', class_='_1wc4apv0 _1wc4apv5 _1ovv93d1o3 hpuvl25')  # Adjusted class based on common patterns; verify if needed
    extracted_value_truncated = ""
    if target_element:
        previous_p_element = target_element.find_previous('p')
        if previous_p_element:
            extracted_value = previous_p_element.get_text(strip=True)
            extracted_value_truncated = extracted_value[8:]

    # Find table
    table = soup.find('table', class_='_1wc4apv0 _1wc4apv5 _1ovv93d1o3 _1ovv93d1o4 b7a64p0')
    data = []
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip header
            cols = row.find_all(['th', 'td'])
            row_data = [col.get_text(strip=True) for col in cols]
            while len(row_data) < 5:
                row_data.append("")
            data.append(row_data)

    # Current date
    current_date = datetime.now().strftime("%d.%m.%Y")

    # Output header
    output_header = ["Nafn", "Kennitala", "Stöð", "Stöðvarnúmer", "Forráðamaður, ef lögaðili", "Uppfært af Samgöngustofu", "Date", "ID"]

    # Process data
    processed_data = []
    for row in data:
        nafn = row[ORIGINAL_NAFN_COL] if len(row) > ORIGINAL_NAFN_COL else ""
        kennitala = row[ORIGINAL_KENNITALA_COL] if len(row) > ORIGINAL_KENNITALA_COL else ""
        if len(kennitala) == 9:
            kennitala = "0" + kennitala
        stod = row[ORIGINAL_STOD_COL] if len(row) > ORIGINAL_STOD_COL else ""
        stodvarnumer = row[ORIGINAL_STODVARNUMER_COL] if len(row) > ORIGINAL_STODVARNUMER_COL else ""
        forradamadur = row[ORIGINAL_FORRADAMADUR_COL] if len(row) > ORIGINAL_FORRADAMADUR_COL else ""

        # Build ID
        id_value = nafn
        if stodvarnumer:
            id_value += " - " + stod + " - " + stodvarnumer
        elif stod:
            id_value += " - " + stod

        # Reconstructed row
        reconstructed_row = [
            nafn, kennitala, stod, stodvarnumer, forradamadur,
            extracted_value_truncated, current_date, id_value
        ]
        processed_data.append(reconstructed_row)

    # Save to taxi_licenses_historical.csv (append if exists)
    filename = "taxi_licenses_historical.csv"
    file_exists = os.path.exists(filename)
    with open(filename, 'a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(output_header)
        writer.writerows(processed_data)

    print(f"Data successfully saved to {filename}")

    # Process to taxi_licenses_summary.csv
    output_filename = "taxi_licenses_summary.csv"
    try:
        df = pd.read_csv(filename, dtype={'Kennitala': str})
        df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y', errors='coerce')
        grouped = df.dropna(subset=['Date']).groupby('ID')['Date'].agg(['min', 'max']).reset_index()
        grouped = grouped.rename(columns={'min': 'First appearance', 'max': 'Last appearance'})
        merged_df = pd.merge(grouped, df[['ID', 'Nafn', 'Kennitala', 'Stöð']].drop_duplicates(subset=['ID']), on='ID', how='left')
        final_df = merged_df[['Nafn', 'Kennitala', 'Stöð', 'First appearance', 'Last appearance', 'ID']]
        final_df = final_df.sort_values(by='Nafn', ascending=True)
        final_df['First appearance'] = final_df['First appearance'].dt.strftime('%d.%m.%Y')
        final_df['Last appearance'] = final_df['Last appearance'].dt.strftime('%d.%m.%Y')
        final_df.to_csv(output_filename, index=False)
        print(f"Processed data saved to {output_filename}")
    except Exception as e:
        print(f"Error processing: {e}")
else:
    print(f"Failed to retrieve data. Status: {response.status_code}")

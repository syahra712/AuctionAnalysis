import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

# URLs to scrape
URLS = {
    "Land Cruiser Prado": "https://www.beforward.jp/toyota/land-cruiser-prado/bw759006/id/10023141/",
    "Corolla Fielder": "https://www.beforward.jp/toyota/corolla-fielder/bx110228/id/10331058/",
    "Probox": "https://www.beforward.jp/toyota/probox/bw892545/id/10157960/"
}

# CSV file name
CSV_FILE = "bef4ward_price_tracking.csv"

# Function to fetch and parse data
def scrape_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edge/98.0.1108.43"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Extracting price values
        price_yen = soup.select_one("span.price.ip-usd-price")
        price_total = soup.select_one("span#fn-vehicle-price-total-price")

        price_yen_text = price_yen.get_text(strip=True) if price_yen else "N/A"
        price_total_text = price_total.get_text(strip=True) if price_total else "N/A"
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        return [timestamp, url, price_yen_text, price_total_text]
    else:
        print(f"Error {response.status_code}: Could not fetch data from {url}")
        return None

# Function to save data to CSV
def save_to_csv(data):
    file_exists = False
    try:
        with open(CSV_FILE, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "URL", "Price (JPY)", "Total Price"])  # Write headers if file doesn't exist
        writer.writerow(data)

# Main execution
if __name__ == "__main__":
    for name, url in URLS.items():
        print(f"Scraping {name}...")
        scraped_data = scrape_data(url)
        if scraped_data:
            save_to_csv(scraped_data)
            print(f"Data saved for {name}: {scraped_data}")

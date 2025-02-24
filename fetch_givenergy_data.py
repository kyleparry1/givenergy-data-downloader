import requests
import datetime
import sys
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup logging
LOG_FILE = "data_fetch.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Load config from file
CONFIG_FILE = "config.json"
if not os.path.exists(CONFIG_FILE):
    print(f"Error: Configuration file '{CONFIG_FILE}' not found.")
    sys.exit(1)

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = json.load(file)

# Extract configuration values
BASE_URL = config.get("base_url", "")
HEADERS = config.get("headers", {})
COOKIES = config.get("cookies", {})

if not BASE_URL or not HEADERS or not COOKIES:
    print("Error: Missing required values in configuration file.")
    sys.exit(1)

# Create the data directory if it doesn't exist
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Number of concurrent downloads (adjust based on server limits)
MAX_WORKERS = 5

def fetch_csv_for_date(date_str, max_retries=3):
    """Fetch CSV for a single date with retries and save in 'data/' directory."""
    filename = os.path.join(DATA_DIR, f"system_data_{date_str}.csv")

    for attempt in range(max_retries):
        try:
            response = requests.post(
                BASE_URL,
                params={"date": date_str},
                headers=HEADERS,
                cookies=COOKIES
            )

            if response.status_code == 200:
                with open(filename, "wb") as file:
                    file.write(response.content)
                logging.info(f"✅ Success: CSV file saved as {filename}")
                return True  # Download successful

            logging.error(f"❌ ERROR {response.status_code}: Failed to fetch CSV for {date_str} (Attempt {attempt+1}/{max_retries})")

        except requests.exceptions.RequestException as e:
            logging.error(f"⚠️ Network Error for {date_str} (Attempt {attempt+1}/{max_retries}): {str(e)}")

    logging.error(f"🚨 Failed to download {date_str} after {max_retries} attempts.")
    return False  # Download failed

def fetch_and_store_data(start_date, end_date):
    """Fetch data from the API using multi-threading for efficiency."""
    date_list = []
    current_date = start_date

    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += datetime.timedelta(days=1)

    logging.info(f"📌 Starting download for {len(date_list)} dates...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_csv_for_date, date): date for date in date_list}
        for future in as_completed(futures):
            date = futures[future]
            try:
                success = future.result()
                if not success:
                    print(f"⚠️ Failed to download: {date}")
            except Exception as e:
                logging.error(f"❌ Exception for {date}: {str(e)}")

    logging.info("✅ All downloads completed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <start_date> [end_date]")
        sys.exit(1)

    start_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d") if len(sys.argv) > 2 else start_date

    fetch_and_store_data(start_date, end_date)
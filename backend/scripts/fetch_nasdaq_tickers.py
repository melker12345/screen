import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from pathlib import Path
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup logging
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
LOG_FILE = PROJECT_ROOT / 'backend' / 'logs' / 'fetch_tickers.log'
TICKERS_FILE = PROJECT_ROOT / 'backend' / 'data' / 'tickers.csv'

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Add console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

def fetch_stockholm_tickers():
    url = "https://stockanalysis.com/list/nasdaq-stockholm/"
    
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    
    # Initialize the driver
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    symbols = []
    try:
        while True:
            # Wait for the table to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='quote/sto/']"))
            )
            
            # Get current page symbols
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            links = soup.find_all('a', href=lambda x: x and 'quote/sto/' in x)
            
            # Extract symbols
            for link in links:
                symbol = link.text.strip()
                symbol = f"{symbol}.ST"
                if symbol not in symbols:  # Avoid duplicates
                    symbols.append(symbol)
            
            # Try to find and click "Next" button
            try:
                next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
                if not next_button.is_enabled():
                    break
                next_button.click()
                time.sleep(2)  # Wait for page to load
            except NoSuchElementException:
                break
            
    except Exception as e:
        logging.error(f"Error during fetching: {str(e)}")
    finally:
        driver.quit()
    
    return sorted(list(set(symbols)))  # Remove any duplicates and sort

def save_tickers(symbols):
    """Save tickers to CSV file"""
    try:
        if not symbols:
            logging.error("No tickers to save!")
            return False
            
        # Ensure directory exists
        TICKERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        df = pd.DataFrame({'Symbol': symbols})
        df.to_csv(TICKERS_FILE, index=False)
        logging.info(f"Successfully saved {len(symbols)} tickers to {TICKERS_FILE}")
        
        # Display first few tickers as verification
        logging.info("\nFirst few tickers saved:")
        for index, row in df.head().iterrows():
            logging.info(f"{row['Symbol']}")
            
        return True
        
    except Exception as e:
        logging.error(f"Error saving tickers: {str(e)}")
        return False

def main():
    """Main function to fetch and save Nasdaq Stockholm tickers"""
    logging.info("Starting Nasdaq Stockholm ticker fetch process...")
    
    # Fetch tickers
    symbols = fetch_stockholm_tickers()
    
    # Save tickers
    if symbols:
        success = save_tickers(symbols)
        if success:
            logging.info("Ticker fetch process completed successfully!")
        else:
            logging.error("Failed to save tickers!")
    else:
        logging.error("No tickers were fetched!")

if __name__ == "__main__":
    main()

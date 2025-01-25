import requests
import pandas as pd
import logging
from pathlib import Path
import time

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

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

def fetch_swedish_stocks():
    """
    Fetch Swedish stocks from Yahoo Finance using their screener API
    """
    try:
        logging.info("Starting to fetch Swedish stocks...")
        
        # Base URL for Yahoo Finance screener
        base_url = "https://query1.finance.yahoo.com/v1/finance/screener"
        
        # Parameters for the request
        params = {
            "crumb": "none",
            "lang": "en-US",
            "region": "US",
            "formatted": "true",
            "corsDomain": "finance.yahoo.com",
            "fields": "symbol,longName,exchange",
            "size": "100",
            "offset": "0",
            "userId": "",
            "userIdType": "guid",
        }

        # Headers to mimic browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # List to store all tickers
        all_tickers = []
        
        # Swedish exchanges
        swedish_exchanges = ['STO', 'ST']
        
        offset = 0
        total_fetched = 0
        
        while True:
            logging.info(f"Fetching batch starting at offset {offset}...")
            
            params['offset'] = str(offset)
            response = requests.get(
                f"{base_url}/lists/EQUITY_SWEDEN",
                params=params,
                headers=headers
            )
            
            if response.status_code != 200:
                logging.error(f"Failed to fetch data: {response.status_code}")
                logging.error(f"Response: {response.text}")
                break
                
            data = response.json()
            
            if 'finance' not in data or 'result' not in data['finance']:
                logging.error("Unexpected response format")
                break
                
            quotes = data['finance']['result'][0].get('quotes', [])
            
            if not quotes:
                break
                
            for quote in quotes:
                symbol = quote.get('symbol', '')
                if any(exchange in symbol for exchange in swedish_exchanges):
                    all_tickers.append({
                        'Ticker': symbol,
                        'Name': quote.get('longName', ''),
                        'Exchange': quote.get('exchange', '')
                    })
                    total_fetched += 1
            
            logging.info(f"Found {len(quotes)} stocks in this batch, {total_fetched} Swedish stocks so far")
            
            offset += 100
            time.sleep(1)  # Be nice to Yahoo's servers
            
            if len(quotes) < 100:  # Last page
                break
        
        logging.info(f"Total Swedish stocks found: {len(all_tickers)}")
        return pd.DataFrame(all_tickers)
        
    except Exception as e:
        logging.error(f"Error fetching Swedish stocks: {e}", exc_info=True)
        return pd.DataFrame()

def save_tickers(df):
    """Save tickers to CSV file"""
    try:
        if df.empty:
            logging.error("No tickers to save!")
            return False
            
        # Ensure the directory exists
        TICKERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        df.to_csv(TICKERS_FILE, index=False)
        logging.info(f"Successfully saved {len(df)} tickers to {TICKERS_FILE}")
        return True
        
    except Exception as e:
        logging.error(f"Error saving tickers: {e}", exc_info=True)
        return False

def main():
    """Main function to fetch and save Swedish stock tickers"""
    logging.info("Starting ticker fetch process...")
    
    # Fetch tickers
    df = fetch_swedish_stocks()
    
    # Save tickers
    if not df.empty:
        success = save_tickers(df)
        if success:
            logging.info("Ticker fetch process completed successfully!")
        else:
            logging.error("Failed to save tickers!")
    else:
        logging.error("No tickers were fetched!")

if __name__ == "__main__":
    main()

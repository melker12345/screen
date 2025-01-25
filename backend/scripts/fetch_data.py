import yfinance as yf
import pandas as pd
import os
from datetime import datetime
import schedule
import time
import logging
import sqlite3
import ta
from pathlib import Path

# Get the absolute path to the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()

# Configuration
TICKERS_FILE = Path(PROJECT_ROOT) / 'backend' / 'data' / 'tickers.csv'
OUTPUT_FILE = Path(PROJECT_ROOT) / 'backend' / 'data' / 'latest_close.csv'
LOG_FILE = Path(PROJECT_ROOT) / 'backend' / 'logs' / 'fetch_data.log'
DB_PATH = Path(PROJECT_ROOT) / 'database' / 'stock_data.db'
DATE_FORMAT = '%Y-%m-%d'

# Ensure directories exist
os.makedirs(TICKERS_FILE.parent, exist_ok=True)
os.makedirs(LOG_FILE.parent, exist_ok=True)
os.makedirs(DB_PATH.parent, exist_ok=True)

# Setup Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    datefmt=DATE_FORMAT
)

# Add console handler for immediate feedback
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

def initialize_database():
    """Initialize the SQLite database and create tables if they don't exist."""
    try:
        logging.info("Initializing database...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS latest_close (
                Ticker TEXT PRIMARY KEY,
                Date TEXT,
                Close REAL,
                RSI REAL,
                MACD REAL,
                MACD_Signal REAL,
                MA50 REAL,
                MA200 REAL
            )
        ''')
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully at %s", DB_PATH)
    except Exception as e:
        logging.error("Error initializing database: %s", str(e), exc_info=True)

def load_tickers(file_path):
    """Load the list of tickers from a CSV file."""
    try:
        if not os.path.exists(file_path):
            logging.error("Tickers file not found at %s", file_path)
            return []
            
        df = pd.read_csv(file_path)
        tickers = df['Ticker'].tolist()
        logging.info("Loaded %d tickers from %s", len(tickers), file_path)
        
        # Log first few tickers for verification
        if tickers:
            logging.info("First 5 tickers: %s", ', '.join(tickers[:5]))
        return tickers
    except Exception as e:
        logging.error("Error loading tickers: %s", str(e), exc_info=True)
        return []

def fetch_latest_close(tickers):
    """Fetch the latest closing price for each ticker."""
    try:
        if not tickers:
            logging.error("No tickers provided to fetch data")
            return pd.DataFrame()

        logging.info("Fetching data for %d tickers...", len(tickers))
        
        # Download data for the latest day
        data = yf.download(
            tickers,
            period='1d',
            interval='1d',
            group_by='ticker',
            threads=True,
            progress=False
        )

        if len(tickers) == 1:
            # yfinance returns a different structure for a single ticker
            data = {tickers[0]: data}

        latest_closes = []
        successful_fetches = 0
        failed_fetches = 0
        
        for ticker in tickers:
            try:
                if ticker in data:
                    ticker_data = data[ticker]
                    if not ticker_data.empty:
                        close_price = ticker_data['Close'].iloc[-1]
                        date = ticker_data.index[-1].strftime(DATE_FORMAT)
                        latest_closes.append({
                            'Ticker': ticker,
                            'Date': date,
                            'Close': close_price
                        })
                        successful_fetches += 1
                    else:
                        logging.warning("No data available for %s", ticker)
                        failed_fetches += 1
                else:
                    logging.warning("Ticker %s not found in response", ticker)
                    failed_fetches += 1
            except Exception as e:
                logging.error("Error processing ticker %s: %s", ticker, str(e))
                failed_fetches += 1
                continue

        logging.info("Data fetch complete. Successful: %d, Failed: %d", 
                    successful_fetches, failed_fetches)

        if not latest_closes:
            logging.warning("No data was fetched for any ticker")
            return pd.DataFrame()

        return pd.DataFrame(latest_closes)
    except Exception as e:
        logging.error("Error in fetch_latest_close: %s", str(e), exc_info=True)
        return pd.DataFrame()

def calculate_indicators(df):
    """Calculate RSI, MACD, and Moving Averages."""
    try:
        if df.empty:
            logging.warning("Empty DataFrame provided for indicator calculation.")
            return df

        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
        macd = ta.trend.MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()
        logging.info("Technical indicators calculated successfully.")
        return df
    except Exception as e:
        logging.error("Error calculating technical indicators: %s", str(e), exc_info=True)
        return df

def store_data(df):
    """Store the DataFrame data into the SQLite database."""
    try:
        if df.empty:
            logging.warning("Empty DataFrame provided for storage.")
            return

        conn = sqlite3.connect(DB_PATH)
        df.to_sql('latest_close', conn, if_exists='replace', index=False)
        conn.close()
        logging.info("Data stored in the database successfully at %s", DB_PATH)
        
        # Also save to CSV for backup
        df.to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Data saved to CSV at {OUTPUT_FILE}")
    except Exception as e:
        logging.error("Error storing data: %s", str(e), exc_info=True)

def job():
    """Scheduled job to fetch and save latest close prices."""
    logging.info("Running scheduled data fetch job.")
    try:
        tickers = load_tickers(TICKERS_FILE)
        if not tickers:
            logging.warning("No tickers to process.")
            return

        latest_close_df = fetch_latest_close(tickers)
        if not latest_close_df.empty:
            latest_close_df = calculate_indicators(latest_close_df)
            store_data(latest_close_df)
            logging.info(f"Successfully processed {len(latest_close_df)} stocks.")
        else:
            logging.warning("No latest close data to save.")
    except Exception as e:
        logging.error("Error in job execution: %s", str(e), exc_info=True)

def main():
    """Run the data fetching process immediately"""
    try:
        initialize_database()
        logging.info("Starting data fetch process...")
        job()
        logging.info("Data fetch process completed")
    except Exception as e:
        logging.error("Error in main execution: %s", str(e), exc_info=True)
        raise

if __name__ == "__main__":
    main()

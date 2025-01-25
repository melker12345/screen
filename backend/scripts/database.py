import sqlite3
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import logging
from pathlib import Path
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
DB_FILE = DATA_DIR / 'stock_data.db'

def create_database():
    """Create SQLite database and tables"""
    # Remove existing database if it exists
    if DB_FILE.exists():
        DB_FILE.unlink()
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Create stocks table with status column
    c.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT PRIMARY KEY,
            name TEXT,
            status TEXT,
            last_updated TIMESTAMP
        )
    ''')
    
    # Create daily_prices table
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_prices (
            symbol TEXT,
            date DATE,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            adjusted_close REAL,
            PRIMARY KEY (symbol, date),
            FOREIGN KEY (symbol) REFERENCES stocks(symbol)
        )
    ''')
    
    conn.commit()
    conn.close()
    logging.info(f"Database created at {DB_FILE}")

def fetch_stock_data(symbol, start_date, end_date):
    """Fetch historical data for a single stock"""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)
        if not df.empty:
            df = df.reset_index()
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            return df, 'active'
        return None, 'no_data'
    except Exception as e:
        if 'No timezone found' in str(e):
            return None, 'delisted'
        logging.error(f"Error fetching data for {symbol}: {str(e)}")
        return None, 'error'

def clean_database():
    """Remove stocks with no data from the database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Remove stocks marked as delisted or with no data
    c.execute('''
        DELETE FROM daily_prices 
        WHERE symbol IN (
            SELECT symbol FROM stocks 
            WHERE status IN ('delisted', 'no_data', 'error')
        )
    ''')
    
    c.execute('''
        DELETE FROM stocks 
        WHERE status IN ('delisted', 'no_data', 'error')
    ''')
    
    conn.commit()
    conn.close()
    logging.info("Database cleaned")

def update_stock_data():
    """Update database with latest stock data"""
    conn = sqlite3.connect(DB_FILE)
    
    # Read tickers from CSV
    tickers_df = pd.read_csv(DATA_DIR / 'tickers.csv')
    
    # Calculate date range (3 years back from today)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)
    
    active_stocks = 0
    delisted_stocks = 0
    error_stocks = 0
    
    total_stocks = len(tickers_df)
    for idx, row in tickers_df.iterrows():
        symbol = row['Symbol']
        logging.info(f"Processing {symbol} ({idx+1}/{total_stocks})")
        
        # Fetch data
        df, status = fetch_stock_data(symbol, start_date, end_date)
        
        # Update stocks table with status
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO stocks (symbol, status, last_updated)
            VALUES (?, ?, ?)
        ''', (symbol, status, datetime.now()))
        
        if status == 'active' and df is not None:
            active_stocks += 1
            # Prepare daily prices data
            price_data = []
            for _, price_row in df.iterrows():
                price_data.append((
                    symbol,
                    price_row['Date'],
                    price_row['Open'],
                    price_row['High'],
                    price_row['Low'],
                    price_row['Close'],
                    price_row['Volume'],
                    price_row['Close']  # Using Close as Adjusted Close if not available
                ))
            
            # Batch insert daily prices
            cursor.executemany('''
                INSERT OR REPLACE INTO daily_prices 
                (symbol, date, open, high, low, close, volume, adjusted_close)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', price_data)
        elif status == 'delisted':
            delisted_stocks += 1
        else:
            error_stocks += 1
            
        conn.commit()
    
    conn.close()
    
    # Clean up the database
    clean_database()
    
    logging.info(f"\nDatabase update completed:")
    logging.info(f"Active stocks: {active_stocks}")
    logging.info(f"Delisted stocks: {delisted_stocks}")
    logging.info(f"Error stocks: {error_stocks}")

if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Create database if it doesn't exist
    create_database()
    
    # Update stock data
    update_stock_data()

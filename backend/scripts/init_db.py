import sqlite3
from pathlib import Path
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import sys
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_path = Path(__file__).parent.parent / 'logs'
    log_path.mkdir(exist_ok=True)
    log_file = log_path / 'stock_data.log'
    
    # Configure logging to both file and console
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # File handler with rotation
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Setup logger
    logger = logging.getLogger('stock_data')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_existing_stocks(conn):
    """Get list of stocks that are already in the database"""
    cursor = conn.execute("SELECT DISTINCT symbol FROM stock_prices")
    return {row[0] for row in cursor.fetchall()}

def init_database():
    logger = setup_logging()
    logger.info("Starting database initialization...")
    db_path = Path(__file__).parent.parent / 'data' / 'stock_data.db'
    logger.info(f"Database path: {db_path}")
    
    # Create tables
    logger.info("Setting up database tables...")
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            symbol TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            PRIMARY KEY (symbol, date)
        )
        """)
        
        # Read tickers from CSV
        tickers_path = Path(__file__).parent.parent / 'data' / 'tickers.csv'
        logger.info(f"Reading tickers from: {tickers_path}")
        df_tickers = pd.read_csv(tickers_path)
        total_tickers = len(df_tickers)
        logger.info(f"Found {total_tickers} tickers")
        
        # Get existing stocks
        existing_stocks = get_existing_stocks(conn)
        logger.info(f"Found {len(existing_stocks)} stocks already in database")
        
        # Get stock data for each ticker
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # Get 1 year of data
        
        success_count = 0
        error_count = 0
        skip_count = 0
        
        for i, symbol in enumerate(df_tickers['Symbol'].values, 1):
            try:
                # Add .ST suffix for Swedish stocks if not present
                if not symbol.endswith('.ST'):
                    symbol = f"{symbol}.ST"
                
                # Skip if already in database
                if symbol in existing_stocks:
                    logger.info(f"[SKIP] [{i}/{total_tickers}] {symbol} - already in database")
                    skip_count += 1
                    continue
                
                logger.info(f"Processing [{i}/{total_tickers}] {symbol}")
                
                stock = yf.Ticker(symbol)
                hist = stock.history(start=start_date, end=end_date)
                
                if not hist.empty:
                    # Prepare data for SQL - select only the columns we want
                    hist.reset_index(inplace=True)
                    selected_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
                    hist = hist[selected_columns]
                    
                    # Rename columns to match our schema
                    hist.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
                    hist['date'] = hist['date'].dt.strftime('%Y-%m-%d')
                    hist['symbol'] = symbol
                    
                    # Insert data
                    hist.to_sql('stock_prices', conn, if_exists='append', index=False,
                              dtype={
                                  'symbol': 'TEXT',
                                  'date': 'TEXT',
                                  'open': 'REAL',
                                  'high': 'REAL',
                                  'low': 'REAL',
                                  'close': 'REAL',
                                  'volume': 'INTEGER'
                              })
                    logger.info(f"[SUCCESS] Added {len(hist)} rows for {symbol}")
                    success_count += 1
                else:
                    logger.warning(f"[FAILED] No data available for {symbol}")
                    error_count += 1
            except Exception as e:
                logger.error(f"[ERROR] Failed processing {symbol}: {str(e)}")
                error_count += 1
                continue
            
            # Print progress every 10 stocks
            if i % 10 == 0:
                logger.info("\n=== Progress Report ===")
                logger.info(f"Processed: {i}/{total_tickers} stocks")
                logger.info(f"Success rate: {(success_count/(i-skip_count))*100:.1f}%")
                logger.info(f"Successful: {success_count}")
                logger.info(f"Failed: {error_count}")
                logger.info(f"Skipped: {skip_count}")
                logger.info("=====================\n")
        
        logger.info("\n=== Final Report ===")
        logger.info(f"Successfully processed: {success_count} stocks")
        logger.info(f"Failed to process: {error_count} stocks")
        logger.info(f"Skipped (already in DB): {skip_count} stocks")
        logger.info(f"Total completion rate: {(success_count/(total_tickers-skip_count))*100:.1f}%")
        
        # Print some sample data
        logger.info("\nSample of data in database:")
        cursor = conn.execute("""
            SELECT symbol, COUNT(*) as days, MIN(date) as first_date, MAX(date) as last_date 
            FROM stock_prices 
            GROUP BY symbol
            LIMIT 5
        """)
        logger.info("Symbol | Days | First Date | Last Date")
        logger.info("-" * 50)
        for row in cursor:
            logger.info(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
        logger.info("===================")

if __name__ == "__main__":
    init_database()

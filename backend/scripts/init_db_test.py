import sqlite3
from pathlib import Path
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import sys

def init_database_test():
    print("Starting database initialization (TEST MODE)...")
    db_path = Path(__file__).parent.parent / 'data' / 'stock_data.db'
    print(f"Database path: {db_path}")
    
    # Create tables
    print("Creating database tables...")
    with sqlite3.connect(db_path) as conn:
        # Drop existing table if it exists
        conn.execute("DROP TABLE IF EXISTS stock_prices")
        
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
        
        # Test with just 5 stocks
        test_stocks = ['ERIC-B.ST', 'VOLV-B.ST', 'SEB-A.ST', 'SAND.ST', 'ABB.ST']
        total_stocks = len(test_stocks)
        print(f"Testing with {total_stocks} stocks")
        
        # Get stock data for each ticker
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)  # Get 30 days of data for testing
        
        success_count = 0
        error_count = 0
        
        for i, symbol in enumerate(test_stocks, 1):
            try:
                print(f"\nProcessing [{i}/{total_stocks}] {symbol}")
                sys.stdout.flush()  # Force print to show immediately
                
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
                    print(f"✓ Added {len(hist)} rows for {symbol}")
                    success_count += 1
                else:
                    print(f"✗ No data available for {symbol}")
                    error_count += 1
            except Exception as e:
                print(f"✗ Error processing {symbol}: {str(e)}")
                error_count += 1
                continue
        
        print("\nTest initialization completed!")
        print(f"Successfully processed: {success_count} stocks")
        print(f"Failed to process: {error_count} stocks")
        print(f"Total completion rate: {(success_count/total_stocks)*100:.1f}%")
        
        # Print some sample data
        print("\nSample of data in database:")
        cursor = conn.execute("""
            SELECT symbol, COUNT(*) as days, MIN(date) as first_date, MAX(date) as last_date 
            FROM stock_prices 
            GROUP BY symbol
        """)
        print("Symbol | Days | First Date | Last Date")
        print("-" * 50)
        for row in cursor:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

if __name__ == "__main__":
    init_database_test()

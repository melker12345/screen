import sqlite3
import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
DB_FILE = DATA_DIR / 'stock_data.db'

# Connect to database
conn = sqlite3.connect(DB_FILE)

# View stocks table
print("\nStocks Table (First 5 rows):")
print("-" * 80)
stocks_df = pd.read_sql_query("""
    SELECT * FROM stocks 
    WHERE status = 'active'
    LIMIT 5
""", conn)
print(stocks_df.to_string())

# View daily prices table
print("\nDaily Prices Table (Sample of recent prices for first stock):")
print("-" * 80)
prices_df = pd.read_sql_query("""
    SELECT symbol, date, open, high, low, close, volume
    FROM daily_prices
    WHERE symbol = (SELECT symbol FROM stocks WHERE status = 'active' LIMIT 1)
    ORDER BY date DESC
    LIMIT 5
""", conn)
print(prices_df.to_string())

conn.close()

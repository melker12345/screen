import sqlite3
from pathlib import Path

def check_database():
    db_path = Path(__file__).parent.parent / 'data' / 'stock_data.db'
    
    with sqlite3.connect(db_path) as conn:
        # Get total number of records
        cursor = conn.execute("SELECT COUNT(*) FROM stock_prices")
        total_records = cursor.fetchone()[0]
        print(f"Total records in database: {total_records}")
        
        # Get number of unique stocks
        cursor = conn.execute("SELECT COUNT(DISTINCT symbol) FROM stock_prices")
        unique_stocks = cursor.fetchone()[0]
        print(f"Number of unique stocks: {unique_stocks}")
        
        # Get some sample data
        cursor = conn.execute("""
            SELECT symbol, COUNT(*) as days, MIN(date) as first_date, MAX(date) as last_date 
            FROM stock_prices 
            GROUP BY symbol 
            LIMIT 5
        """)
        print("\nSample of stocks in database:")
        print("Symbol | Days | First Date | Last Date")
        print("-" * 50)
        for row in cursor:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

if __name__ == "__main__":
    check_database()

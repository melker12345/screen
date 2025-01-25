import pandas as pd
import ta
import sqlite3
from typing import Dict, Any, List
from pathlib import Path
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechnicalIndicators:
    def __init__(self):
        self.db_path = str(Path(__file__).parent.parent / 'data' / 'stock_data.db')
        logger.info(f"Database path: {self.db_path}")

    def get_stock_data(self, symbol: str) -> pd.DataFrame:
        """Get stock data from database"""
        try:
            query = "SELECT date, open, high, low, close, volume FROM stock_prices WHERE symbol = ? ORDER BY date"
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(query, conn, params=(symbol,))
                df['date'] = pd.to_datetime(df['date'])
                logger.info(f"Retrieved {len(df)} rows for {symbol}")
                return df
        except Exception as e:
            logger.error(f"Error getting stock data for {symbol}: {str(e)}")
            raise

    def get_all_stocks(self) -> List[str]:
        """Get list of all available stocks"""
        try:
            query = "SELECT DISTINCT symbol FROM stock_prices"
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(query, conn)
                stocks = df['symbol'].tolist()
                logger.info(f"Found {len(stocks)} stocks")
                return stocks
        except Exception as e:
            logger.error(f"Error getting stock list: {str(e)}")
            raise

    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate RSI"""
        try:
            # Check if we have enough data points
            if len(df) < period * 2:
                logger.warning(f"Not enough data points for RSI calculation. Need at least {period * 2}, got {len(df)}")
                return pd.Series([50] * len(df))  # Return neutral RSI for insufficient data
            
            # Log input data
            logger.info(f"Calculating RSI with {len(df)} data points")
            logger.info(f"Last 5 closing prices:\n{df['close'].tail()}")
            
            # Calculate price changes
            delta = df['close'].diff()
            logger.info(f"Last 5 price changes:\n{delta.tail()}")
            
            # Calculate RSI using ta library
            rsi = ta.momentum.RSIIndicator(df['close'], window=period).rsi()
            
            # Handle NaN values
            nan_count = rsi.isna().sum()
            if nan_count > 0:
                logger.warning(f"Found {nan_count} NaN values in RSI calculation")
                # Fill NaN values with previous valid values, then fill remaining with 50
                rsi = rsi.ffill(limit=1).fillna(50)
            
            # Log RSI values
            logger.info(f"RSI calculation:")
            logger.info(f"Min RSI: {rsi.min()}")
            logger.info(f"Max RSI: {rsi.max()}")
            logger.info(f"Mean RSI: {rsi.mean()}")
            logger.info(f"Last 5 RSI values:\n{rsi.tail()}")
            
            # Ensure RSI values are within valid range
            rsi = rsi.clip(0, 100)
            
            return rsi
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            raise

    def calculate_macd(self, df: pd.DataFrame) -> tuple:
        """Calculate MACD"""
        try:
            # We need enough data points for both MACD and signal line
            if len(df) < 35:  # 26 (slow MA) + 9 (signal) = 35 minimum points
                logger.warning(f"Not enough data points for MACD calculation. Need at least 35, got {len(df)}")
                return pd.Series([0] * len(df)), pd.Series([0] * len(df)), pd.Series([0] * len(df))
            
            # Calculate MACD using ta library
            macd_indicator = ta.trend.MACD(df['close'])
            macd = macd_indicator.macd()
            signal = macd_indicator.macd_signal()
            
            # Handle NaN values
            macd = macd.ffill().fillna(0)
            signal = signal.ffill().fillna(0)
            
            # Calculate histogram as the difference between MACD and signal
            hist = macd - signal
            
            logger.info(f"MACD calculation:")
            logger.info(f"Last 5 MACD values:\n{macd.tail()}")
            logger.info(f"Last 5 Signal values:\n{signal.tail()}")
            logger.info(f"Last 5 Histogram values:\n{hist.tail()}")
            
            return macd, signal, hist
        except Exception as e:
            logger.error(f"Error calculating MACD: {str(e)}")
            raise

    def calculate_moving_averages(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calculate moving averages"""
        try:
            return {
                'MA20': ta.trend.SMAIndicator(df['close'], window=20).sma_indicator(),
                'MA50': ta.trend.SMAIndicator(df['close'], window=50).sma_indicator(),
                'MA200': ta.trend.SMAIndicator(df['close'], window=200).sma_indicator()
            }
        except Exception as e:
            logger.error(f"Error calculating moving averages: {str(e)}")
            raise

    def check_rsi_criteria(self, df: pd.DataFrame, criteria: Dict) -> bool:
        """Check if stock meets RSI criteria"""
        try:
            # Calculate RSI
            rsi = self.calculate_rsi(df)
            
            # Get the latest valid RSI value
            latest_rsi = rsi.iloc[-1]
            
            # Check if RSI is within specified range
            if 'below' in criteria:
                threshold = float(criteria['below'])
                if not (0 <= threshold <= 100):
                    logger.warning(f"Invalid RSI threshold: {threshold}")
                    return False
                return latest_rsi < threshold
                
            if 'above' in criteria:
                threshold = float(criteria['above'])
                if not (0 <= threshold <= 100):
                    logger.warning(f"Invalid RSI threshold: {threshold}")
                    return False
                return latest_rsi > threshold
                
            return True
            
        except Exception as e:
            logger.error(f"Error checking RSI criteria: {str(e)}")
            return False

    def check_macd_criteria(self, df: pd.DataFrame, criteria: dict) -> bool:
        """Check if stock meets MACD criteria"""
        try:
            if 'signal' not in criteria:
                return True
                
            # Calculate MACD
            macd, signal, hist = self.calculate_macd(df)
            
            # Get the last few values to check for crossover
            last_values = 10  # Look at more recent values
            recent_macd = macd.tail(last_values)
            recent_signal = signal.tail(last_values)
            recent_hist = hist.tail(last_values)
            
            # Log values for debugging
            logger.info(f"Checking MACD crossover:")
            logger.info(f"Recent MACD: {recent_macd.values}")
            logger.info(f"Recent Signal: {recent_signal.values}")
            logger.info(f"Recent Histogram: {recent_hist.values}")
            
            if criteria['signal'] == 'bullish':
                # Look for bullish crossover in recent values
                # MACD line crosses above signal line
                for i in range(1, len(recent_hist)):
                    # Crossover occurs when histogram changes from negative to positive
                    was_negative = recent_hist.iloc[i-1] < 0
                    is_positive = recent_hist.iloc[i] > 0
                    if was_negative and is_positive:
                        logger.info(f"Found bullish crossover at index {i}")
                        return True
                        
            elif criteria['signal'] == 'bearish':
                # Look for bearish crossover in recent values
                # MACD line crosses below signal line
                for i in range(1, len(recent_hist)):
                    # Crossover occurs when histogram changes from positive to negative
                    was_positive = recent_hist.iloc[i-1] > 0
                    is_negative = recent_hist.iloc[i] < 0
                    if was_positive and is_negative:
                        logger.info(f"Found bearish crossover at index {i}")
                        return True
                
            return False
            
        except Exception as e:
            logger.error(f"Error checking MACD criteria: {str(e)}")
            return False

    def check_ma_criteria(self, df: pd.DataFrame, criteria: Dict) -> bool:
        """Check if stock meets Moving Average criteria"""
        try:
            mas = self.calculate_moving_averages(df)
            price = df['close'].iloc[-1]
            
            if criteria.get('criteria') == 'price_above_ma20':
                return price > mas['MA20'].iloc[-1]
            elif criteria.get('criteria') == 'ma20_above_ma50':
                return mas['MA20'].iloc[-1] > mas['MA50'].iloc[-1]
            return False
        except Exception as e:
            logger.error(f"Error checking MA criteria: {str(e)}")
            raise

    def screen_stocks(self, criteria: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Screen stocks based on technical indicator criteria"""
        matching_stocks = []
        try:
            stocks = self.get_all_stocks()
            logger.info(f"Screening {len(stocks)} stocks with criteria: {criteria}")

            for symbol in stocks:
                try:
                    df = self.get_stock_data(symbol)
                    if len(df) < 200:  # Need enough data for indicators
                        logger.warning(f"Not enough data for {symbol}, skipping")
                        continue

                    meets_criteria = True

                    # Check each indicator's criteria
                    for indicator, indicator_criteria in criteria.items():
                        if indicator == 'RSI':
                            meets_criteria &= self.check_rsi_criteria(df, indicator_criteria)
                        elif indicator == 'MACD':
                            meets_criteria &= self.check_macd_criteria(df, indicator_criteria)
                        elif indicator == 'MA':
                            meets_criteria &= self.check_ma_criteria(df, indicator_criteria)

                    if meets_criteria:
                        # Get latest values for the matching stock
                        latest_values = {
                            'symbol': symbol,
                            'price': float(df['close'].iloc[-1]),
                            'date': df['date'].iloc[-1].strftime('%Y-%m-%d'),
                            'indicators': {}
                        }
                        
                        # Add indicator values
                        if 'RSI' in criteria:
                            latest_values['indicators']['RSI'] = float(self.calculate_rsi(df).iloc[-1])
                        if 'MACD' in criteria:
                            macd, signal, _ = self.calculate_macd(df)
                            latest_values['indicators']['MACD'] = {
                                'macd': float(macd.iloc[-1]),
                                'signal': float(signal.iloc[-1])
                            }
                        if 'MA' in criteria:
                            mas = self.calculate_moving_averages(df)
                            latest_values['indicators']['MA'] = {
                                k: float(v.iloc[-1]) for k, v in mas.items()
                            }
                        
                        matching_stocks.append(latest_values)
                        logger.info(f"Stock {symbol} matches criteria")
                except Exception as e:
                    logger.error(f"Error processing {symbol}: {str(e)}")
                    continue

            logger.info(f"Found {len(matching_stocks)} matching stocks")
            return matching_stocks
        except Exception as e:
            logger.error(f"Error in screen_stocks: {str(e)}")
            raise

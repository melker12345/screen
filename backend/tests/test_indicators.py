import pytest
import pandas as pd
import numpy as np
from scripts.indicators import TechnicalIndicators
from datetime import datetime, timedelta

@pytest.fixture
def sample_data():
    """Create sample stock data for testing"""
    dates = pd.date_range(start='2024-01-01', end='2025-01-24', freq='D')
    df = pd.DataFrame({
        'date': dates,
        'open': np.random.uniform(100, 110, len(dates)),
        'high': np.random.uniform(110, 120, len(dates)),
        'low': np.random.uniform(90, 100, len(dates)),
        'close': np.random.uniform(100, 110, len(dates)),
        'volume': np.random.randint(1000, 10000, len(dates))
    })
    return df

@pytest.fixture
def indicators():
    """Create TechnicalIndicators instance"""
    return TechnicalIndicators()

def test_rsi_calculation(indicators, sample_data):
    """Test RSI calculation"""
    rsi = indicators.calculate_rsi(sample_data)
    
    # RSI should be between 0 and 100
    assert rsi.min() >= 0
    assert rsi.max() <= 100
    
    # RSI should not have NaN values after period
    assert rsi.iloc[14:].isna().sum() == 0
    
    # Test with known values
    # Create a simple uptrend
    df_up = pd.DataFrame({
        'close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        'date': pd.date_range(start='2024-01-01', periods=11)
    })
    rsi_up = indicators.calculate_rsi(df_up, period=2)
    assert rsi_up.iloc[-1] > 70  # Should be overbought in uptrend
    
    # Create a simple downtrend
    df_down = pd.DataFrame({
        'close': [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10],
        'date': pd.date_range(start='2024-01-01', periods=11)
    })
    rsi_down = indicators.calculate_rsi(df_down, period=2)
    assert rsi_down.iloc[-1] < 30  # Should be oversold in downtrend

def test_macd_calculation(indicators, sample_data):
    """Test MACD calculation"""
    macd, signal, hist = indicators.calculate_macd(sample_data)
    
    # MACD components should not be None
    assert macd is not None
    assert signal is not None
    assert hist is not None
    
    # Histogram should be the difference between MACD and signal
    np.testing.assert_array_almost_equal(hist, macd - signal)
    
    # Test with data that should create a clear bullish crossover
    # Create price data that will force a MACD crossover
    prices = ([10] * 20 +  # Stable period
              [9, 8, 7, 6, 5] * 4 +  # Downtrend
              [6, 7, 8, 9, 10] * 4)  # Uptrend
    
    df_cross = pd.DataFrame({
        'close': prices,
        'date': pd.date_range(start='2024-01-01', periods=len(prices))
    })
    
    # Calculate MACD for crossover test
    macd, signal, hist = indicators.calculate_macd(df_cross)
    
    # Log MACD values for debugging
    print("\nMACD values for crossover test:")
    print(f"MACD:\n{macd.tail(10)}")
    print(f"Signal:\n{signal.tail(10)}")
    print(f"Histogram:\n{hist.tail(10)}")
    
    # Test both bullish and bearish scenarios
    bullish = indicators.check_macd_criteria(df_cross, {'signal': 'bullish'})
    bearish = indicators.check_macd_criteria(df_cross, {'signal': 'bearish'})
    
    # At least one type of crossover should be detected
    assert bullish or bearish, "Neither bullish nor bearish crossover detected"

def test_moving_averages(indicators, sample_data):
    """Test moving averages calculation"""
    mas = indicators.calculate_moving_averages(sample_data)
    
    # Should have all required MAs
    assert 'MA20' in mas
    assert 'MA50' in mas
    assert 'MA200' in mas
    
    # MAs should have correct lengths
    assert len(mas['MA20']) == len(sample_data)
    assert len(mas['MA50']) == len(sample_data)
    assert len(mas['MA200']) == len(sample_data)
    
    # Test with simple data
    df_simple = pd.DataFrame({
        'close': [1, 2, 3, 4, 5] * 4,
        'date': pd.date_range(start='2024-01-01', periods=20)
    })
    mas_simple = indicators.calculate_moving_averages(df_simple)
    
    # MA20 should be 3 (average of 1,2,3,4,5 repeated)
    assert abs(mas_simple['MA20'].iloc[-1] - 3) < 0.0001

def test_stock_screening(indicators, sample_data):
    """Test stock screening functionality"""
    # Mock get_all_stocks and get_stock_data
    def mock_get_all_stocks(self):
        return ['TEST.ST']
    
    def mock_get_stock_data(self, symbol):
        return sample_data
    
    # Temporarily replace methods
    original_get_all = indicators.get_all_stocks
    original_get_data = indicators.get_stock_data
    indicators.get_all_stocks = lambda: ['TEST.ST']
    indicators.get_stock_data = lambda x: sample_data
    
    try:
        # Test RSI screening
        stocks_rsi = indicators.screen_stocks({'RSI': {'below': 70}})
        assert isinstance(stocks_rsi, list)
        if stocks_rsi:
            assert all(isinstance(s, dict) for s in stocks_rsi)
            assert all('RSI' in s['indicators'] for s in stocks_rsi)
        
        # Test MACD screening
        stocks_macd = indicators.screen_stocks({'MACD': {'signal': 'bullish'}})
        assert isinstance(stocks_macd, list)
        if stocks_macd:
            assert all('MACD' in s['indicators'] for s in stocks_macd)
        
        # Test MA screening
        stocks_ma = indicators.screen_stocks({'MA': {'criteria': 'price_above_ma20'}})
        assert isinstance(stocks_ma, list)
        if stocks_ma:
            assert all('MA' in s['indicators'] for s in stocks_ma)
    
    finally:
        # Restore original methods
        indicators.get_all_stocks = original_get_all
        indicators.get_stock_data = original_get_data

def test_data_consistency(indicators):
    """Test data retrieval and consistency"""
    # Get all stocks
    stocks = indicators.get_all_stocks()
    assert isinstance(stocks, list)
    assert len(stocks) > 0
    
    # Test data for first stock
    first_stock = stocks[0]
    df = indicators.get_stock_data(first_stock)
    
    # Check DataFrame structure
    assert isinstance(df, pd.DataFrame)
    assert all(col in df.columns for col in ['date', 'open', 'high', 'low', 'close', 'volume'])
    
    # Check data types
    assert pd.api.types.is_datetime64_any_dtype(df['date'])
    assert pd.api.types.is_float_dtype(df['close'])
    assert pd.api.types.is_float_dtype(df['high'])
    assert pd.api.types.is_float_dtype(df['low'])
    assert pd.api.types.is_float_dtype(df['open'])
    assert pd.api.types.is_integer_dtype(df['volume'])
    
    # Check data validity
    assert df['high'].max() >= df['close'].max()
    assert df['low'].min() <= df['close'].min()
    assert all(df['volume'] >= 0)

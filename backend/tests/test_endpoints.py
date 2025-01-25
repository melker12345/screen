import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

def test_get_stocks():
    """Test getting list of available stocks"""
    response = client.get("/api/stocks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_stock_data():
    """Test getting individual stock data"""
    # Get list of stocks first
    stocks_response = client.get("/api/stocks")
    stocks = stocks_response.json()
    
    # Test with first available stock
    first_stock = stocks[0]
    response = client.get(f"/api/stocks/{first_stock}")
    assert response.status_code == 200
    
    data = response.json()
    assert "symbol" in data
    assert "price" in data
    assert "date" in data
    assert "indicators" in data
    assert "RSI" in data["indicators"]
    assert "MACD" in data["indicators"]
    assert "MA" in data["indicators"]
    
    # Test with invalid stock
    response = client.get("/api/stocks/INVALID")
    assert response.status_code == 404

def test_analyze_stock():
    """Test stock analysis endpoint"""
    # Get list of stocks first
    stocks_response = client.get("/api/stocks")
    stocks = stocks_response.json()
    first_stock = stocks[0]
    
    # Test with all indicators
    payload = {
        "symbol": first_stock,
        "indicators": ["RSI", "MACD", "MA"]
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "symbol" in data
    assert "price" in data
    assert "date" in data
    assert "indicators" in data
    
    # Test with specific indicators
    payload = {
        "symbol": first_stock,
        "indicators": ["RSI"]
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "RSI" in data["indicators"]
    assert "MACD" not in data["indicators"]
    
    # Test with invalid stock
    payload = {
        "symbol": "INVALID",
        "indicators": ["RSI"]
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 404

def test_screen_stocks():
    """Test stock screening endpoint"""
    # Test RSI screening
    payload = {
        "below": 30  # RSI below 30
    }
    response = client.post("/api/screen", json=payload)
    assert response.status_code == 200
    assert "stocks" in response.json()
    
    # Test MACD screening
    payload = {
        "signal": "bullish"  # Bullish MACD crossover
    }
    response = client.post("/api/screen", json=payload)
    assert response.status_code == 200
    assert "stocks" in response.json()
    
    # Test show all stocks
    payload = {
        "show_all": True
    }
    response = client.post("/api/screen", json=payload)
    assert response.status_code == 200
    assert "stocks" in response.json()
    assert len(response.json()["stocks"]) > 0

def test_error_handling():
    """Test error handling"""
    # Test invalid stock symbol
    response = client.get("/api/stock/INVALID")
    assert response.status_code == 404
    
    # Test invalid RSI value
    payload = {
        "below": 150  # Invalid RSI value
    }
    response = client.post("/api/screen", json=payload)
    assert response.status_code == 200  # Should still return 200 but with no stocks
    assert response.json()["stocks"] == []
    
    # Test invalid MACD signal
    payload = {
        "signal": "invalid"  # Invalid MACD signal
    }
    response = client.post("/api/screen", json=payload)
    assert response.status_code == 200  # Should still return 200 but with no stocks
    assert response.json()["stocks"] == []

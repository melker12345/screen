from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Dict, Any
from models.schemas import StockResponse, IndicatorRequest, ScreenerRequest
from scripts.indicators import TechnicalIndicators
import logging
import yfinance as yf

logger = logging.getLogger(__name__)

router = APIRouter()
indicators = TechnicalIndicators()

@router.get("/stocks")
async def get_stocks():
    """Get list of available stocks"""
    try:
        # Get stocks from database
        indicators = TechnicalIndicators()
        stocks = indicators.get_all_stocks()
        return stocks
    except Exception as e:
        logger.error(f"Error getting stocks: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting stocks")

@router.get("/stocks/{symbol}", response_model=StockResponse)
async def get_stock_data(symbol: str):
    """Get stock data with technical indicators"""
    try:
        # Get stock data using yfinance
        stock = yf.Ticker(symbol)
        df = stock.history(period="1y")
        
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for stock {symbol}")
            
        # Rename columns to lowercase for consistency
        df.columns = df.columns.str.lower()
        
        # Initialize indicators
        indicators = TechnicalIndicators()
        
        # Calculate indicators
        rsi = indicators.calculate_rsi(df)
        macd, signal, _ = indicators.calculate_macd(df)
        mas = indicators.calculate_moving_averages(df)
        
        # Create response
        response = {
            "symbol": symbol,
            "price": float(df['close'].iloc[-1]),
            "date": df.index[-1].strftime('%Y-%m-%d'),
            "indicators": {
                "RSI": float(rsi.iloc[-1]),
                "MACD": {
                    "macd": float(macd.iloc[-1]),
                    "signal": float(signal.iloc[-1])
                },
                "MA": {
                    k: float(v.iloc[-1]) for k, v in mas.items()
                }
            }
        }
        return response
        
    except Exception as e:
        logger.error(f"Error getting stock data for {symbol}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error getting data for stock {symbol}")

@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_stock(request: IndicatorRequest):
    """Analyze a stock with specified indicators"""
    try:
        # Get stock data using yfinance
        stock = yf.Ticker(request.symbol)
        df = stock.history(period="1y")
        
        if df.empty:
            logger.warning(f"No data found for stock {request.symbol}")
            raise HTTPException(status_code=404, detail=f"No data found for stock {request.symbol}")
            
        # Rename columns to lowercase for consistency
        df.columns = df.columns.str.lower()
        
        # Initialize indicators
        indicators = TechnicalIndicators()
            
        # Calculate requested indicators
        response = {
            "symbol": request.symbol,
            "price": float(df['close'].iloc[-1]),
            "date": df.index[-1].strftime('%Y-%m-%d'),
            "indicators": {}
        }
        
        if "RSI" in request.indicators:
            rsi = indicators.calculate_rsi(df)
            response["indicators"]["RSI"] = float(rsi.iloc[-1])
            
        if "MACD" in request.indicators:
            macd, signal, hist = indicators.calculate_macd(df)
            response["indicators"]["MACD"] = {
                "macd": float(macd.iloc[-1]),
                "signal": float(signal.iloc[-1]),
                "histogram": float(hist.iloc[-1])
            }
            
        if "MA" in request.indicators:
            mas = indicators.calculate_moving_averages(df)
            response["indicators"]["MA"] = {
                k: float(v.iloc[-1]) for k, v in mas.items()
            }
            
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing stock {request.symbol}: {str(e)}")
        if "No data found" in str(e) or "404" in str(e):
            raise HTTPException(status_code=404, detail=f"No data found for stock {request.symbol}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/screen")
async def screen_stocks(criteria: Dict = Body(...)):
    """Screen stocks based on technical indicators"""
    try:
        # Initialize indicators
        indicators = TechnicalIndicators()
        
        # If no criteria or show_all is true, return all stocks
        if not criteria or criteria.get('show_all', False):
            stocks = indicators.get_all_stocks()
            return {"stocks": stocks}
            
        # Get all stocks from database
        stocks = indicators.get_all_stocks()
        
        # Screen stocks based on criteria
        screened_stocks = []
        for symbol in stocks:
            try:
                # Get stock data from database
                df = indicators.get_stock_data(symbol)
                
                if df.empty:
                    continue
                    
                # Check if stock meets all criteria
                meets_criteria = True
                
                # Check RSI criteria
                if 'RSI' in criteria:
                    rsi = indicators.calculate_rsi(df)
                    if 'below' in criteria['RSI']:
                        meets_criteria = meets_criteria and (rsi.iloc[-1] < criteria['RSI']['below'])
                    if 'above' in criteria['RSI']:
                        meets_criteria = meets_criteria and (rsi.iloc[-1] > criteria['RSI']['above'])
                
                # Check MACD criteria
                if 'MACD' in criteria:
                    macd, signal, hist = indicators.calculate_macd(df)
                    if criteria['MACD'].get('signal') == 'bullish':
                        meets_criteria = meets_criteria and (hist.iloc[-1] > 0 and hist.iloc[-2] <= 0)
                    elif criteria['MACD'].get('signal') == 'bearish':
                        meets_criteria = meets_criteria and (hist.iloc[-1] < 0 and hist.iloc[-2] >= 0)
                
                # Check MA criteria
                if 'MA' in criteria:
                    mas = indicators.calculate_moving_averages(df)
                    for ma_type, ma_criteria in criteria['MA'].items():
                        if ma_type in mas:
                            if ma_criteria == 'price_above':
                                meets_criteria = meets_criteria and (df['close'].iloc[-1] > mas[ma_type].iloc[-1])
                            elif ma_criteria == 'price_below':
                                meets_criteria = meets_criteria and (df['close'].iloc[-1] < mas[ma_type].iloc[-1])
                
                if meets_criteria:
                    screened_stocks.append(symbol)
                    
            except Exception as e:
                logger.error(f"Error screening stock {symbol}: {str(e)}")
                continue
                
        return {"stocks": screened_stocks}
        
    except Exception as e:
        logger.error(f"Error in screen_stocks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

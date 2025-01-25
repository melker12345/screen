from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class MACDIndicator(BaseModel):
    macd: float
    signal: float
    histogram: Optional[float] = None

class Indicators(BaseModel):
    RSI: Optional[float] = None
    MACD: Optional[MACDIndicator] = None
    MA: Optional[Dict[str, float]] = None

class StockResponse(BaseModel):
    symbol: str
    price: float
    date: str
    indicators: Indicators

class IndicatorRequest(BaseModel):
    symbol: str
    indicators: List[str]

class ScreenerRequest(BaseModel):
    show_all: Optional[bool] = False
    criteria: Optional[Dict[str, Any]] = None

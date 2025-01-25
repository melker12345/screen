# Swedish Stock Screener

A robust system for analyzing Swedish stocks using technical indicators. Features include automatic data fetching, technical analysis, and a web interface for visualization.

## Project Structure

```
stock-screener/
├── backend/
│   ├── api/
│   │   ├── main.py            # FastAPI application
│   │   ├── endpoints.py       # API endpoints
│   ├── data/
│   │   ├── tickers.csv        # List of Swedish stock tickers
│   │   ├── stock_data.db      # SQLite database
│   ├── models/
│   │   ├── schemas.py         # Pydantic models
│   ├── scripts/
│   │   ├── database.py        # Database operations
│   │   ├── indicators.py      # Technical indicators
│   │   ├── fetch_nasdaq_tickers.py  # Ticker fetching
│   ├── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StockList.js
│   │   │   ├── IndicatorSelector.js
│   │   │   ├── Chart.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   ├── App.js
│   │   ├── App.css
└── .gitignore

## Features

- Automatic fetching of stock data using yfinance
- Technical indicators (RSI, MACD, Moving Averages)
- Interactive charts with TradingView
- Stock screening based on technical indicators
- Modern React frontend with real-time updates

## Setup Instructions

### Backend Setup

1. Set up the Python virtual environment:
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   uvicorn api.main:app --reload
   ```

### Frontend Setup

1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Available Indicators

- Relative Strength Index (RSI)
- Moving Average Convergence Divergence (MACD)
- Simple Moving Averages (20, 50, 200 days)

## Adding New Indicators

To add new indicators:
1. Add the indicator calculation in `backend/scripts/indicators.py`
2. Update the API endpoints in `backend/api/endpoints.py`
3. Add the indicator option in the frontend selector



$body = @{indicators=@{RSI=@{below=40}}} | ConvertTo-Json; Invoke-RestMethod -Uri http://localhost:8000/api/screen -Method Post -Body $body -ContentType 'application/json'
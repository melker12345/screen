import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Divider, 
  List, 
  ListItem, 
  ListItemText, 
  TextField,
  InputAdornment,
  Grid
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const Documentation = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const sections = [
    { id: 'features', title: 'Features' },
    { id: 'technical-indicators', title: 'Technical Indicators' },
    { id: 'how-to-use', title: 'How to Use the Screener' },
    { id: 'best-practices', title: 'Best Practices' },
    { id: 'technical-details', title: 'Technical Details' },
    { id: 'tips', title: 'Tips for Success' },
    { id: 'backend-architecture', title: 'Backend Architecture' },
    { id: 'frontend-architecture', title: 'Frontend Architecture' }
  ];

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <Grid container spacing={2}>
      {/* Left Navigation Sidebar */}
      <Grid item xs={12} md={3}>
        <Paper sx={{ p: 2, position: 'sticky', top: 16 }}>
          <TextField
            fullWidth
            size="small"
            placeholder="Search documentation..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            sx={{ mb: 2 }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
          <List component="nav" dense>
            {sections
              .filter(section => 
                section.title.toLowerCase().includes(searchQuery.toLowerCase())
              )
              .map((section) => (
                <ListItem
                  key={section.id}
                  button
                  onClick={() => scrollToSection(section.id)}
                  sx={{
                    borderRadius: 1,
                    '&:hover': {
                      backgroundColor: 'rgba(0, 0, 0, 0.04)',
                    }
                  }}
                >
                  <ListItemText primary={section.title} />
                </ListItem>
              ))}
          </List>
        </Paper>
      </Grid>

      {/* Main Content */}
      <Grid item xs={12} md={9}>
        <Paper sx={{ p: 3 }}>
          <Box>
            <Typography variant="h4" gutterBottom>
              Swedish Stock Screener Documentation
            </Typography>
            
            <Typography paragraph color="text.secondary">
              A powerful tool for screening Swedish stocks using technical indicators and real-time market data.
            </Typography>

            <Divider sx={{ my: 3 }} />

            <div id="features">
              <Typography variant="h5" gutterBottom>
                Features
              </Typography>
              <Typography paragraph>
                • Advanced stock screening based on technical indicators (RSI, MACD)<br />
                • Real-time data updates from reliable market sources<br />
                • Interactive stock cards with detailed information<br />
                • Historical price data visualization<br />
                • Customizable screening criteria<br />
                • Support for multiple technical indicators simultaneously
              </Typography>
            </div>

            <div id="technical-indicators">
              <Typography variant="h5" gutterBottom sx={{ mt: 3 }}>
                Technical Indicators
              </Typography>
              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                RSI (Relative Strength Index)
              </Typography>
              <Typography paragraph>
                RSI is a momentum oscillator that measures the speed and magnitude of recent price changes to evaluate overbought or oversold conditions.
              </Typography>
              <Typography paragraph>
                <strong>Interpretation:</strong><br />
                • Below 30: Stock is considered oversold, potential buying opportunity<br />
                • Above 70: Stock is considered overbought, potential selling opportunity<br />
                • 50 level: Used as a centerline for determining trend direction
              </Typography>
              <Typography paragraph>
                <strong>Calculation:</strong><br />
                RSI = 100 - (100 / (1 + RS))<br />
                where RS = Average Gain / Average Loss
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                MACD (Moving Average Convergence Divergence)
              </Typography>
              <Typography paragraph>
                MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a stock's price.
              </Typography>
              <Typography paragraph>
                <strong>Components:</strong><br />
                • MACD Line: Difference between 12-day and 26-day EMA<br />
                • Signal Line: 9-day EMA of MACD Line<br />
                • MACD Histogram: MACD Line minus Signal Line
              </Typography>
              <Typography paragraph>
                <strong>Signal Interpretations:</strong><br />
                • Bullish Crossover: MACD line crosses above signal line<br />
                • Bearish Crossover: MACD line crosses below signal line<br />
                • Divergence: When price and MACD move in opposite directions (strong signal)<br />
                • Centerline Crossover: MACD crossing above/below zero line
              </Typography>
            </div>

            <div id="how-to-use">
              <Typography variant="h5" gutterBottom sx={{ mt: 3 }}>
                How to Use the Screener
              </Typography>
              <Typography paragraph>
                <strong>1. Select Screening Criteria:</strong><br />
                • Use the RSI dropdown to screen for oversold or overbought conditions<br />
                • Use the MACD dropdown to identify trend changes and momentum<br />
                • Combine multiple indicators for more refined results
              </Typography>
              <Typography paragraph>
                <strong>2. View Results:</strong><br />
                • Matching stocks are displayed in an interactive grid<br />
                • Each card shows the stock symbol and basic information<br />
                • Click on a stock card to view detailed information
              </Typography>
              <Typography paragraph>
                <strong>3. Analyze Stock Details:</strong><br />
                • Current price and date<br />
                • RSI value with color coding (green for oversold, red for overbought)<br />
                • MACD values including signal line and histogram<br />
                • Historical price trends and indicators
              </Typography>
            </div>

            <div id="best-practices">
              <Typography variant="h5" gutterBottom sx={{ mt: 3 }}>
                Best Practices
              </Typography>
              <Typography paragraph>
                <strong>For Day Trading:</strong><br />
                • Focus on RSI extremes (below 30 or above 70)<br />
                • Look for MACD crossovers near the zero line<br />
                • Combine with volume analysis for confirmation
              </Typography>
              <Typography paragraph>
                <strong>For Swing Trading:</strong><br />
                • Use RSI divergence with price<br />
                • Wait for MACD histogram to show momentum shift<br />
                • Consider multiple timeframes for confirmation
              </Typography>
              <Typography paragraph>
                <strong>For Position Trading:</strong><br />
                • Focus on longer-term MACD trends<br />
                • Use RSI to identify major market reversals<br />
                • Combine with fundamental analysis
              </Typography>
            </div>

            <div id="technical-details">
              <Typography variant="h5" gutterBottom sx={{ mt: 3 }}>
                Technical Details
              </Typography>
              <Typography paragraph>
                <strong>Data Updates:</strong><br />
                • Stock prices are updated every trading day<br />
                • Technical indicators are calculated in real-time<br />
                • Historical data is maintained for accurate calculations
              </Typography>
              <Typography paragraph>
                <strong>Calculation Periods:</strong><br />
                • RSI: 14-period standard calculation<br />
                • MACD: 12-26-9 standard settings<br />
                • All calculations use closing prices
              </Typography>
            </div>

            <div id="tips">
              <Typography variant="h5" gutterBottom sx={{ mt: 3 }}>
                Tips for Success
              </Typography>
              <Typography paragraph>
                1. Don't rely on a single indicator - combine multiple signals<br />
                2. Always confirm signals with price action<br />
                3. Consider market conditions and sector trends<br />
                4. Use the "Show All Stocks" feature to analyze the broader market<br />
                5. Monitor indicator divergences for potential trend reversals<br />
                6. Keep track of your screening results and success rate
              </Typography>
            </div>

            <div id="backend-architecture">
              <Typography variant="h5" gutterBottom sx={{ mt: 3 }}>
                Backend Architecture
              </Typography>
              <Typography paragraph>
                The backend is built with FastAPI, providing a high-performance REST API for stock screening. It uses SQLite for data storage and pandas for efficient data processing and technical analysis.
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Project Structure
              </Typography>
              <Typography component="div" sx={{ mb: 2 }}>
                <pre style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px', overflowX: 'auto' }}>
{`backend/
├── main.py              # FastAPI application entry point
├── database.py          # Database connection and models
├── routers/
│   ├── stocks.py        # Stock-related endpoints
│   └── indicators.py    # Technical indicator calculations
├── models/
│   ├── stock.py         # Pydantic models for requests/responses
│   └── indicator.py     # Technical indicator models
└── services/
    ├── stock_service.py # Business logic for stocks
    └── data_service.py  # Data fetching and processing`}
                </pre>
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                API Endpoints
              </Typography>
              <Typography paragraph>
                <strong>1. Stock Screening:</strong>
              </Typography>
              <Typography component="div" sx={{ mb: 2 }}>
                <pre style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px', overflowX: 'auto' }}>
{`# Screen stocks based on technical indicators
POST /api/screen
{
  "indicators": {
    "rsi": { 
      "below": 30,      # RSI below 30 (oversold)
      "above": 70       # RSI above 70 (overbought)
    },
    "macd": {
      "crossover": "bullish",  # MACD line crosses above signal
      "divergence": "bearish"  # Price up, MACD down
    }
  },
  "filters": {
    "min_volume": 100000,      # Minimum trading volume
    "price_range": {
      "min": 10,
      "max": 100
    }
  }
}`}
                </pre>
              </Typography>

              <Typography paragraph>
                <strong>2. Stock Data:</strong>
              </Typography>
              <Typography component="div" sx={{ mb: 2 }}>
                <pre style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px', overflowX: 'auto' }}>
{`# Get historical data for a stock
GET /api/stocks/{symbol}/history
?start_date=2024-01-01&end_date=2024-01-26

# Get real-time stock updates
GET /api/stocks/updates
?symbols=["AAPL","MSFT"]

# Get technical indicators for a stock
GET /api/stocks/{symbol}/indicators
?indicators=["rsi","macd"]`}
                </pre>
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Database Schema
              </Typography>
              <Typography component="div" sx={{ mb: 2 }}>
                <pre style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px', overflowX: 'auto' }}>
{`# Main stock information
CREATE TABLE stocks (
    symbol TEXT PRIMARY KEY,
    name TEXT,
    sector TEXT,
    market_cap REAL,
    last_updated TIMESTAMP
);

# Historical price data
CREATE TABLE stock_prices (
    symbol TEXT,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    adjusted_close REAL,
    PRIMARY KEY (symbol, date),
    FOREIGN KEY (symbol) REFERENCES stocks(symbol)
);

# Technical indicators cache
CREATE TABLE indicator_values (
    symbol TEXT,
    date TEXT,
    indicator TEXT,
    value REAL,
    parameters TEXT,
    PRIMARY KEY (symbol, date, indicator, parameters),
    FOREIGN KEY (symbol) REFERENCES stocks(symbol)
);`}
                </pre>
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Technical Indicators Implementation
              </Typography>
              <Typography paragraph>
                <strong>1. RSI Calculation:</strong>
              </Typography>
              <Typography component="div" sx={{ mb: 2 }}>
                <pre style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px', overflowX: 'auto' }}>
{`def calculate_rsi(data: pd.DataFrame, periods: int = 14) -> pd.Series:
    # Calculate price changes
    delta = data['close'].diff()
    
    # Separate gains and losses
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    
    # Calculate RS and RSI
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi`}
                </pre>
              </Typography>

              <Typography paragraph>
                <strong>2. MACD Calculation:</strong>
              </Typography>
              <Typography component="div" sx={{ mb: 2 }}>
                <pre style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px', overflowX: 'auto' }}>
{`def calculate_macd(data: pd.DataFrame, 
                  fast_period: int = 12,
                  slow_period: int = 26,
                  signal_period: int = 9) -> tuple:
    # Calculate EMAs
    fast_ema = data['close'].ewm(span=fast_period).mean()
    slow_ema = data['close'].ewm(span=slow_period).mean()
    
    # Calculate MACD line
    macd_line = fast_ema - slow_ema
    
    # Calculate signal line
    signal_line = macd_line.ewm(span=signal_period).mean()
    
    # Calculate histogram
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram`}
                </pre>
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Data Processing Pipeline
              </Typography>
              <Typography paragraph>
                <strong>1. Data Ingestion:</strong>
                <br />• Daily updates from market data providers
                <br />• Real-time price updates during market hours
                <br />• Automatic data validation and cleaning
              </Typography>
              
              <Typography paragraph>
                <strong>2. Technical Analysis:</strong>
                <br />• Indicators calculated in real-time for screening
                <br />• Results cached in indicator_values table
                <br />• Automatic recalculation on new data
              </Typography>

              <Typography paragraph>
                <strong>3. Performance Optimization:</strong>
                <br />• Database indexing on frequently queried columns
                <br />• Caching of commonly requested data
                <br />• Batch processing for indicator calculations
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Error Handling
              </Typography>
              <Typography component="div" sx={{ mb: 2 }}>
                <pre style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px', overflowX: 'auto' }}>
{`# Example error responses
{
  "error": "InvalidIndicator",
  "message": "Invalid indicator parameters",
  "details": {
    "indicator": "rsi",
    "invalid_params": ["period"]
  }
}

{
  "error": "StockNotFound",
  "message": "Stock symbol not found",
  "details": {
    "symbol": "INVALID"
  }
}`}
                </pre>
              </Typography>
            </div>

            <div id="frontend-architecture">
              <Typography variant="h5" gutterBottom sx={{ mt: 3 }}>
                Frontend Architecture
              </Typography>
              <Typography paragraph>
                The frontend is built with React and Material-UI, implementing a component-based architecture.
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Component Structure
              </Typography>
              <Typography component="div" sx={{ mb: 2 }}>
                <pre style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px', overflowX: 'auto' }}>
{`src/
├── components/
│   ├── IndicatorSelector.js  # Handles indicator selection
│   ├── StockList.js         # Displays filtered stocks
│   └── Documentation.js      # This documentation
├── App.js                    # Main application component
└── index.js                  # Application entry point`}
                </pre>
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                State Management Example
              </Typography>
              <Typography component="div" sx={{ mb: 2 }}>
                <pre style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px', overflowX: 'auto' }}>
{`// App.js - Main State Management
const [selectedIndicators, setSelectedIndicators] = useState({});
const [matchingStocks, setMatchingStocks] = useState([]);

const handleIndicatorSelect = (indicators) => {
  setSelectedIndicators(indicators);
  screenStocks(indicators);
};

// API Call Example
const screenStocks = async (indicators) => {
  const response = await fetch('http://localhost:8000/api/screen', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ indicators })
  });
  const data = await response.json();
  setMatchingStocks(data.stocks);
};`}
                </pre>
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Component Communication
              </Typography>
              <Typography component="div" sx={{ mb: 2 }}>
                <pre style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px', overflowX: 'auto' }}>
{`// IndicatorSelector.js
const IndicatorSelector = ({ onSelectIndicators }) => {
  const [rsiValue, setRsiValue] = useState("");
  
  const handleRSIChange = (value) => {
    setRsiValue(value);
    onSelectIndicators({
      rsi: { below: parseInt(value) }
    });
  };
  
  return (
    <Select value={rsiValue} onChange={(e) => handleRSIChange(e.target.value)}>
      <MenuItem value={30}>RSI Below 30</MenuItem>
      <MenuItem value={70}>RSI Above 70</MenuItem>
    </Select>
  );
};`}
                </pre>
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Real-time Updates
              </Typography>
              <Typography component="div" sx={{ mb: 2 }}>
                <pre style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px', overflowX: 'auto' }}>
{`// StockList.js - Real-time Updates
useEffect(() => {
  const fetchStockUpdates = async () => {
    const response = await fetch('http://localhost:8000/api/stocks/updates');
    const updates = await response.json();
    setStocks(prevStocks => ({
      ...prevStocks,
      ...updates
    }));
  };

  const interval = setInterval(fetchStockUpdates, 5000);
  return () => clearInterval(interval);
}, []);`}
                </pre>
              </Typography>
            </div>
          </Box>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default Documentation;

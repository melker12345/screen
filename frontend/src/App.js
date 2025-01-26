import React, { useState } from 'react';
import { Box, AppBar, Toolbar, Typography, Button, Container } from '@mui/material';
import IndicatorSelector from './components/IndicatorSelector';
import StockList from './components/StockList';
import Documentation from './components/Documentation';

function App() {
  const [selectedIndicators, setSelectedIndicators] = useState({});
  const [matchingStocks, setMatchingStocks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentView, setCurrentView] = useState('screener'); // 'screener' or 'docs'

  const indicatorOptions = {
    RSI: {
      name: 'Relative Strength Index (RSI)',
      criteria: [
        { value: 'below_30', label: 'Below 30 (Oversold)', settings: { below: 30 } },
        { value: 'below_20', label: 'Below 20 (Extremely Oversold)', settings: { below: 20 } }
      ]
    },
    MACD: {
      name: 'MACD',
      criteria: [
        { value: 'bullish_cross', label: 'Bullish Cross', settings: { signal: 'bullish' } },
        { value: 'bearish_cross', label: 'Bearish Cross', settings: { signal: 'bearish' } }
      ]
    },
    MA: {
      name: 'Moving Averages',
      criteria: [
        { value: 'price_above_ma20', label: 'Price Above MA20', settings: { criteria: 'price_above_ma20' } },
        { value: 'ma20_above_ma50', label: 'MA20 Above MA50', settings: { criteria: 'ma20_above_ma50' } }
      ]
    }
  };

  const handleIndicatorSelect = (indicators) => {
    setSelectedIndicators(indicators);
  };

  const screenStocks = async () => {
    if (Object.keys(selectedIndicators).length === 0) {
      alert('Please select at least one indicator');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/screen', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          indicators: selectedIndicators
        }),
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      setMatchingStocks(data.stocks || []);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to screen stocks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Swedish Stock Screener
          </Typography>
          <Button 
            color="inherit" 
            onClick={() => setCurrentView('screener')}
            sx={{ mr: 2 }}
          >
            Screener
          </Button>
          <Button 
            color="inherit" 
            onClick={() => setCurrentView('docs')}
          >
            Documentation
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4 }}>
        {currentView === 'screener' ? (
          <>
            <IndicatorSelector
              options={indicatorOptions}
              onSelectIndicators={handleIndicatorSelect}
              onScreenStocks={screenStocks}
              loading={loading}
            />
            <StockList
              stocks={matchingStocks}
              loading={loading}
              selectedIndicators={selectedIndicators}
            />
          </>
        ) : (
          <Documentation />
        )}
      </Container>
    </Box>
  );
}

export default App;

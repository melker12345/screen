import React, { useState } from 'react';
import IndicatorSelector from './components/IndicatorSelector';
import StockList from './components/StockList';

function App() {
  const [selectedCriteria, setSelectedCriteria] = useState({});
  const [matchingStocks, setMatchingStocks] = useState([]);
  const [loading, setLoading] = useState(false);

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

  const handleIndicatorSelect = (criteria) => {
    setSelectedCriteria(criteria);
  };

  const screenStocks = async () => {
    if (Object.keys(selectedCriteria).length === 0) {
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
          indicators: selectedCriteria
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch matching stocks');
      }

      const data = await response.json();
      setMatchingStocks(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to screen stocks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-2xl font-bold text-indigo-600">Stock Screener</h1>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          <div className="bg-white overflow-hidden shadow-xl rounded-lg">
            <div className="p-6">
              <IndicatorSelector 
                onSelectIndicators={handleIndicatorSelect} 
                indicatorOptions={indicatorOptions}
                onScreenStocks={screenStocks}
                loading={loading}
              />
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow-xl rounded-lg">
            <div className="p-6">
              <StockList 
                selectedIndicators={selectedCriteria} 
                matchingStocks={matchingStocks} 
                loading={loading}
              />
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-white shadow-lg mt-12">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-500">
            Stock Screener {new Date().getFullYear()}
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

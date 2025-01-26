import React, { useState, useEffect } from 'react';
import { screenStocks, getStockData } from '../services/api';

const StockList = ({ selectedIndicators }) => {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedStock, setSelectedStock] = useState(null);
  const [stockDetails, setStockDetails] = useState(null);

  useEffect(() => {
    const fetchStocks = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await screenStocks(selectedIndicators);
        setStocks(response.stocks || []);
      } catch (err) {
        setError('Failed to fetch stocks: ' + err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStocks();
  }, [selectedIndicators]);

  const handleStockClick = async (symbol) => {
    try {
      setSelectedStock(symbol);
      const details = await getStockData(symbol);
      setStockDetails(details);
    } catch (err) {
      setError('Failed to fetch stock details: ' + err.message);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-16">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-indigo-500 border-t-transparent"></div>
          <p className="text-gray-500 text-sm font-medium">Loading stocks...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-red-50 p-4 mb-6">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
            <p className="mt-1 text-sm text-red-700">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-900">Matching Stocks</h2>
        <span className="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800">
          {stocks.length} stocks found
        </span>
      </div>
      
      {stocks.length === 0 ? (
        <div className="bg-white rounded-lg border-2 border-dashed border-gray-300 p-12">
          <div className="text-center">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M12 12h.01M12 12h.01M12 12h.01M12 12h.01M12 12h.01M12 12h.01M12 12h.01M12 12h.01M12 12h.01M12 12h.01" />
            </svg>
            <h3 className="mt-4 text-lg font-medium text-gray-900">No matching stocks</h3>
            <p className="mt-2 text-sm text-gray-500 max-w-sm mx-auto">
              Try adjusting your screening criteria or click "Show All Stocks" to see all available stocks.
            </p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {stocks.map((symbol) => (
            <div
              key={symbol}
              onClick={() => handleStockClick(symbol)}
              className={`
                relative rounded-lg border p-4 cursor-pointer
                transform transition-all duration-200 hover:scale-105
                ${selectedStock === symbol 
                  ? 'border-indigo-500 ring-2 ring-indigo-500 ring-opacity-50 bg-indigo-50' 
                  : 'border-gray-200 hover:border-indigo-400 hover:shadow-md'}
              `}
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">{symbol}</h3>
                <svg className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              
              {selectedStock === symbol && stockDetails && (
                <div className="mt-4 space-y-3">
                  <div className="flex justify-between items-center py-2 border-t border-gray-100">
                    <span className="text-sm font-medium text-gray-500">Price</span>
                    <span className="text-sm font-semibold text-gray-900">${stockDetails.price.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-t border-gray-100">
                    <span className="text-sm font-medium text-gray-500">Date</span>
                    <span className="text-sm text-gray-900">{stockDetails.date}</span>
                  </div>
                  {stockDetails.indicators && stockDetails.indicators.RSI && (
                    <div className="flex justify-between items-center py-2 border-t border-gray-100">
                      <span className="text-sm font-medium text-gray-500">RSI</span>
                      <span className={`text-sm font-semibold ${
                        stockDetails.indicators.RSI <= 30 ? 'text-green-600' : 
                        stockDetails.indicators.RSI >= 70 ? 'text-red-600' : 
                        'text-gray-900'
                      }`}>
                        {stockDetails.indicators.RSI.toFixed(2)}
                      </span>
                    </div>
                  )}
                  {stockDetails.indicators && stockDetails.indicators.MACD && (
                    <div className="space-y-2 py-2 border-t border-gray-100">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-medium text-gray-500">MACD</span>
                        <span className={`text-sm font-semibold ${
                          stockDetails.indicators.MACD.macd > 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {stockDetails.indicators.MACD.macd.toFixed(2)}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-medium text-gray-500">Signal</span>
                        <span className={`text-sm font-semibold ${
                          stockDetails.indicators.MACD.signal > 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {stockDetails.indicators.MACD.signal.toFixed(2)}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default StockList;

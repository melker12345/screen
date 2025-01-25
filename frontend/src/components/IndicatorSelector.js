import React, { useState } from 'react';

const IndicatorSelector = ({ onSelectIndicators }) => {
  const [showAll, setShowAll] = useState(false);
  const [selectedRSI, setSelectedRSI] = useState('');
  const [selectedMACD, setSelectedMACD] = useState('');

  const rsiOptions = [
    { value: 'below30', label: 'Below 30 (Oversold)', criteria: { RSI: { below: 30 } } },
    { value: 'above70', label: 'Above 70 (Overbought)', criteria: { RSI: { above: 70 } } }
  ];

  const macdOptions = [
    { value: 'bullish', label: 'Bullish Crossover', criteria: { MACD: { signal: 'bullish' } } },
    { value: 'bearish', label: 'Bearish Crossover', criteria: { MACD: { signal: 'bearish' } } }
  ];

  const handleShowAllChange = (event) => {
    const isChecked = event.target.checked;
    setShowAll(isChecked);
    if (isChecked) {
      setSelectedRSI('');
      setSelectedMACD('');
      onSelectIndicators({ show_all: true });
    } else {
      const criteria = {};
      if (selectedRSI) {
        const rsiOption = rsiOptions.find(option => option.value === selectedRSI);
        Object.assign(criteria, rsiOption.criteria);
      }
      if (selectedMACD) {
        const macdOption = macdOptions.find(option => option.value === selectedMACD);
        Object.assign(criteria, macdOption.criteria);
      }
      onSelectIndicators(criteria);
    }
  };

  const handleRSIChange = (event) => {
    const value = event.target.value;
    setSelectedRSI(value);
    if (!showAll) {
      if (value) {
        const selectedOption = rsiOptions.find(option => option.value === value);
        const criteria = { ...selectedOption.criteria };
        if (selectedMACD) {
          const macdOption = macdOptions.find(option => option.value === selectedMACD);
          Object.assign(criteria, macdOption.criteria);
        }
        onSelectIndicators(criteria);
      } else {
        if (selectedMACD) {
          const macdOption = macdOptions.find(option => option.value === selectedMACD);
          onSelectIndicators(macdOption.criteria);
        } else {
          onSelectIndicators({});
        }
      }
    }
  };

  const handleMACDChange = (event) => {
    const value = event.target.value;
    setSelectedMACD(value);
    if (!showAll) {
      if (value) {
        const selectedOption = macdOptions.find(option => option.value === value);
        const criteria = { ...selectedOption.criteria };
        if (selectedRSI) {
          const rsiOption = rsiOptions.find(option => option.value === selectedRSI);
          Object.assign(criteria, rsiOption.criteria);
        }
        onSelectIndicators(criteria);
      } else {
        if (selectedRSI) {
          const rsiOption = rsiOptions.find(option => option.value === selectedRSI);
          onSelectIndicators(rsiOption.criteria);
        } else {
          onSelectIndicators({});
        }
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-900">Screening Criteria</h2>
        <div className="flex items-center">
          <label className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500 cursor-pointer transition-colors duration-150">
            <input
              type="checkbox"
              checked={showAll}
              onChange={handleShowAllChange}
              className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded transition-colors duration-150"
            />
            <span className="ml-2">Show All Stocks</span>
          </label>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">
            RSI (Relative Strength Index)
          </label>
          <div className="relative">
            <select 
              value={selectedRSI} 
              onChange={handleRSIChange}
              disabled={showAll}
              className={`
                block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 rounded-md
                ${showAll ? 'bg-gray-100 cursor-not-allowed' : 'bg-white cursor-pointer'}
                transition-colors duration-150
              `}
            >
              <option value="">Select RSI Criteria</option>
              {rsiOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <div className="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
              <svg className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </div>
          </div>
          <p className="mt-1 text-sm text-gray-500">
            Select RSI threshold for oversold or overbought conditions
          </p>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">
            MACD (Moving Average Convergence Divergence)
          </label>
          <div className="relative">
            <select 
              value={selectedMACD}
              onChange={handleMACDChange}
              disabled={showAll}
              className={`
                block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 rounded-md
                ${showAll ? 'bg-gray-100 cursor-not-allowed' : 'bg-white cursor-pointer'}
                transition-colors duration-150
              `}
            >
              <option value="">Select MACD Criteria</option>
              {macdOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <div className="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
              <svg className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </div>
          </div>
          <p className="mt-1 text-sm text-gray-500">
            Choose MACD signal for trend direction
          </p>
        </div>
      </div>
    </div>
  );
};

export default IndicatorSelector;

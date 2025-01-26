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
    <div className="bg-white shadow rounded-lg p-6 mb-8">
      <div className="mb-6">
        <label className="inline-flex items-center">
          <input
            type="checkbox"
            className="form-checkbox h-5 w-5 text-indigo-600"
            checked={showAll}
            onChange={handleShowAllChange}
          />
          <span className="ml-2 text-gray-700">Show All Stocks</span>
        </label>
      </div>

      {!showAll && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              RSI (Relative Strength Index)
            </label>
            <select
              value={selectedRSI}
              onChange={handleRSIChange}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
              disabled={showAll}
            >
              <option value="">Select RSI condition</option>
              {rsiOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              MACD (Moving Average Convergence Divergence)
            </label>
            <select
              value={selectedMACD}
              onChange={handleMACDChange}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
              disabled={showAll}
            >
              <option value="">Select MACD condition</option>
              {macdOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      )}
    </div>
  );
};

export default IndicatorSelector;

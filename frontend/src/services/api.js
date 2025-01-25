const API_BASE_URL = 'http://localhost:8000/api';

export const getStocks = async () => {
  const response = await fetch(`${API_BASE_URL}/stocks`);
  if (!response.ok) {
    throw new Error('Failed to fetch stocks');
  }
  return response.json();
};

export const getStockData = async (symbol) => {
  const response = await fetch(`${API_BASE_URL}/stocks/${symbol}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch data for ${symbol}`);
  }
  return response.json();
};

export const analyzeStock = async (symbol, indicators) => {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ symbol, indicators }),
  });
  if (!response.ok) {
    throw new Error('Failed to analyze stock');
  }
  return response.json();
};

export const screenStocks = async (criteria) => {
  const response = await fetch(`${API_BASE_URL}/screen`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(criteria),
  });
  if (!response.ok) {
    throw new Error('Failed to screen stocks');
  }
  return response.json();
};

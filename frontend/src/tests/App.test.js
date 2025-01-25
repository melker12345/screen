import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../App';

// Mock the fetch API
global.fetch = jest.fn();

describe('Stock Screener App', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText(/Stock Screener/i)).toBeInTheDocument();
  });

  it('loads and displays stock list', async () => {
    // Mock the API response
    fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(['ERIC-B.ST', 'VOLV-B.ST']),
      })
    );

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('ERIC-B.ST')).toBeInTheDocument();
      expect(screen.getByText('VOLV-B.ST')).toBeInTheDocument();
    });
  });

  it('handles stock selection', async () => {
    // Mock the stocks API response
    fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(['ERIC-B.ST']),
      })
    );

    // Mock the stock data API response
    const mockStockData = {
      symbol: 'ERIC-B.ST',
      price: 85.20,
      date: '2025-01-24',
      indicators: {
        RSI: 33.21,
        MACD: {
          macd: 0.5,
          signal: 0.3
        },
        MA: {
          MA20: 84.5,
          MA50: 83.2,
          MA200: 82.1
        }
      }
    };

    fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockStockData),
      })
    );

    render(<App />);

    // Wait for stock list to load
    await waitFor(() => {
      expect(screen.getByText('ERIC-B.ST')).toBeInTheDocument();
    });

    // Click on the stock
    fireEvent.click(screen.getByText('ERIC-B.ST'));

    // Wait for stock details to load
    await waitFor(() => {
      expect(screen.getByText(/RSI: 33.21/i)).toBeInTheDocument();
      expect(screen.getByText(/Price: 85.20/i)).toBeInTheDocument();
    });
  });

  it('handles screening criteria', async () => {
    // Mock the screening API response
    const mockScreeningResults = [
      {
        symbol: 'ERIC-B.ST',
        price: 85.20,
        date: '2025-01-24',
        indicators: {
          RSI: 33.21,
          MACD: { macd: 0.5, signal: 0.3 },
          MA: { MA20: 84.5, MA50: 83.2, MA200: 82.1 }
        }
      }
    ];

    fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockScreeningResults),
      })
    );

    render(<App />);

    // Set RSI criteria
    const rsiInput = screen.getByLabelText(/RSI Below/i);
    fireEvent.change(rsiInput, { target: { value: '40' } });

    // Click screen button
    const screenButton = screen.getByText(/Screen Stocks/i);
    fireEvent.click(screenButton);

    // Wait for results
    await waitFor(() => {
      expect(screen.getByText('ERIC-B.ST')).toBeInTheDocument();
      expect(screen.getByText(/RSI: 33.21/i)).toBeInTheDocument();
    });
  });

  it('handles API errors gracefully', async () => {
    // Mock a failed API call
    fetch.mockImplementationOnce(() =>
      Promise.reject(new Error('API Error'))
    );

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/Error loading stocks/i)).toBeInTheDocument();
    });
  });

  it('displays loading states', async () => {
    // Mock a delayed API response
    fetch.mockImplementationOnce(() =>
      new Promise(resolve =>
        setTimeout(() =>
          resolve({
            ok: true,
            json: () => Promise.resolve(['ERIC-B.ST'])
          }), 100)
      )
    );

    render(<App />);

    expect(screen.getByText(/Loading/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('ERIC-B.ST')).toBeInTheDocument();
    });
  });
});

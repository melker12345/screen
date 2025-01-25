import React, { useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';

const Chart = ({ data, indicators }) => {
  const chartContainerRef = useRef();
  const chartRef = useRef();

  useEffect(() => {
    if (!data || data.length === 0) return;

    // Create chart
    const chart = createChart(chartContainerRef.current, {
      width: 800,
      height: 400,
      layout: {
        background: { color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: '#f0f0f0' },
        horzLines: { color: '#f0f0f0' },
      },
    });

    // Add candlestick series
    const candlestickSeries = chart.addCandlestickSeries();
    candlestickSeries.setData(data);

    // Add indicators if selected
    if (indicators.includes('MA')) {
      const ma20Series = chart.addLineSeries({ color: '#2962FF' });
      const ma50Series = chart.addLineSeries({ color: '#FF6D00' });
      // Add MA data...
    }

    // Store chart reference
    chartRef.current = chart;

    // Cleanup
    return () => {
      chart.remove();
    };
  }, [data, indicators]);

  return <div ref={chartContainerRef} />;
};

export default Chart;

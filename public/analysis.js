// DataAnalysis.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function DataAnalysis() {
  const [clickData, setClickData] = useState(null);
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('public/chart_data.json');
        setChartData(response.data);
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    };

    fetchData();
  }, []);

  const handlePlotClick = (data) => {
    if (data.points.length > 0) {
      const year = data.points[0].x;
      const chartDataItem = chartData.find(item => item.Year === year);
      setClickData(chartDataItem);
    }
  };

  const handleClearClickData = () => {
    setClickData(null);
  };

  return (
    <div className="DataAnalysis">
      <h1>Data Analysis</h1>
      {clickData && (
        <div className="clickData">
          <h2>{clickData.Year}</h2>
          <p>Average: {clickData.Average}</p>
          <p>Total Rated Movies: {clickData.Total}</p>
          <p>Top Movies:</p>
          <ul>
            {JSON.parse(clickData.Movies).map((movie, index) => (
              <li key={index}>{movie}</li>
            ))}
          </ul>
          <button onClick={handleClearClickData}>Clear</button>
        </div>
      )}
      <div className="plotContainer">
        {/* Include your Plotly chart component here */}
        {/* You can reuse the same Plot component and pass chartData as a prop */}
        <div className="back-button-container">
        <button onClick={() => window.location.href = '/'}>Back to Top 4</button>
      </div>
      </div>
    </div>
  );
}

export default DataAnalysis;

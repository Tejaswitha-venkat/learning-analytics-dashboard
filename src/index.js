import React from 'react';
import ReactDOM from 'react-dom/client';
import './frontend/styles/AnalyticsDashboard.css';
import AnalyticsDashboard from './frontend/components/AnalyticsDashboard';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AnalyticsDashboard />
  </React.StrictMode>
);
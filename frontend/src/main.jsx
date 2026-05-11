import React from 'react';
import ReactDOM from 'react-dom/client';
import DonorDashboard from '../../static/js/DonorDashboard.jsx';

const root = ReactDOM.createRoot(document.getElementById('donor-dashboard-root'));
root.render(
  <React.StrictMode>
    <DonorDashboard />
  </React.StrictMode>
);

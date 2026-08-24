import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';

function App() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Portfolio project</p>
          <h1>Real-Time CV Analytics</h1>
        </div>
        <button className="primary-btn">Start Camera</button>
      </header>

      <main className="dashboard-grid">
        <section className="panel camera-panel">
          <div className="panel-header">
            <h2>LIVE CAMERA</h2>
            <span className="status-online">● Online</span>
          </div>
          <div className="camera-placeholder">
            <div className="stat-overlay">
              <span>FPS: 28.4</span>
              <span>Objects: 14</span>
              <span>People: 9</span>
              <span>Cars: 5</span>
            </div>
          </div>
        </section>

        <aside className="panel metrics-panel">
          <h3>Live Metrics</h3>
          <div className="metric-list">
            <div><label>Entered</label><strong>124</strong></div>
            <div><label>Exited</label><strong>98</strong></div>
            <div><label>Occupancy</label><strong>26</strong></div>
            <div><label>Latency</label><strong>31ms</strong></div>
          </div>
        </aside>

        <section className="panel events-panel">
          <h3>Recent Events</h3>
          <ul>
            <li>Person #17 entered Entrance Region</li>
            <li>Car #5 exited</li>
            <li>Occupancy threshold exceeded</li>
          </ul>
        </section>

        <section className="panel analytics-panel">
          <h3>Analytics</h3>
          <div className="chart-grid">
            <div className="sparkline" />
            <div className="sparkline alt" />
          </div>
        </section>
      </main>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

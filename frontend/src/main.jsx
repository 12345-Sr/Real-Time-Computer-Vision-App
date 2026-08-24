import React, { useEffect, useRef, useState } from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';

function App() {
  const [running, setRunning] = useState(false);
  const [source, setSource] = useState('0');
  const [metrics, setMetrics] = useState({ fps: 0, latency_ms: 0 });
  const [detections, setDetections] = useState([]);
  const [error, setError] = useState('');
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const toggleCamera = async () => {
    if (running) {
      streamRef.current?.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
      setRunning(false);
      return;
    }
    try {
      if (source === '0') {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        streamRef.current = stream;
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      } else {
        const response = await fetch('/camera/start', {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ source }),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'Unable to open camera');
      }
      setError('');
      setRunning(true);
    } catch (cameraError) {
      setError(cameraError.message || 'Camera permission was denied or no camera is available');
    }
  };

  useEffect(() => {
    if (!running) return undefined;
    const interval = setInterval(async () => {
      const response = await fetch('/detections');
      const data = await response.json();
      setDetections(data.detections || []);
      setMetrics(data.metrics || { fps: 0, latency_ms: 0 });
    }, 1000);
    return () => clearInterval(interval);
  }, [running]);

  const people = detections.filter((item) => item.label === 'person').length;
  const distribution = detections.reduce((result, item) => ({ ...result, [item.label]: (result[item.label] || 0) + 1 }), {});
  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Portfolio project</p>
          <h1>Real-Time CV Analytics</h1>
        </div>
        <div className="controls">
          <input value={source} onChange={(event) => setSource(event.target.value)} aria-label="Camera source" />
          <button className="primary-btn" onClick={toggleCamera}>{running ? 'Stop Camera' : 'Start Camera'}</button>
        </div>
      </header>

      <main className="dashboard-grid">
        <section className="panel camera-panel">
          <div className="panel-header">
            <h2>LIVE CAMERA</h2>
            <span className={running ? 'status-online' : 'status-offline'}>{running ? '● Online' : '● Offline'}</span>
          </div>
          <div className="camera-placeholder">{source === '0' ? <video ref={videoRef} muted playsInline aria-label="Live webcam" /> : running ? <img src="/camera/stream" alt="Live camera stream" /> : <span>Start a camera source to begin</span>}
            <div className="stat-overlay"><span>FPS: {metrics.fps.toFixed(1)}</span><span>Objects: {detections.length}</span><span>People: {people}</span><span>Latency: {metrics.latency_ms.toFixed(0)}ms</span></div>
          </div>
          {error && <p className="error-message">{error}</p>}
        </section>

        <aside className="panel metrics-panel">
          <h3>Live Metrics</h3>
          <div className="metric-list">
            <div><label>Tracked</label><strong>{detections.length}</strong></div>
            <div><label>People</label><strong>{people}</strong></div>
            <div><label>Classes</label><strong>{Object.keys(distribution).length}</strong></div>
            <div><label>Latency</label><strong>{metrics.latency_ms.toFixed(0)}ms</strong></div>
          </div>
        </aside>

        <section className="panel events-panel">
          <h3>Recent Events</h3>
          <ul>
            {detections.length ? detections.slice(0, 5).map((item) => <li key={item.id}>{item.label} #{item.id} detected at {(item.confidence * 100).toFixed(0)}%</li>) : <li>No detections yet</li>}
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

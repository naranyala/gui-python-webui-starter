import React, { useEffect, useState } from 'react';
import { useService } from '../../hooks/useService.js';
import { SERVICE_KEYS } from '../../core/index.js';

export default function SystemPage() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);
  const [rustAnalysis, setRustAnalysis] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  const apiClient = useService(SERVICE_KEYS.API_CLIENT);

  const fetchStats = async () => {
    try {
      const data = await apiClient.get('/system');
      if (data.success) {
        setStats(data.data);
        setError(null);
      } else {
        setError(data.error);
      }
    } catch (e) {
      setError('Failed to fetch system stats');
    }
  };

  const runRustAnalysis = async () => {
    setAnalyzing(true);
    try {
      const data = await apiClient.get('/rust/analyze');
      if (data.success) {
        setRustAnalysis(data.data);
      }
    } catch (e) {
      console.error('Rust analysis failed', e);
    } finally {
      setAnalyzing(false);
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 2000);
    return () => clearInterval(interval);
  }, []);

  if (error) return <div className="error-message">{error}</div>;
  if (!stats) return <div className="loading-message">Loading system stats...</div>;

  return (
    <div className="system-container">
      <h2>System Monitor</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <span className="label">CPU Usage</span>
          <span className="value">{stats.cpu}%</span>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${stats.cpu}%` }}></div>
          </div>
        </div>

        <div className="stat-card">
          <span className="label">Memory Usage</span>
          <span className="value">
            {((stats.memory.used / stats.memory.total) * 100).toFixed(1)}%
          </span>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${(stats.memory.used / stats.memory.total) * 100}%` }}></div>
          </div>
          <span className="detail">{ (stats.memory.used / 1024**3).toFixed(2) } / { (stats.memory.total / 1024**3).toFixed(2) } GB</span>
        </div>

        <div className="stat-card">
          <span className="label">Disk Usage</span>
          <span className="value">
            {((stats.disk.used / stats.disk.total) * 100).toFixed(1)}%
          </span>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${(stats.disk.used / stats.disk.total) * 100}%` }}></div>
          </div>
          <span className="detail">{ (stats.disk.used / 1024**3).toFixed(2) } / { (stats.disk.total / 1024**3).toFixed(2) } GB</span>
        </div>
      </div>

      <div className="os-info">
        <h3>OS Information</h3>
        <ul>
          <li><strong>System:</strong> {stats.os.system}</li>
          <li><strong>Release:</strong> {stats.os.release}</li>
          <li><strong>Version:</strong> {stats.os.version}</li>
          <li><strong>Machine:</strong> {stats.os.machine}</li>
        </ul>
      </div>

      <div className="rust-demo" style={{ marginTop: '30px', padding: '20px', background: '#2d2d2d', borderRadius: '12px', border: '1px solid #444' }}>
        <h3>🦀 Rust Performance Demo</h3>
        <p style={{ color: '#9d9d9d', fontSize: '14px', marginBottom: '15px' }}>
          Use a Rust-written CLI to analyze the current project directory recursively.
        </p>
        <button 
          className="action-button" 
          onClick={runRustAnalysis} 
          disabled={analyzing}
          style={{ padding: '10px 20px', cursor: 'pointer', background: '#f97316', color: '#fff', border: 'none', borderRadius: '6px', fontWeight: '600' }}
        >
          {analyzing ? 'Analyzing...' : 'Analyze Project Folder'}
        </button>

        {rustAnalysis && (
          <div style={{ marginTop: '20px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div className="stat-card">
              <span className="label">Total Files</span>
              <span className="value">{rustAnalysis.total_files}</span>
            </div>
            <div className="stat-card">
              <span className="label">Total Size</span>
              <span className="value">{(rustAnalysis.total_size / 1024**2).toFixed(2)} MB</span>
            </div>
            <div style={{ gridColumn: 'span 2' }}>
              <span className="label" style={{ display: 'block', marginBottom: '10px' }}>Top 5 Largest Files:</span>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '13px', color: '#ccc' }}>
                {rustAnalysis.largest_files.map((f, i) => (
                  <li key={i} style={{ marginBottom: '5px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    <strong>{(f.size / 1024**2).toFixed(2)} MB</strong> - {f.path}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

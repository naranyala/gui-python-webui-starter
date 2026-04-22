import React, { useEffect, useState } from 'react';

export default function SystemPage() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/system');
      const data = await response.json();
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
    </div>
  );
}

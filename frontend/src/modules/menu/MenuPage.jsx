import React, { useState, useEffect, useMemo } from 'react';
import Fuse from 'fuse.js';
import { useService } from '../../hooks/useService.js';
import { SERVICE_KEYS } from '../../core/index.js';

const HARDCODED_TABLES = [
  { id: 'documents', title: 'Documents', icon: '📄', description: 'Database table for application docs' },
  { id: 'todos', title: 'Todos', icon: '✅', description: 'Database table for user tasks' },
  { id: 'users', title: 'Users', icon: '👥', description: 'Database table for user accounts' },
  { id: 'projects', title: 'Projects', icon: '📁', description: 'Database table for project tracking' },
  { id: 'logs', title: 'Logs', icon: '📜', description: 'Database table for system events' },
  { id: 'settings', title: 'Settings', icon: '⚙️', description: 'Database table for app config' },
];

export default function MenuPage({ onSelectModule }) {
  const [search, setSearch] = useState('');
  
  const fuse = useMemo(() => new Fuse(HARDCODED_TABLES, {
    keys: ['title', 'description'],
    threshold: 0.4
  }), []);

  const filteredModules = useMemo(() => {
    if (!search) return HARDCODED_TABLES;
    return fuse.search(search).map(r => r.item);
  }, [search, fuse]);

  return (
    <div className="menu-container">
      <div className="menu-header">
        <div className="stats-grid">
          <div className="stat-card">
            <span className="label">Active Projects</span>
            <span className="value">12</span>
          </div>
          <div className="stat-card">
            <span className="label">Total Documents</span>
            <span className="value">156</span>
          </div>
          <div className="stat-card">
            <span className="label">Pending Tasks</span>
            <span className="value">7</span>
          </div>
          <div className="stat-card">
            <span className="label">System Health</span>
            <span className="value">Optimal</span>
          </div>
        </div>
        <input 
          type="text" 
          className="search-box main-search" 
          placeholder="Search tables..." 
          autoFocus
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
      </div>
      <div className="card-grid">
        {filteredModules.map(table => (
          <div key={table.id} className="card" onClick={() => onSelectModule(table.id)}>
            <div className="card-icon">{table.icon}</div>
            <h3>{table.title}</h3>
            <p>{table.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

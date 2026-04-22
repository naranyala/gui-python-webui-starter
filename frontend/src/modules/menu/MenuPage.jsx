import React, { useState, useMemo } from 'react';
import Fuse from 'fuse.js';

export const MODULES = [
  { id: 'docs', title: 'Documentation', icon: '📄', description: 'View and search markdown documents' },
  { id: 'graph', title: 'Interactive Graph', icon: '🕸️', description: 'Explore relationships in a graph view' },
  { id: 'system', title: 'System Monitor', icon: '🖥️', description: 'Real-time CPU and memory usage' },
  { id: 'todos', title: 'Todo List', icon: '✅', description: 'Simple SQLite-backed task manager' },
];

export default function MenuPage({ onSelectModule }) {
  const [search, setSearch] = useState('');
  
  const fuse = useMemo(() => new Fuse(MODULES, {
    keys: ['title', 'description'],
    threshold: 0.4
  }), []);

  const filteredModules = useMemo(() => {
    if (!search) return MODULES;
    return fuse.search(search).map(r => r.item);
  }, [search, fuse]);

  return (
    <div className="menu-container">
      <div className="menu-header">
        <h1>Welcome to WebUI Starter</h1>
        <p>Select a module to explore</p>
        <input 
          type="text" 
          className="search-box main-search" 
          placeholder="Search modules..." 
          autoFocus
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
      </div>
      <div className="card-grid">
        {filteredModules.map(module => (
          <div key={module.id} className="card" onClick={() => onSelectModule(module.id)}>
            <div className="card-icon">{module.icon}</div>
            <h3>{module.title}</h3>
            <p>{module.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

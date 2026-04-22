import React, { useState, useEffect, useMemo } from 'react';
import { resolve, SERVICE_KEYS, getConfig } from './core/index.js';

// Import Module Pages
import MenuPage, { MODULES } from './modules/menu/MenuPage.jsx';
import DocsPage from './modules/docs/DocsPage.jsx';
import GraphPage from './modules/graph/GraphPage.jsx';
import SystemPage from './modules/system/SystemPage.jsx';
import TodoPage from './modules/todos/TodoPage.jsx';

import './styles/global.css';

function LoadingScreen() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh', background: '#1e1e1e' }}>
      <div style={{ textAlign: 'center' }}>
        <h2 style={{ color: '#fff' }}>Loading...</h2>
        <p style={{ color: '#9d9d9d' }}>Please wait while the application loads.</p>
      </div>
    </div>
  );
}

function App() {
  const [view, setView] = useState('menu');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Services are now initialized globally in index.jsx
    // We just need a small delay to ensure WebUI is ready if needed,
    // though usually it's ready by now.
    const timer = setTimeout(() => setLoading(false), 100);
    
    const config = getConfig();
    const ws = new WebSocket(config.wsBase);
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'status') {
          console.log('[WebSocket] Status:', data.message);
        }
      } catch (e) {}
    };
    
    return () => {
        clearTimeout(timer);
        ws.close();
    };
  }, []);

  if (loading) return <LoadingScreen />;

  const currentModule = MODULES.find(m => m.id === view);

  return (
    <div className="app-container">
      <header className="header">
        <div className="header-left">
          <h1 onClick={() => setView('menu')} style={{ cursor: 'pointer' }}>WebUI Starter</h1>
          {view !== 'menu' && <span className="breadcrumb"> / {currentModule?.title}</span>}
        </div>
        <nav className="tabs">
          <button className={view === 'menu' ? 'active' : ''} onClick={() => setView('menu')}>Home</button>
          {view !== 'menu' && (
            <button onClick={() => setView('menu')}>Back to Menu</button>
          )}
        </nav>
      </header>
      
      <main className="main-content">
        {view === 'menu' && <MenuPage onSelectModule={setView} />}
        {view === 'docs' && <DocsPage />}
        {view === 'graph' && <GraphPage />}
        {view === 'system' && <SystemPage />}
        {view === 'todos' && <TodoPage />}
      </main>
    </div>
  );
}

export default App;

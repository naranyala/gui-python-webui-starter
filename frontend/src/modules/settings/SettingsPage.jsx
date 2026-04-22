import React, { useEffect, useState } from 'react';

export default function SettingsPage() {
  const [settings, setSettings] = useState({});
  const [newKey, setNewKey] = useState('');
  const [newValue, setNewValue] = useState('');
  const [error, setError] = useState(null);

  const fetchSettings = async () => {
    try {
      const response = await fetch('/api/settings');
      const data = await response.json();
      if (data.success) {
        setSettings(data.data);
      }
    } catch (e) {
      setError('Failed to load settings');
    }
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  const saveSetting = async (e) => {
    e.preventDefault();
    if (!newKey) return;
    try {
      const response = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key: newKey, value: newValue }),
      });
      const data = await response.json();
      if (data.success) {
        setNewKey('');
        setNewValue('');
        fetchSettings();
      } else {
        setError(data.error);
      }
    } catch (e) {
      setError('Failed to save setting');
    }
  };

  const deleteSetting = async (key) => {
    // We don't have a delete API yet in server.py, but we'll implement it in the service
    // For now, let's just notify that it's coming or add the route.
    setError('Delete not yet implemented in API');
  };

  return (
    <div className="settings-container">
      <h2>Application Settings</h2>
      
      <form onSubmit={saveSetting} className="settings-form">
        <input 
          type="text" 
          placeholder="Setting Key" 
          value={newKey} 
          onChange={e => setNewKey(e.target.value)} 
        />
        <input 
          type="text" 
          placeholder="Value" 
          value={newValue} 
          onChange={e => setNewValue(e.target.value)} 
        />
        <button type="submit">Save Setting</button>
      </form>

      {error && <div className="error-message">{error}</div>}

      <div className="settings-list">
        <h3>Current Settings</h3>
        {Object.keys(settings).length === 0 ? (
          <p>No settings configured.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Key</th>
                <th>Value</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(settings).map(([key, value]) => (
                <tr key={key}>
                  <td><code>{key}</code></td>
                  <td>{typeof value === 'object' ? JSON.stringify(value) : String(value)}</td>
                  <td>
                    <button onClick={() => deleteSetting(key)} className="btn-delete">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

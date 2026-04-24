import React, { useState, useEffect } from 'react';
import { useService } from '../hooks/useService.js';
import { SERVICE_KEYS } from '../core/index.js';

export default function TableCrudPage({ tableName }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const crudService = useService(SERVICE_KEYS.T_SERVICE);

  const loadData = async () => {
    setLoading(true);
    try {
      const result = await crudService.getData(tableName);
      setData(result);
    } catch (e) {
      console.error('Error loading table data:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [tableName]);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this record?')) return;
    try {
      await crudService.delete(tableName, id);
      loadData();
    } catch (e) {
      alert('Delete failed: ' + e.message);
    }
  };

  if (loading) return <div className="empty-state">Loading data...</div>;

  return (
    <div className="table-crud-container" style={{ padding: '20px' }}>
      <div className="doc-header">
        <h2>{tableName.replace('_', ' ').toUpperCase()}</h2>
        <button 
          className="tabs button active" 
          style={{ padding: '8px 16px', cursor: 'pointer' }}
          onClick={() => {
            const name = prompt('Enter value for primary key (id):');
            if (name) {
                // This is a simplified insert. In a real app, we'd have a form.
                crudService.insert(tableName, { id: name, name: 'New Record' })
                    .then(loadData)
                    .catch(e => alert(e));
            }
          }}
        >
          + Add Record
        </button>
      </div>
      
      <div style={{ overflowX: 'auto', background: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', color: 'var(--text-color)' }}>
          <thead>
            <tr style={{ background: 'var(--header-color)', textAlign: 'left' }}>
              {data.length > 0 && Object.keys(data[0]).map(key => (
                <th key={key} style={{ padding: '12px', borderBottom: '1px solid var(--border-color)' }}>{key}</th>
              ))}
              <th style={{ padding: '12px', borderBottom: '1px solid var(--border-color)' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid var(--border-color)' }}>
                {Object.values(row).map((val, vIdx) => (
                  <td key={vIdx} style={{ padding: '12px' }}>{String(val)}</td>
                ))}
                <td style={{ padding: '12px' }}>
                  <button 
                    className="btn-delete" 
                    onClick={() => handleDelete(Object.values(row)[0])}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {data.length === 0 && <div className="empty-state" style={{ padding: '40px' }}>No records found in this table.</div>}
      </div>
    </div>
  );
}

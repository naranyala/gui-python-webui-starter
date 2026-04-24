import React, { useState, useEffect } from 'react';
import { resolve } from '../core/index.js';

const NotificationToast = () => {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    try {
      const notificationService = resolve(Symbol.for('NotificationService'));
      if (!notificationService) return;

      const unsubscribe = notificationService.subscribe((updatedNotifications) => {
        setNotifications(updatedNotifications);
      });

      return () => unsubscribe();
    } catch (e) {
      console.error('[NotificationToast] Failed to resolve NotificationService', e);
    }
  }, []);

  if (notifications.length === 0) return null;

  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      zIndex: 9999,
      display: 'flex',
      flexDirection: 'column',
      gap: '10px',
      pointerEvents: 'none'
    }}>
      {notifications.map(n => (
        <div key={n.id} style={{
          pointerEvents: 'auto',
          padding: '12px 20px',
          borderRadius: '8px',
          color: '#fff',
          fontSize: '14px',
          fontWeight: '500',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          animation: 'slideIn 0.3s ease-out',
          backgroundColor: n.type === 'error' ? '#ef4444' : n.type === 'success' ? '#22c55e' : '#3b82f6',
          minWidth: '250px',
          maxWidth: '350px',
          cursor: 'pointer'
        }} onClick={() => {
          try {
            resolve(Symbol.for('NotificationService')).remove(n.id);
          } catch(e){}
        }}>
          {n.message}
        </div>
      ))}
      <style>{`
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
      `}</style>
    </div>
  );
};

export default NotificationToast;

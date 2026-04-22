import React, { useState, useEffect, useMemo, useRef } from 'react';
import { resolve, SERVICE_KEYS } from '../../core/index.js';

export default function TodoPage() {
  const service = useMemo(() => resolve(SERVICE_KEYS.TODO_SERVICE), []);
  
  // Local state only stores the latest slice of data from the service
  const [state, setState] = useState({ todos: [], loading: true });
  const [newTask, setNewTask] = useState('');
  const [filter, setFilter] = useState('all');

  // --- Subscription Logic ---
  useEffect(() => {
    // 1. Subscribe to service updates
    const unsubscribe = service.subscribe((newState) => {
        setState(newState);
    });

    // 2. Trigger initial fetch
    service.getAll();

    // 3. Cleanup on unmount
    return () => unsubscribe();
  }, [service]);

  // --- Action Handlers ---
  const handleAdd = (e) => {
    if (e.key === 'Enter' && newTask.trim()) {
      service.create(newTask.trim());
      setNewTask('');
    }
  };

  const handleToggle = (id) => service.toggle(id);
  const handleDelete = (id) => service.delete(id);
  const handleClearCompleted = () => service.clearCompleted();

  // --- UI Derived Data ---
  const filteredTodos = useMemo(() => {
    const { todos } = state;
    if (filter === 'active') return todos.filter(t => !t.completed);
    if (filter === 'completed') return todos.filter(t => t.completed);
    return todos;
  }, [state.todos, filter]);

  const activeCount = state.todos.filter(t => !t.completed).length;

  if (state.loading && state.todos.length === 0) return (
    <div style={{ padding: '40px', color: '#9d9d9d' }}>
      Loading tasks...
    </div>
  );

  return (
    <div className="todo-container mvc-style">
      <header className="todo-header">
        <h2>todos</h2>
        <input 
          type="text" 
          className="new-todo-input" 
          placeholder="What needs to be done?" 
          value={newTask}
          onChange={e => setNewTask(e.target.value)}
          onKeyDown={handleAdd}
          autoFocus
        />
      </header>

      <section className="todo-main">
        <ul className="todo-list mvc">
          {filteredTodos.map(todo => (
            <li key={todo.id} className={todo.completed ? 'completed' : ''}>
              <div className="view">
                <input 
                  type="checkbox" 
                  className="toggle" 
                  checked={!!todo.completed} 
                  onChange={() => handleToggle(todo.id)} 
                />
                <label>
                  {todo.task}
                </label>
                <button className="destroy" onClick={() => handleDelete(todo.id)}>×</button>
              </div>
            </li>
          ))}
        </ul>
      </section>

      {state.todos.length > 0 && (
        <footer className="todo-footer">
          <span className="todo-count">
            <strong>{activeCount}</strong> {activeCount === 1 ? 'item' : 'items'} left
          </span>
          <ul className="filters">
            <li>
              <button className={filter === 'all' ? 'selected' : ''} onClick={() => setFilter('all')}>All</button>
            </li>
            <li>
              <button className={filter === 'active' ? 'selected' : ''} onClick={() => setFilter('active')}>Active</button>
            </li>
            <li>
              <button className={filter === 'completed' ? 'selected' : ''} onClick={() => setFilter('completed')}>Completed</button>
            </li>
          </ul>
          {state.todos.some(t => t.completed) && (
            <button className="clear-completed" onClick={handleClearCompleted}>
              Clear completed
            </button>
          )}
        </footer>
      )}
    </div>
  );
}

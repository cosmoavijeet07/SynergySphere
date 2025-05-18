import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Sidebar() {
  const user = JSON.parse(localStorage.getItem('user')) || { name: 'User', email: 'user@example.com' };
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <aside className="sidebar">
      <div className="user-info">
        <div className="user-avatar large">{user.name.charAt(0)}</div>
        <h3>{user.name}</h3>
        <p>{user.email}</p>
      </div>
      
      <nav className="sidebar-links">
        <Link to="/projects" className={isActive('/projects')}>
          <i className="icon">📋</i>
          Projects
        </Link>
        <Link to="/my-tasks" className={isActive('/my-tasks')}>
          <i className="icon">✓</i>
          My Tasks
        </Link>
      </nav>
    </aside>
  );
}

export default Sidebar; 
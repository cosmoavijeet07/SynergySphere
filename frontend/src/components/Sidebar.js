import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

function Sidebar({ isSidebarOpen, setIsSidebarOpen }) {
  const location = useLocation();
  
  const getUserData = () => {
    try {
      const userData = localStorage.getItem('user');
      if (userData) {
        return JSON.parse(userData);
      }
    } catch (error) {
      console.error('Failed to parse user data', error);
    }
    return { 
      name: 'Guest User', 
      email: 'guest@example.com',
      fallback: true
    };
  };

  const user = getUserData();
  const firstChar = user.name?.charAt(0) || 'G';

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <aside className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
      <button 
        className="sidebar-close"
        onClick={() => setIsSidebarOpen(false)}
      >
        ×
      </button>
      {/* <div className="user-info">
        <div className="user-avatar large">{firstChar}</div>
        <h3>{user.name}</h3>
        <p>{user.email}</p>
        {user.fallback && (
          <small className="login-prompt">Please log in properly</small>
        )}
      </div> */}
      
      <nav className="sidebar-links">
        {user && (
          <div className="sidebar-profile">
            <Link to="/profile" className="profile-link">
              <div className="profile-avatar">{user.name?.charAt(0).toUpperCase()}</div>
              <div className="profile-info">
                <span className="profile-name">{user.name}</span><br></br>
                <span className="profile-email">{user.email}</span>
              </div>
            </Link>
          </div>
        )}
        <Link to="/projects" className={isActive('/projects')} onClick={() => setIsSidebarOpen(false)}>
          <i className="icon">📋</i>
          Projects
        </Link>
        <Link to="/my-tasks" className={isActive('/my-tasks')} onClick={() => setIsSidebarOpen(false)}>
          <i className="icon">✓</i>
          My Tasks
        </Link>
      </nav>
    </aside>
  );
}

export default Sidebar;
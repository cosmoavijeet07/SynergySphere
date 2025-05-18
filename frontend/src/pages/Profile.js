import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { logoutUser } from '../services/api';
import './Profile.css';

function Profile() {
  const navigate = useNavigate();
  const [preferences, setPreferences] = useState({
    notifications: localStorage.getItem('prefs_notifications') === 'true',
    emailUpdates: localStorage.getItem('prefs_emailUpdates') === 'true',
    darkMode: localStorage.getItem('prefs_darkMode') === 'true',
    soundEffects: localStorage.getItem('prefs_soundEffects') === 'true',
    taskReminders: localStorage.getItem('prefs_taskReminders') === 'true',
    projectUpdates: localStorage.getItem('prefs_projectUpdates') === 'true',
  });
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Get user data from localStorage
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    } else {
      navigate('/login');
    }
  }, [navigate]);

  const handleLogout = () => {
    logoutUser();
    navigate('/login');
  };

  const handleToggle = (key) => {
    const newValue = !preferences[key];
    setPreferences(prev => ({
      ...prev,
      [key]: newValue
    }));
    localStorage.setItem(`prefs_${key}`, newValue);
  };

  if (!user) {
    return null;
  }

  return (
    <div className="profile-container">
      <div className="profile-card">
        <div className="profile-header">
          <h2>Profile</h2>
          <div className="profile-avatar">
            {user.name?.charAt(0).toUpperCase()}
          </div>
        </div>

        <div className="profile-info">
          <div className="info-group">
            <label>Name</label>
            <p>{user.name}</p>
          </div>

          <div className="info-group">
            <label>Email</label>
            <p>{user.email}</p>
          </div>

          <div className="preferences">
            <h3>Preferences</h3>
            
            <div className="preferences-section">
              <h4>Notifications</h4>
              <div className="toggle-group">
                <label>
                  Push Notifications
                  <div 
                    className={`toggle ${preferences.notifications ? 'active' : ''}`}
                    onClick={() => handleToggle('notifications')}
                  >
                    <div className="toggle-handle"></div>
                  </div>
                </label>
              </div>
              <div className="toggle-group">
                <label>
                  Email Updates
                  <div 
                    className={`toggle ${preferences.emailUpdates ? 'active' : ''}`}
                    onClick={() => handleToggle('emailUpdates')}
                  >
                    <div className="toggle-handle"></div>
                  </div>
                </label>
              </div>
              <div className="toggle-group">
                <label>
                  Task Reminders
                  <div 
                    className={`toggle ${preferences.taskReminders ? 'active' : ''}`}
                    onClick={() => handleToggle('taskReminders')}
                  >
                    <div className="toggle-handle"></div>
                  </div>
                </label>
              </div>
              <div className="toggle-group">
                <label>
                  Project Updates
                  <div 
                    className={`toggle ${preferences.projectUpdates ? 'active' : ''}`}
                    onClick={() => handleToggle('projectUpdates')}
                  >
                    <div className="toggle-handle"></div>
                  </div>
                </label>
              </div>
            </div>

            <div className="preferences-section">
              <h4>App Settings</h4>
              <div className="toggle-group">
                <label>
                  Dark Mode
                  <div 
                    className={`toggle ${preferences.darkMode ? 'active' : ''}`}
                    onClick={() => handleToggle('darkMode')}
                  >
                    <div className="toggle-handle"></div>
                  </div>
                </label>
              </div>
              <div className="toggle-group">
                <label>
                  Sound Effects
                  <div 
                    className={`toggle ${preferences.soundEffects ? 'active' : ''}`}
                    onClick={() => handleToggle('soundEffects')}
                  >
                    <div className="toggle-handle"></div>
                  </div>
                </label>
              </div>
            </div>
          </div>

          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}

export default Profile;

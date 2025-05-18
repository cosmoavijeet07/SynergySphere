import { useState, useEffect } from 'react';

export default function useAuth() {
  const [auth, setAuth] = useState(null);

  useEffect(() => {
    const loadAuth = () => {
      try {
        const token = localStorage.getItem('token');
        const user = JSON.parse(localStorage.getItem('user'));
        
        if (token && user) {
          setAuth({ token, user });
        } else {
          setAuth(null);
        }
      } catch (error) {
        console.error('Auth load error:', error);
        setAuth(null);
      }
    };

    loadAuth();
    window.addEventListener('storage', loadAuth);
    return () => window.removeEventListener('storage', loadAuth);
  }, []);

  return auth;
}
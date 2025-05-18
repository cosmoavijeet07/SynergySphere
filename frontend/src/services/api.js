import axios from 'axios';

const baseURL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// -------------------- AUTH ------------------------

/**
 * Logs in the user and stores token + user in localStorage.
 * @returns {Promise<{token: string, user: object}>}
 */
export const loginUser = async (email, password) => {
  try {
    const response = await api.post('/login', { email, password });
    
    // Validate response structure
    if (!response.data?.token || !response.data?.user?.id || !response.data?.user?.email) {
      throw new Error('Invalid server response structure');
    }

    // Create normalized auth data
    const authData = {
      token: response.data.token,
      user: {
        id: response.data.user.id,
        name: response.data.user.name || email.split('@')[0] || 'User',
        email: response.data.user.email
      }
    };

    // Store auth data
    localStorage.setItem('token', authData.token);
    localStorage.setItem('user', JSON.stringify(authData.user));
    
    return authData;
  } catch (error) {
    // Clear any partial auth data on failure
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    // Enhance error message for debugging
    const errorMessage = error.response?.data?.message || 
                        error.message || 
                        'Login failed. Please try again.';
    
    throw new Error(errorMessage);
  }
};

/**
 * Signs up the user and returns response (user creation only).
 */
export const signupUser = (name, email, password) => {
  return api.post('/signup', { name, email, password });
};

/**
 * Logs out the user and clears stored auth data.
 */
export const logoutUser = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

// -------------------- PROJECTS ------------------------

export const getProjects = () => api.get('/projects');
export const getProjectById = (id) => api.get(`/projects/${id}`);
export const createProject = (projectData) => api.post('/projects', projectData);
export const updateProject = (id, projectData) => api.put(`/projects/${id}`, projectData);

// -------------------- TASKS ------------------------

export const getTasks = () => api.get('/tasks');
export const getTaskById = (id) => api.get(`/tasks/${id}`);
export const createTask = (taskData) => api.post('/tasks', taskData);
export const updateTask = (id, taskData) => api.put(`/tasks/${id}`, taskData);

export default api;

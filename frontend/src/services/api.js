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
  const response = await api.post('/login', { email, password });

  // Save auth data to localStorage
  const { token, user } = response.data;
  localStorage.setItem('token', token);
  localStorage.setItem('user', JSON.stringify(user));
  
  return response;
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

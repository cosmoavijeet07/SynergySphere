import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, Outlet } from 'react-router-dom';
import Signup from './pages/Signup';
import Login from './pages/Login';
import Projects from './pages/Projects';
import ProjectDetails from './pages/ProjectDetails';
import MyTasks from './pages/MyTasks';
import CreateProject from './pages/CreateProject';
import CreateTask from './pages/CreateTask';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

// Layout for authenticated pages
function MainLayout() {
  return (
    <>
      <Navbar />
      <div className="main-content">
        <Sidebar />
        <div className="content">
          <Outlet />
        </div>
      </div>
    </>
  );
}

// Layout for auth pages (login/signup)
function AuthLayout() {
  return <Outlet />;
}

// Route guard
const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Auth pages */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
        </Route>
        {/* Protected pages */}
        <Route element={<PrivateRoute><MainLayout /></PrivateRoute>}>
          <Route path="/projects" element={<Projects />} />
          <Route path="/projects/:id" element={<ProjectDetails />} />
          <Route path="/my-tasks" element={<MyTasks />} />
          <Route path="/projects/new" element={<CreateProject />} />
          <Route path="/tasks/new" element={<CreateTask />} />
          <Route path="/tasks/edit/:id" element={<CreateTask />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;

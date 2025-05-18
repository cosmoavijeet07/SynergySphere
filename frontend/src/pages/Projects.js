import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProjects } from '../services/api'; // Import the API function
import ProjectCard from '../components/ProjectCard';
import './Projects.css';

function Projects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        const response = await getProjects(); // Use the imported API function
        setProjects(response.data);
      } catch (err) {
        console.error('Error fetching projects:', err);
        setError('Failed to load projects. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchProjects();
  }, []);

  const handleAddProject = () => {
    navigate('/projects/new');
  };

  if (loading) {
    return <div className="loading">Loading projects...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="projects-page">
      <div className="projects-header">
        <h2 className="projects-title">Projects</h2>
        <button className="add-project-btn" onClick={handleAddProject}>
          + Add Project
        </button>
      </div>
      <div className="projects-grid">
        {projects.length > 0 ? (
          projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))
        ) : (
          <p>No projects found. Create your first project!</p>
        )}
      </div>
    </div>
  );
}

export default Projects;
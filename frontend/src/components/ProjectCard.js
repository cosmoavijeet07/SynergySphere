import React from 'react';
import { useNavigate } from 'react-router-dom';
import './ProjectCard.css';

function ProjectCard({ project }) {
  const navigate = useNavigate();

  const getStatusClass = (status) => {
    switch (status?.toLowerCase()) {
      case 'completed':
        return 'status-completed';
      case 'in progress':
        return 'status-in-progress';
      default:
        return 'status-pending';
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'No deadline';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="card project-card" onClick={() => navigate(`/projects/${project.id}`)}>
      {project.image && (
        <div className="card-image">
          <img src={project.image} alt={project.name} />
        </div>
      )}
      
      <div className="card-content">
        <h3 className="card-title">{project.name}</h3>
        
        <div className="card-details">
          <p className="topic">
            <span className="label">Topic:</span>
            {project.topic || 'Not specified'}
          </p>
          
          <p className="deadline">
            <span className="label">Deadline:</span>
            {formatDate(project.deadline)}
          </p>
          
          <p className="manager">
            <span className="label">Manager:</span>
            {project.manager_name || 'Not assigned'}
          </p>
        </div>

        <div className="card-footer">
          <span className={`status ${getStatusClass(project.status)}`}>
            {project.status || 'Pending'}
          </span>
          
          {project.description && (
            <p className="description">{project.description}</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProjectCard; 
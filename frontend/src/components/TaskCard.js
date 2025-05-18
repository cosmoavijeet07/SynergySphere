import React from 'react';
import { useNavigate } from 'react-router-dom';
import './TaskCard.css';

function TaskCard({ task }) {
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
    <div className="card task-card" onClick={() => navigate(`/tasks/edit/${task.id}`)}>
      {task.image && (
        <div className="card-image">
          <img src={task.image} alt={task.name} />
        </div>
      )}
      
      <div className="card-content">
        <h3 className="card-title">{task.name}</h3>
        
        <div className="card-details">
          <p className="project">
            <span className="label">Project:</span>
            {task.project_name || 'Not assigned'}
          </p>
          
          <p className="assignee">
            <span className="label">Assignee:</span>
            {task.assignee_name || 'Not assigned'}
          </p>
          
          <p className="topic">
            <span className="label">Topic:</span>
            {task.topic || 'Not specified'}
          </p>
          
          <p className="deadline">
            <span className="label">Deadline:</span>
            {formatDate(task.deadline)}
          </p>
        </div>

        <div className="card-footer">
          <span className={`status ${getStatusClass(task.status)}`}>
            {task.status || 'Pending'}
          </span>
          
          {task.description && (
            <p className="description">{task.description}</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default TaskCard; 
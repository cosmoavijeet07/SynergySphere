import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import TaskCard from '../components/TaskCard';
import './ProjectDetails.css';

function ProjectDetails() {
  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProjectDetails = async () => {
      try {
        const response = await axios.get(`/api/projects/${id}`);
        setProject(response.data);
      } catch (error) {
        console.error('Error fetching project details:', error);
      }
    };
    fetchProjectDetails();
  }, [id]);

  const handleAddTask = () => {
    navigate(`/tasks/new?projectId=${id}`);
  };

  return (
    <div className="project-details-page">
      {project ? (
        <div className="project-details-card">
          <div className="project-details-header">
            <h2>{project.name}</h2>
            <button className="add-task-btn" onClick={handleAddTask}>+ Add Task</button>
          </div>
          <div className="project-details-info">
            <p><strong>Topic:</strong> {project.topic}</p>
            <p><strong>Deadline:</strong> {project.deadline}</p>
            <p><strong>Status:</strong> {project.status}</p>
          </div>
          <div className="project-details-description">
            {project.description}
          </div>
        </div>
      ) : (
        <p>Loading...</p>
      )}
      <div className="tasks-section">
        <h3>Tasks</h3>
        <div className="tasks-grid">
          {tasks.map(task => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default ProjectDetails; 
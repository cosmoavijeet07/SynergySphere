import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getProjectById, getTasks } from '../services/api';
import TaskCard from '../components/TaskCard';
import './ProjectDetails.css';

function ProjectDetails() {
  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch project details
        const projectResponse = await getProjectById(id);
        console.log(projectResponse);
        setProject(projectResponse.data[0]);
        
        // Fetch tasks for this project
        const tasksResponse = await getTasks();
        const projectTasks = tasksResponse.data.filter(task => task.project_id === parseInt(id));
        setTasks(projectTasks);
        
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load project details. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const handleAddTask = () => {
    navigate(`/tasks/new?projectId=${id}`);
  };

  if (loading) {
    return <div className="loading">Loading project details...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!project) {
    return <div className="error">Project not found</div>;
  }

  return (
    <div className="project-details-page">
      <div className="project-details-card">
        <div className="project-details-header">
          <h2>{project.name}</h2>
          <button className="add-task-btn" onClick={handleAddTask}>
            + Add Task
          </button>
        </div>
        
        <div className="project-details-info">
          <p><strong>Topic:</strong> {project.topic || 'Not specified'}</p>
          <p><strong>Deadline:</strong> {project.deadline || 'No deadline set'}</p>
          <p><strong>Status:</strong> <span className={`status-${project.status}`}>{project.status}</span></p>
        </div>
        
        {project.description && (
          <div className="project-details-description">
            <h4>Description:</h4>
            <p>{project.description}</p>
          </div>
        )}
      </div>

      <div className="tasks-section">
        <h3>Tasks ({tasks.length})</h3>
        {tasks.length > 0 ? (
          <div className="tasks-grid">
            {tasks.map(task => (
              <TaskCard key={task.id} task={task} />
            ))}
          </div>
        ) : (
          <p className="no-tasks">No tasks yet for this project</p>
        )}
      </div>
    </div>
  );
}

export default ProjectDetails;
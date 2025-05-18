import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { createProject, getProjectById, updateProject } from '../services/api';
import './CreateProject.css';

function CreateProject() {
  const [name, setName] = useState('');
  const [topic, setTopic] = useState('');
  const [manager, setManager] = useState('');
  const [deadline, setDeadline] = useState('');
  const [image, setImage] = useState('');
  const [description, setDescription] = useState('');
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    if (id) {
      const fetchProject = async () => {
        try {
          const response = await getProjectById(id);
          const project = response.data;
          setName(project.name);
          setTopic(project.topic);
          setManager(project.manager_id);
          setDeadline(project.deadline);
          setImage(project.image);
          setDescription(project.description);
        } catch (error) {
          setError('Error fetching project details');
          console.error('Error fetching project:', error);
        }
      };
      fetchProject();
    }
  }, [id]);

  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const projectData = {
        name,
        topic,
        manager_id: parseInt(manager), // Convert to integer
        deadline,
        image,
        description,
        status: 'active' // Set default status
      };

      if (id) {
        await updateProject(id, projectData);
      } else {
        await createProject(projectData);
      }
      navigate('/projects');
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Error saving project. Please try again.';
      setError(errorMessage);
      console.error('Error saving project:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="create-project">
      <h2>{id ? 'Edit Project' : 'Create Project'}</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
        <input type="text" placeholder="Topic" value={topic} onChange={(e) => setTopic(e.target.value)} />
        <input type="text" placeholder="Manager ID" value={manager} onChange={(e) => setManager(e.target.value)} required />
        <input type="date" placeholder="Deadline" value={deadline} onChange={(e) => setDeadline(e.target.value)} />
        <input type="text" placeholder="Image URL" value={image} onChange={(e) => setImage(e.target.value)} />
        <textarea placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Saving...' : (id ? 'Update Project' : 'Create Project')}
        </button>
      </form>
    </div>
  );
}

export default CreateProject;
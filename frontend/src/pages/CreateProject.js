import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

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
          const response = await axios.get(`/api/projects/${id}`);
          const project = response.data;
          setName(project.name);
          setTopic(project.topic);
          setManager(project.manager_id);
          setDeadline(project.deadline);
          setImage(project.image);
          setDescription(project.description);
        } catch (error) {
          console.error('Error fetching project:', error);
        }
      };
      fetchProject();
    }
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (id) {
        await axios.put(`/api/projects/${id}`, { name, topic, manager_id: manager, deadline, image, description });
      } else {
        await axios.post('/api/projects', { name, topic, manager_id: manager, deadline, image, description });
      }
      navigate('/projects');
    } catch (error) {
      console.error('Error saving project:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>{id ? 'Edit Project' : 'Create Project'}</h2>
      <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
      <input type="text" placeholder="Topic" value={topic} onChange={(e) => setTopic(e.target.value)} />
      <input type="text" placeholder="Manager ID" value={manager} onChange={(e) => setManager(e.target.value)} required />
      <input type="date" placeholder="Deadline" value={deadline} onChange={(e) => setDeadline(e.target.value)} />
      <input type="text" placeholder="Image URL" value={image} onChange={(e) => setImage(e.target.value)} />
      <textarea placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
      <button type="submit">{id ? 'Update Project' : 'Create Project'}</button>
    </form>
  );
}

export default CreateProject; 
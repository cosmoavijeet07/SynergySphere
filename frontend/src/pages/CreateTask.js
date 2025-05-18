import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import './CreateTask.css';

function CreateTask() {
  const [name, setName] = useState('');
  const [assignee, setAssignee] = useState('');
  const [project, setProject] = useState('');
  const [topic, setTopic] = useState('');
  const [deadline, setDeadline] = useState('');
  const [image, setImage] = useState('');
  const [description, setDescription] = useState('');
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const projectId = queryParams.get('projectId');

  useEffect(() => {
    if (id) {
      const fetchTask = async () => {
        try {
          const response = await axios.get(`/api/tasks/${id}`);
          const task = response.data;
          setName(task.name);
          setAssignee(task.assignee_id);
          setProject(task.project_id);
          setTopic(task.topic);
          setDeadline(task.deadline);
          setImage(task.image);
          setDescription(task.description);
        } catch (error) {
          console.error('Error fetching task:', error);
        }
      };
      fetchTask();
    } else if (projectId) {
      setProject(projectId);
    }
  }, [id, projectId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (id) {
        await axios.put(`/api/tasks/${id}`, { name, assignee_id: assignee, project_id: project, topic, deadline, image, description });
      } else {
        await axios.post('/api/tasks', { name, assignee_id: assignee, project_id: project, topic, deadline, image, description });
      }
      navigate('/my-tasks');
    } catch (error) {
      console.error('Error saving task:', error);
    }
  };

  return (
    <div className="create-task">
      <h2>{id ? 'Edit Task' : 'Create Task'}</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
        <input type="text" placeholder="Assignee ID" value={assignee} onChange={(e) => setAssignee(e.target.value)} required />
        <input type="text" placeholder="Project ID" value={project} onChange={(e) => setProject(e.target.value)} required />
        <input type="text" placeholder="Topic" value={topic} onChange={(e) => setTopic(e.target.value)} />
        <input type="date" placeholder="Deadline" value={deadline} onChange={(e) => setDeadline(e.target.value)} />
        <input type="text" placeholder="Image URL" value={image} onChange={(e) => setImage(e.target.value)} />
        <textarea placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
        <button type="submit">{id ? 'Update Task' : 'Create Task'}</button>
      </form>
    </div>
  );
}

export default CreateTask;
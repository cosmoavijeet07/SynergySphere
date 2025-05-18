import React, { useState, useEffect } from 'react';
import { getTasks } from '../services/api';
import TaskCard from '../components/TaskCard';
import './MyTasks.css';

function MyTasks() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await getTasks();
        setTasks(response.data);
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    };

    fetchTasks();
  }, []);

  return (
    <div className="mytasks-page">
      <div className="mytasks-header">
        <h2>My Tasks</h2>
      </div>
      <div className="tasks-grid">
        {tasks.map(task => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
    </div>
  );
}

export default MyTasks;

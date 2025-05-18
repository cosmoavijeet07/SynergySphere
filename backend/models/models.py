import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

DB_NAME = 'synergysphere.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================
# USER FUNCTIONS
# ==========================

def create_user(name, email, password):
    """Creates a new user with hashed password."""
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    cursor.execute(
        'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
        (name, email, hashed_password)
    )
    conn.commit()
    conn.close()

def get_user_by_email(email):
    """Fetches a user by email."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

# ==========================
# PROJECT FUNCTIONS
# ==========================

def get_all_projects():
    """Fetches all projects."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects')
    projects = cursor.fetchall()
    conn.close()
    return projects

def create_project(name, manager_id, topic, deadline, status, image, description):
    """Creates a new project."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO projects (name, manager_id, topic, deadline, status, image, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (name, manager_id, topic, deadline, status, image, description)
    )
    conn.commit()
    conn.close()

def get_project_by_id(project_id):
    """Fetches a project by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()
    conn.close()
    return project

def update_project(project_id, name, manager_id, topic, deadline, status, image, description):
    """Updates an existing project."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE projects
        SET name = ?, manager_id = ?, topic = ?, deadline = ?, status = ?, image = ?, description = ?
        WHERE id = ?
        ''',
        (name, manager_id, topic, deadline, status, image, description, project_id)
    )
    conn.commit()
    conn.close()

# ==========================
# TASK FUNCTIONS
# ==========================

def get_all_tasks():
    """Fetches all tasks."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def create_task(name, assignee_id, project_id, topic, deadline, status, image, description):
    """Creates a new task."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO tasks (name, assignee_id, project_id, topic, deadline, status, image, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (name, assignee_id, project_id, topic, deadline, status, image, description)
    )
    conn.commit()
    conn.close()

def get_task_by_id(task_id):
    """Fetches a task by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def update_task(task_id, name, assignee_id, project_id, topic, deadline, status, image, description):
    """Updates an existing task."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE tasks
        SET name = ?, assignee_id = ?, project_id = ?, topic = ?, deadline = ?, status = ?, image = ?, description = ?
        WHERE id = ?
        ''',
        (name, assignee_id, project_id, topic, deadline, status, image, description, task_id)
    )
    conn.commit()
    conn.close()

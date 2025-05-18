import sqlite3
from datetime import datetime

DB_NAME = 'synergysphere.db'

def init_db():
    """Initialize the database with required tables and constraints"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Enable foreign key constraints
    cursor.execute('PRAGMA foreign_keys = ON;')

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create projects table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        manager_id INTEGER NOT NULL,
        topic TEXT,
        deadline DATETIME,
        status TEXT DEFAULT 'pending',
        image TEXT,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

    # Create tasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        assignee_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        topic TEXT,
        deadline DATETIME,
        status TEXT DEFAULT 'todo',
        image TEXT,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (assignee_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
    )
    ''')

    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_email ON users(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_project_manager ON projects(manager_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_task_assignee ON tasks(assignee_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_task_project ON tasks(project_id)')

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

def reset_db():
    """Reset the database (for development purposes)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS tasks')
    cursor.execute('DROP TABLE IF EXISTS projects')
    cursor.execute('DROP TABLE IF EXISTS users')
    
    conn.commit()
    conn.close()
    init_db()
    print("✅ Database reset successfully.")

if __name__ == '__main__':
    init_db()
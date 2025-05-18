import sqlite3

DB_NAME = 'synergysphere.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('PRAGMA foreign_keys = ON;')

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
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
        status TEXT,
        image TEXT,
        description TEXT,
        FOREIGN KEY (manager_id) REFERENCES users (id) ON DELETE CASCADE
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
        status TEXT,
        image TEXT,
        description TEXT,
        FOREIGN KEY (assignee_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

if __name__ == '__main__':
    init_db()

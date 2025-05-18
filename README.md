# SynergySphere – Advanced Team Collaboration Platform

SynergySphere is a smart, responsive team collaboration platform designed to optimize productivity, streamline communication, and proactively manage project tasks. This README covers everything you need to get started with development, deployment, and understanding the codebase.

---

## Demo Video
(click here) [https://drive.google.com/file/d/1P8F9R_yeXgh6fBF7UTtt65exJ5ByMVCb/view?usp=sharing]

## 📦 1. Cloning the Repository

```bash
git clone https://github.com/cosmoavijeet07/SynergySphere.git
cd SynergySphere
```

Make sure to update the URL to your actual GitHub repo.

---

## 🐳 2. Building with Docker and Running the Application

### 🔧 Prerequisites

* Python installed
* Node.js and Python installed (if you want to run without Docker)


### 🥪 Running without Docker

```bash
# Backend
cd backend
pip install -r requirements.txt
python3 app.py

# Frontend
cd frontend
npm install
npm start
```

---

## 📂 3. File System Structure

```bash
SynergySphere/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   └── package.json
│
├── README.md

```

---

## 🧠 4. Tech Stack

**Frontend:**

* React.js
* TailwindCSS
* Axios (for API calls)

**Backend:**

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL (or SQLite for dev)

**Others:**

* Docker & Docker Compose
* JWT for auth
* WebSockets for real-time updates (planned)

---

## 📡 5. API Endpoints

### Auth

* `POST /api/auth/register` – Register new user
* `POST /api/auth/login` – Login and receive JWT token

### Projects

* `GET /api/projects` – List all projects for a user
* `POST /api/projects` – Create a new project
* `GET /api/projects/{id}` – Get project details

### Tasks

* `GET /api/projects/{id}/tasks` – List all tasks in project
* `POST /api/projects/{id}/tasks` – Create task
* `PATCH /api/tasks/{task_id}` – Update task status/details

### Team

* `POST /api/projects/{id}/add-member` – Add user to project


---

## 🧹 6. Models

### User

```python
User {
  id: UUID
  name: str
  email: str
  password_hash: str
}
```

### Project

```python
Project {
  id: UUID
  name: str
  owner_id: UUID
  members: List[User]
}
```

### Task

```python
Task {
  id: UUID
  title: str
  description: str
  due_date: date
  status: Enum('To-Do', 'In Progress', 'Done')
  assignee_id: UUID
  project_id: UUID
}
```


## 📈 Future Enhancements

* Real-time collaboration (WebSocket-based)
* Calendar and timeline views
* Advanced notifications and reminders
* AI-based issue predictions and suggestions

---


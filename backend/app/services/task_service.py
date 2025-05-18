from datetime import datetime
from app.extensions import db
from app.models import Task, TaskAssignment, Comment

def create_task(project_id, title, description, due_date, created_by, assignee_ids=None):
    task = Task(
        project_id=project_id,
        title=title,
        description=description,
        due_date=due_date,
        created_by=created_by,
        status='todo'
    )
    db.session.add(task)
    db.session.commit()
    
    if assignee_ids:
        for user_id in assignee_ids:
            assign_task(task.id, user_id)
    
    return task

def assign_task(task_id, user_id):
    assignment = TaskAssignment(
        task_id=task_id,
        user_id=user_id
    )
    db.session.add(assignment)
    db.session.commit()
    return assignment

def update_task_status(task_id, status):
    task = Task.query.get(task_id)
    if not task:
        return None
    
    task.status = status
    db.session.commit()
    return task

def add_comment(task_id, user_id, content):
    comment = Comment(
        task_id=task_id,
        user_id=user_id,
        content=content
    )
    db.session.add(comment)
    db.session.commit()
    return comment

def get_project_tasks(project_id, user_id=None):
    query = Task.query.filter_by(project_id=project_id)
    if user_id:
        query = query.join(TaskAssignment).filter(
            TaskAssignment.user_id == user_id
        )
    return query.all()
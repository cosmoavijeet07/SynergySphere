from flask import Blueprint, request, jsonify
from flask_security import auth_required, current_user
from app.services.task_service import (
    create_task, assign_task, update_task_status,
    add_comment, get_project_tasks
)
from app.services.project_service import get_project_by_id
from app.extensions import db
from datetime import datetime

task_bp = Blueprint('task', __name__)

@task_bp.route('/project/<int:project_id>', methods=['GET'])
@auth_required()
def list_tasks(project_id):
    project = get_project_by_id(project_id, current_user.id)
    if not project:
        return jsonify({'error': 'Project not found or access denied'}), 404
    
    tasks = get_project_tasks(project_id)
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'status': t.status,
        'due_date': t.due_date.isoformat() if t.due_date else None,
        'created_by': t.created_by,
        'assignees': [a.user_id for a in t.assignments]
    } for t in tasks])

@task_bp.route('/', methods=['POST'])
@auth_required()
def create_new_task():
    data = request.get_json()
    project_id = data.get('project_id')
    title = data.get('title')
    description = data.get('description')
    due_date_str = data.get('due_date')
    assignee_ids = data.get('assignee_ids', [])
    
    if not all([project_id, title]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    project = get_project_by_id(project_id, current_user.id)
    if not project:
        return jsonify({'error': 'Project not found or access denied'}), 404
    
    try:
        due_date = datetime.fromisoformat(due_date_str) if due_date_str else None
    except ValueError:
        return jsonify({'error': 'Invalid due date format'}), 400
    
    task = create_task(
        project_id=project_id,
        title=title,
        description=description,
        due_date=due_date,
        created_by=current_user.id,
        assignee_ids=assignee_ids
    )
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'status': task.status,
        'due_date': task.due_date.isoformat() if task.due_date else None
    }), 201

@task_bp.route('/<int:task_id>/status', methods=['PUT'])
@auth_required()
def update_task(task_id):
    data = request.get_json()
    status = data.get('status')
    
    if not status:
        return jsonify({'error': 'Status is required'}), 400
    
    task = update_task_status(task_id, status)
    if not task:
        return jsonify({'error': 'Task not found or access denied'}), 404
    
    return jsonify({
        'id': task.id,
        'status': task.status
    })

@task_bp.route('/<int:task_id>/comments', methods=['POST'])
@auth_required()
def add_task_comment(task_id):
    data = request.get_json()
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'Comment content is required'}), 400
    
    comment = add_comment(task_id, current_user.id, content)
    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'created_at': comment.created_at.isoformat(),
        'user': {
            'id': comment.user.id,
            'name': comment.user.name
        }
    }), 201
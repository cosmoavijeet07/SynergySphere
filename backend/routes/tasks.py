from flask import Blueprint, request, jsonify
from models.models import get_all_tasks, create_task, get_task_by_id, update_task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = get_all_tasks()
    return jsonify(tasks), 200

@tasks_bp.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    name = data.get('name')
    assignee_id = data.get('assignee_id')
    project_id = data.get('project_id')
    topic = data.get('topic')
    deadline = data.get('deadline')
    status = data.get('status')
    image = data.get('image')
    description = data.get('description')

    if not name or not assignee_id or not project_id:
        return jsonify({'error': 'Missing required fields'}), 400

    create_task(name, assignee_id, project_id, topic, deadline, status, image, description)
    return jsonify({'message': 'Task created successfully'}), 201

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task), 200

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    data = request.get_json()
    name = data.get('name')
    assignee_id = data.get('assignee_id')
    project_id = data.get('project_id')
    topic = data.get('topic')
    deadline = data.get('deadline')
    status = data.get('status')
    image = data.get('image')
    description = data.get('description')

    if not name or not assignee_id or not project_id:
        return jsonify({'error': 'Missing required fields'}), 400

    task = get_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    update_task(task_id, name, assignee_id, project_id, topic, deadline, status, image, description)
    return jsonify({'message': 'Task updated successfully'}), 200 
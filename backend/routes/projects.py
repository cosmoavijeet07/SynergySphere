from flask import Blueprint, request, jsonify
from models.models import get_all_projects, create_project, get_project_by_id, update_project

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/api/projects', methods=['GET'])
def get_projects():
    projects = get_all_projects()
    return jsonify(projects), 200

@projects_bp.route('/api/projects', methods=['POST'])
def add_project():
    data = request.get_json()
    name = data.get('name')
    manager_id = data.get('manager_id')
    topic = data.get('topic')
    deadline = data.get('deadline')
    status = data.get('status')
    image = data.get('image')
    description = data.get('description')

    if not name or not manager_id:
        return jsonify({'error': 'Missing required fields'}), 400

    create_project(name, manager_id, topic, deadline, status, image, description)
    return jsonify({'message': 'Project created successfully'}), 201

@projects_bp.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = get_project_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify(project), 200

@projects_bp.route('/api/projects/<int:project_id>', methods=['PUT'])
def edit_project(project_id):
    data = request.get_json()
    name = data.get('name')
    manager_id = data.get('manager_id')
    topic = data.get('topic')
    deadline = data.get('deadline')
    status = data.get('status')
    image = data.get('image')
    description = data.get('description')

    if not name or not manager_id:
        return jsonify({'error': 'Missing required fields'}), 400

    project = get_project_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    update_project(project_id, name, manager_id, topic, deadline, status, image, description)
    return jsonify({'message': 'Project updated successfully'}), 200 
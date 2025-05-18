from flask import Blueprint, request, jsonify
from models.models import get_all_projects, create_project, get_project_by_id, update_project

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    projects = get_all_projects()
    projects_list = [dict(project) for project in projects]
    return jsonify(projects_list), 200

@projects_bp.route('/projects', methods=['POST'])
def add_project():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        name = data.get('name')
        manager_id = data.get('manager_id')
        topic = data.get('topic')
        deadline = data.get('deadline')
        status = data.get('status', 'active')  # Default status
        image = data.get('image')
        description = data.get('description')

        if not name:
            return jsonify({'error': 'Project name is required'}), 400
        if not manager_id:
            return jsonify({'error': 'Manager ID is required'}), 400

        # Ensure manager_id is an integer
        try:
            manager_id = int(manager_id)
        except (TypeError, ValueError):
            return jsonify({'error': 'Manager ID must be a valid number'}), 400

        create_project(name, manager_id, topic, deadline, status, image, description)
        return jsonify({
            'message': 'Project created successfully',
            'project': {
                'name': name,
                'manager_id': manager_id,
                'topic': topic,
                'deadline': deadline,
                'status': status,
                'image': image,
                'description': description
            }
        }), 201
    except Exception as e:
        return jsonify({'error': f'Failed to create project: {str(e)}'}), 500

@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = get_project_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    projectd = [dict(project)]
    return jsonify(projectd), 200

@projects_bp.route('/projects/<int:project_id>', methods=['PUT'])
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
from flask import Blueprint, request, jsonify
from flask_security import auth_required, current_user
from app.services.project_service import (
    create_project, add_project_member, 
    get_user_projects, get_project_by_id
)
from app.extensions import db

project_bp = Blueprint('project', __name__)

@project_bp.route('/', methods=['GET'])
@auth_required()
def list_projects():
    projects = get_user_projects(current_user.id)
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'created_at': p.created_at.isoformat()
    } for p in projects])

@project_bp.route('/', methods=['POST'])
@auth_required()
def create_new_project():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    
    if not name:
        return jsonify({'error': 'Project name is required'}), 400
    
    project = create_project(name, description, current_user.id)
    return jsonify({
        'id': project.id,
        'name': project.name,
        'description': project.description
    }), 201

@project_bp.route('/<int:project_id>', methods=['GET'])
@auth_required()
def get_project(project_id):
    project = get_project_by_id(project_id, current_user.id)
    if not project:
        return jsonify({'error': 'Project not found or access denied'}), 404
    
    return jsonify({
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'created_by': project.created_by,
        'created_at': project.created_at.isoformat()
    })

@project_bp.route('/<int:project_id>/members', methods=['POST'])
@auth_required()
def add_member(project_id):
    data = request.get_json()
    user_id = data.get('user_id')
    role = data.get('role', 'member')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    project = get_project_by_id(project_id, current_user.id)
    if not project:
        return jsonify({'error': 'Project not found or access denied'}), 404
    
    # Check if current user has permission to add members
    member = next((m for m in project.members if m.user_id == current_user.id), None)
    if not member or member.role not in ['admin', 'owner']:
        return jsonify({'error': 'Permission denied'}), 403
    
    member = add_project_member(project_id, user_id, role)
    return jsonify({
        'id': member.id,
        'project_id': member.project_id,
        'user_id': member.user_id,
        'role': member.role
    }), 201
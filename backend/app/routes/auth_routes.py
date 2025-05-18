from flask import Blueprint, request, jsonify, current_app
from flask_security import login_user, logout_user, current_user
from app.services.auth_service import register_user
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if not all([email, password, name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user, error = register_user(email, password, name)
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = current_app.user_datastore.get_user(email)
    if not user or not user.verify_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    login_user(user)
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name
        }
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify({
        'id': current_user.id,
        'email': current_user.email,
        'name': current_user.name
    })
from flask import Blueprint, request, jsonify
from flask_security import auth_required, current_user
from app.services.notification_service import (
    get_user_notifications, mark_notification_as_read
)

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/', methods=['GET'])
@auth_required()
def list_notifications():
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    notifications = get_user_notifications(current_user.id, unread_only)
    return jsonify([{
        'id': n.id,
        'content': n.content,
        'is_read': n.is_read,
        'type': n.notification_type,
        'reference_id': n.reference_id,
        'created_at': n.created_at.isoformat()
    } for n in notifications])

@notification_bp.route('/<int:notification_id>/read', methods=['PUT'])
@auth_required()
def mark_as_read(notification_id):
    notification = mark_notification_as_read(notification_id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    
    return jsonify({
        'id': notification.id,
        'is_read': notification.is_read
    })


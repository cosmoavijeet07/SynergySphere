from flask_security import current_user
from functools import wraps
from flask import jsonify

def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({"msg": "Unauthorized"}), 401
            if not any(role in current_user.get_role_names() for role in roles):
                return jsonify({"msg": "Forbidden"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

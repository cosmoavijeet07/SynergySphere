from .auth_routes import auth_bp
from .project_routes import project_bp
from .task_routes import task_bp
from .notification_routes import notification_bp

__all__ = ['auth_bp', 'project_bp', 'task_bp', 'notification_bp']
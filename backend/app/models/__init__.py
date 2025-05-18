from .user import User, Role, user_datastore
from .project import Project, ProjectMember
from .task import Task, TaskAssignment, Comment
from .notification import Notification
from flask_security import SQLAlchemyUserDatastore

# Initialize user_datastore
user_datastore = None

__all__ = [
    'User', 'Role', 'user_datastore',
    'Project', 'ProjectMember',
    'Task', 'TaskAssignment', 'Comment',
    'Notification'
]
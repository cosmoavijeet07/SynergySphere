# app/models/user.py
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

# Define models
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    notification_preferences = db.Column(db.JSON, default=lambda: {
        'email_notifications': True,
        'task_assignments': True,
        'deadline_warnings': True,
        'project_updates': True
    })
    
    roles = db.relationship('Role', secondary=roles_users,
                           backref=db.backref('users', lazy='dynamic'))
    
    # Relationships
    owned_projects = db.relationship('Project', backref='owner', lazy='dynamic')
    assigned_tasks = db.relationship('Task', foreign_keys='Task.assignee_id', backref='assignee', lazy='dynamic')
    created_tasks = db.relationship('Task', foreign_keys='Task.creator_id', backref='creator', lazy='dynamic')
    comments = db.relationship('TaskComment', backref='author', lazy='dynamic')
    expenses = db.relationship('Expense', backref='user', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    
    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)
    
    def get_role_names(self):
        return [role.name for role in self.roles]
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'roles': self.get_role_names(),
            'notification_preferences': self.notification_preferences
        }

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# app/models/project.py
from app import db
from datetime import datetime
from enum import Enum

class ProjectStatus(Enum):
    PLANNING = 'planning'
    ACTIVE = 'active'
    ON_HOLD = 'on_hold'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class ProjectRole(Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    MEMBER = 'member'
    VIEWER = 'viewer'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    budget = db.Column(db.Numeric(10, 2), default=0.00)
    status = db.Column(db.Enum(ProjectStatus), default=ProjectStatus.PLANNING)
    deadline = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = db.relationship('ProjectMember', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    tasks = db.relationship('Task', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    discussions = db.relationship('ProjectDiscussion', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_member_role(self, user_id):
        member = self.members.filter_by(user_id=user_id).first()
        return member.role if member else None
    
    def is_member(self, user_id):
        return self.members.filter_by(user_id=user_id).first() is not None
    
    def can_manage(self, user_id):
        if self.owner_id == user_id:
            return True
        member = self.members.filter_by(user_id=user_id).first()
        return member and member.role in [ProjectRole.ADMIN, ProjectRole.MANAGER]
    
    def to_dict(self, include_members=False):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'budget': float(self.budget) if self.budget else 0.0,
            'status': self.status.value,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'task_count': self.tasks.count(),
            'member_count': self.members.count()
        }
        
        if include_members:
            data['members'] = [member.to_dict() for member in self.members]
        
        return data

class ProjectMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.Enum(ProjectRole), default=ProjectRole.MEMBER)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    permissions = db.Column(db.JSON, default=lambda: {
        'can_create_tasks': True,
        'can_edit_tasks': True,
        'can_delete_tasks': False,
        'can_manage_members': False,
        'can_edit_project': False
    })
    
    # Relationships
    user = db.relationship('User', backref='project_memberships')
    
    __table_args__ = (db.UniqueConstraint('project_id', 'user_id'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'user_name': self.user.name,
            'user_email': self.user.email,
            'role': self.role.value,
            'joined_at': self.joined_at.isoformat(),
            'permissions': self.permissions
        }

# app/models/task.py
from app import db
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    BLOCKED = 'blocked'

class TaskPriority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    URGENT = 'urgent'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.TODO)
    priority = db.Column(db.Enum(TaskPriority), default=TaskPriority.MEDIUM)
    priority_score = db.Column(db.Float, default=0.0)
    due_date = db.Column(db.DateTime)
    estimated_effort = db.Column(db.Integer)  # in hours
    actual_effort = db.Column(db.Integer)     # in hours
    budget_allocated = db.Column(db.Numeric(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    dependencies = db.relationship('TaskDependency', 
                                 foreign_keys='TaskDependency.task_id',
                                 backref='task', lazy='dynamic')
    dependent_tasks = db.relationship('TaskDependency',
                                    foreign_keys='TaskDependency.depends_on_task_id',
                                    backref='dependency', lazy='dynamic')
    comments = db.relationship('TaskComment', backref='task', lazy='dynamic', cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='task', lazy='dynamic')
    
    def calculate_priority_score(self):
        """Calculate dynamic priority score based on various factors"""
        score = 0.0
        
        # Base priority score
        priority_weights = {
            TaskPriority.LOW: 1.0,
            TaskPriority.MEDIUM: 2.0,
            TaskPriority.HIGH: 3.0,
            TaskPriority.URGENT: 4.0
        }
        score += priority_weights.get(self.priority, 2.0)
        
        # Due date urgency
        if self.due_date:
            days_until_due = (self.due_date - datetime.utcnow()).days
            if days_until_due <= 0:
                score += 5.0  # Overdue
            elif days_until_due <= 1:
                score += 3.0  # Due today/tomorrow
            elif days_until_due <= 7:
                score += 2.0  # Due this week
        
        # Dependencies factor
        blocking_count = self.dependent_tasks.count()
        score += blocking_count * 0.5
        
        self.priority_score = score
        return score
    
    def get_dependencies(self):
        return [dep.depends_on_task_id for dep in self.dependencies]
    
    def to_dict(self, include_comments=False):
        data = {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'assignee_id': self.assignee_id,
            'assignee_name': self.assignee.name if self.assignee else None,
            'creator_id': self.creator_id,
            'creator_name': self.creator.name if self.creator else None,
            'status': self.status.value,
            'priority': self.priority.value,
            'priority_score': self.priority_score,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'estimated_effort': self.estimated_effort,
            'actual_effort': self.actual_effort,
            'budget_allocated': float(self.budget_allocated) if self.budget_allocated else 0.0,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'dependencies': self.get_dependencies(),
            'comments_count': self.comments.count()
        }
        
        if include_comments:
            data['comments'] = [comment.to_dict() for comment in self.comments.order_by(TaskComment.created_at)]
        
        return data

class TaskDependency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    depends_on_task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    dependency_type = db.Column(db.String(50), default='finish_to_start')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('task_id', 'depends_on_task_id'),)

class TaskComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('task_comment.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Self-referential relationship for threading
    replies = db.relationship('TaskComment', backref=db.backref('parent', remote_side=[id]))
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'user_name': self.author.name,
            'message': self.message,
            'parent_comment_id': self.parent_comment_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'replies_count': len(self.replies)
        }

# app/models/discussion.py
from app import db
from datetime import datetime

class ProjectDiscussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='discussions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'user_name': self.user.name,
            'title': self.title,
            'message': self.message,
            'is_pinned': self.is_pinned,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# app/models/expense.py
from app import db
from datetime import datetime

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    expense_date = db.Column(db.DateTime, nullable=False)
    receipt_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'user_name': self.user.name,
            'amount': float(self.amount),
            'category': self.category,
            'description': self.description,
            'expense_date': self.expense_date.isoformat(),
            'receipt_url': self.receipt_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# app/models/notification.py
from app import db
from datetime import datetime
from enum import Enum

class NotificationType(Enum):
    TASK_ASSIGNED = 'task_assigned'
    TASK_COMPLETED = 'task_completed'
    DEADLINE_WARNING = 'deadline_warning'
    PROJECT_INVITATION = 'project_invitation'
    COMMENT_ADDED = 'comment_added'
    PROJECT_UPDATE = 'project_update'

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Enum(NotificationType), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    related_entity_type = db.Column(db.String(50))  # 'project', 'task', etc.
    related_entity_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type.value,
            'title': self.title,
            'message': self.message,
            'is_read': self.is_read,
            'related_entity_type': self.related_entity_type,
            'related_entity_id': self.related_entity_id,
            'created_at': self.created_at.isoformat()
        }

# app/models/analytics.py
from app import db
from datetime import datetime

class AnalyticsEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    event_type = db.Column(db.String(100), nullable=False)
    event_data = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(100))
    
    # Relationships
    user = db.relationship('User', backref='analytics_events')
    project = db.relationship('Project', backref='analytics_events')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'event_type': self.event_type,
            'event_data': self.event_data,
            'timestamp': self.timestamp.isoformat(),
            'session_id': self.session_id
        }

from datetime import datetime
from app.extensions import db
from flask_security import UserMixin, RoleMixin
import uuid

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False,
                             default=lambda: str(uuid.uuid4()))
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    roles = db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users', lazy='dynamic'))
    
    projects = db.relationship('ProjectMember', back_populates='user')
    assigned_tasks = db.relationship('TaskAssignment', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    notifications = db.relationship('Notification', back_populates='user')

user_datastore = None  # Will be initialized in app factory
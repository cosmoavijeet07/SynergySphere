from datetime import datetime
from app.extensions import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    members = db.relationship('ProjectMember', back_populates='project')
    tasks = db.relationship('Task', back_populates='project')

class ProjectMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(50), default='member')  # 'member', 'admin', 'owner'
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    project = db.relationship('Project', back_populates='members')
    user = db.relationship('User', back_populates='projects')
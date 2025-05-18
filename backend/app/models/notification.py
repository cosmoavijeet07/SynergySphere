from datetime import datetime
from app.extensions import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notification_type = db.Column(db.String(50))  # 'task_assignment', 'due_date', 'mention', etc.
    reference_id = db.Column(db.Integer)  # ID of the related entity (task, project, etc.)
    
    user = db.relationship('User', back_populates='notifications')
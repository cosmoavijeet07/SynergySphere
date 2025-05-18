from datetime import datetime
from app.extensions import db, mail
from app.models import Notification
from flask_mail import Message
from flask import render_template, current_app
from datetime import datetime
from app.extensions import db, mail
from app.models import Notification
from flask_mail import Message
from flask import render_template, current_app

def create_notification(user_id, content, notification_type, reference_id=None):
    notification = Notification(
        user_id=user_id,
        content=content,
        notification_type=notification_type,
        reference_id=reference_id
    )
    db.session.add(notification)
    db.session.commit()
    return notification

def send_email_notification(to, subject, template, **kwargs):
    msg = Message(
        subject,
        recipients=[to],
        html=render_template(f'email/{template}', **kwargs)
    )
    mail.send(msg)

def get_user_notifications(user_id, unread_only=False):
    query = Notification.query.filter_by(user_id=user_id)
    if unread_only:
        query = query.filter_by(is_read=False)
    return query.order_by(Notification.created_at.desc()).all()

def mark_notification_as_read(notification_id):
    notification = Notification.query.get(notification_id)
    if notification:
        notification.is_read = True
        db.session.commit()
    return notification
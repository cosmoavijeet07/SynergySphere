from celery import Celery
from celery.schedules import crontab
from app.extensions import db, mail, celery
from app.models import Task, User, Notification
from app.services.notification_service import create_notification
from datetime import datetime, timedelta
from flask_mail import Message
from flask import render_template, current_app


@celery.task
def send_daily_task_reminders():
    """Send daily email reminders for tasks due today or overdue"""
    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    
    # Get tasks due today or overdue
    tasks = Task.query.filter(
        Task.due_date >= start_of_day,
        Task.due_date < end_of_day,
        Task.status != 'done'
    ).all()
    
    # Group tasks by assignee
    user_tasks = {}
    for task in tasks:
        for assignment in task.assignments:
            if assignment.user_id not in user_tasks:
                user_tasks[assignment.user_id] = []
            user_tasks[assignment.user_id].append(task)
    
    # Send emails
    for user_id, tasks in user_tasks.items():
        user = User.query.get(user_id)
        if not user or not user.email:
            continue
        
        msg = Message(
            "Your Daily Task Reminder",
            recipients=[user.email],
            html=render_template('email/task_reminder.html', 
                              user=user, 
                              tasks=tasks,
                              now=now)
        )
        
        try:
            mail.send(msg)
            current_app.logger.info(f"Sent task reminder to {user.email}")
        except Exception as e:
            current_app.logger.error(f"Failed to send email to {user.email}: {str(e)}")
@celery.task
def send_daily_digest():
    """Send daily digest email at 9:00 AM IST with overview of tasks and notifications"""
    from datetime import datetime, timedelta
    from app.models import User, Task, Notification
    from app.services.notification_service import send_email_notification
    
    # Calculate time ranges (IST is UTC+5:30)
    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    three_days_later = end_of_day + timedelta(days=3)
    
    # Get all active users
    users = User.query.filter(User.active == True).all()
    
    for user in users:
        if not user.email:
            continue
        
        # Get tasks due today
        tasks_due_today = Task.query.join(Task.assignments).filter(
            TaskAssignment.user_id == user.id,
            Task.due_date >= start_of_day,
            Task.due_date < end_of_day,
            Task.status != 'done'
        ).all()
        
        # Get upcoming tasks (next 3 days)
        upcoming_tasks = Task.query.join(Task.assignments).filter(
            TaskAssignment.user_id == user.id,
            Task.due_date >= end_of_day,
            Task.due_date < three_days_later,
            Task.status != 'done'
        ).all()
        
        # Get recent unread notifications
        recent_notifications = Notification.query.filter(
            Notification.user_id == user.id,
            Notification.is_read == False,
            Notification.created_at >= now - timedelta(days=1)
        ).order_by(Notification.created_at.desc()).limit(5).all()
        
        # Only send if there's something to report
        if tasks_due_today or upcoming_tasks or recent_notifications:
            try:
                send_email_notification(
                    to=user.email,
                    subject=f"Your SynergySphere Daily Digest - {now.strftime('%m/%d/%Y')}",
                    template='daily_digest.html',
                    user=user,
                    tasks_due_today=tasks_due_today,
                    upcoming_tasks=upcoming_tasks,
                    recent_notifications=recent_notifications,
                    now=now,
                    app_link='https://app.synergysphere.example.com',
                    preferences_link='https://app.synergysphere.example.com/settings/notifications'
                )
                current_app.logger.info(f"Sent daily digest to {user.email}")
            except Exception as e:
                current_app.logger.error(f"Failed to send daily digest to {user.email}: {str(e)}")
@celery.task
def check_for_upcoming_deadlines():
    """Check for tasks due in the next 24 hours and create notifications"""
    now = datetime.utcnow()
    deadline = now + timedelta(days=1)
    
    tasks = Task.query.filter(
        Task.due_date > now,
        Task.due_date <= deadline,
        Task.status != 'done'
    ).all()
    
    for task in tasks:
        for assignment in task.assignments:
            create_notification(
                user_id=assignment.user_id,
                content=f"Task '{task.title}' is due soon (by {task.due_date})",
                notification_type='due_date_reminder',
                reference_id=task.id
            )
    
    db.session.commit()

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Schedule daily task reminders at 9:00 AM IST (3:30 UTC)
    sender.add_periodic_task(
        crontab(hour=3, minute=30),
        send_daily_task_reminders.s(),
        name='daily-task-reminders'
    )
    # Schedule daily digest at 9:15 AM IST (3:45 UTC)
    sender.add_periodic_task(
        crontab(hour=3, minute=45),
        send_daily_digest.s(),
        name='daily-digest'
    )
    # Check for upcoming deadlines every 6 hours
    sender.add_periodic_task(
        timedelta(hours=6),
        check_for_upcoming_deadlines.s(),
        name='check-upcoming-deadlines'
    )
import google.generativeai as genai
from app.extensions import db
from app.models import Task, Project
from datetime import datetime, timedelta
from app.config import Config
from flask import current_app

genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_task_suggestions(project_id):
    project = Project.query.get(project_id)
    if not project:
        return None
    
    tasks = Task.query.filter_by(project_id=project_id).all()
    members = [m.user for m in project.members]
    
    prompt = f"""
    Analyze this project and suggest optimal task assignments:
    
    Project: {project.name}
    Description: {project.description}
    
    Current Tasks:
    {[f"{t.title} (Status: {t.status})" for t in tasks]}
    
    Team Members: {[m.name for m in members]}
    
    Suggest:
    1. Which tasks should be prioritized
    2. Optimal assignment of tasks to team members based on workload
    3. Any potential bottlenecks or risks
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        current_app.logger.error(f"AI service error: {str(e)}")
        return None

def summarize_comments(task_id):
    task = Task.query.get(task_id)
    if not task or not task.comments:
        return None
    
    comments = [f"{c.user.name}: {c.content}" for c in task.comments]
    prompt = f"""
    Summarize these task discussion comments into key points and action items:
    
    Task: {task.title}
    
    Comments:
    {comments}
    
    Provide:
    1. A concise summary of the discussion
    2. Clear action items (if any)
    3. Any decisions made
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        current_app.logger.error(f"AI service error: {str(e)}")
        return None
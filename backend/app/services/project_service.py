from datetime import datetime
from app.extensions import db
from app.models import Project, ProjectMember

def create_project(name, description, created_by):
    project = Project(
        name=name,
        description=description,
        created_by=created_by
    )
    db.session.add(project)
    db.session.commit()
    
    # Add creator as project owner
    add_project_member(project.id, created_by, 'owner')
    
    return project

def add_project_member(project_id, user_id, role='member'):
    member = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        role=role
    )
    db.session.add(member)
    db.session.commit()
    return member

def get_user_projects(user_id):
    return Project.query.join(ProjectMember).filter(
        ProjectMember.user_id == user_id
    ).all()

def get_project_by_id(project_id, user_id=None):
    query = Project.query.filter_by(id=project_id)
    if user_id:
        query = query.join(ProjectMember).filter(
            ProjectMember.user_id == user_id
        )
    return query.first()
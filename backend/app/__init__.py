from flask import Flask
from flask_migrate import Migrate
from .config import Config
from .extensions import db, security, mail, ContextTask, celery

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Import models after db initialization
    from .models.user import User, Role
    from .models.project import Project, ProjectMember
    from .models.task import Task, TaskAssignment, Comment
    from .models.notification import Notification
    
    # Setup Flask-Security
    from flask_security import SQLAlchemyUserDatastore
    app.user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, app.user_datastore)
    
    mail.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default roles if they don't exist
        if not Role.query.filter_by(name='admin').first():
            app.user_datastore.create_role(name='admin', description='Administrator')
        if not Role.query.filter_by(name='member').first():
            app.user_datastore.create_role(name='member', description='Team Member')
        db.session.commit()
    
    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.project_routes import project_bp
    from .routes.task_routes import task_bp
    from .routes.notification_routes import notification_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    app.register_blueprint(task_bp, url_prefix='/api/tasks')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    
    celery = extensions.celery
    celery.conf.update(
     broker_url= app.config["CELERY_BROKER_URL"],
     result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = ContextTask
    
    return app, celery
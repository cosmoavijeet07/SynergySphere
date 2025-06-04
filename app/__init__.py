from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import config

db = SQLAlchemy()
migrate = Migrate()
security = Security()
jwt = JWTManager()
mail = Mail()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)
    
    # Import models before initializing security
    from app.models import User, Role
    from app.models.user import user_datastore
    
    # Initialize Flask-Security
    security.init_app(app, user_datastore)
    
    # Register blueprints
    # from app.api.auth import auth_bp
    # from app.api.projects import projects_bp
    # from app.api.tasks import tasks_bp
    # from app.api.users import users_bp
    # from app.api.analytics import analytics_bp
    
    # app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # app.register_blueprint(projects_bp, url_prefix='/api/projects')
    # app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    # app.register_blueprint(users_bp, url_prefix='/api/users')
    # app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    
    # Create default roles and admin user
    @app.before_first_request
    def create_default_data():
        db.create_all()
        
        # Create roles if they don't exist
        if not user_datastore.find_role('admin'):
            user_datastore.create_role(name='admin', description='Administrator')
        if not user_datastore.find_role('manager'):
            user_datastore.create_role(name='manager', description='Project Manager')
        if not user_datastore.find_role('member'):
            user_datastore.create_role(name='member', description='Team Member')
        
        # Create admin user if doesn't exist
        if not user_datastore.find_user(email='admin@synergysphere.com'):
            user_datastore.create_user(
                email='admin@synergysphere.com',
                password='admin123',
                name='System Administrator',
                active=True,
                roles=['admin']
            )
        
        db.session.commit()
    
    return app

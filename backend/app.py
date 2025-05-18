from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.tasks import tasks_bp

app = Flask(__name__)

# Configure CORS to allow requests from React app
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Register blueprints with /api prefix
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(projects_bp, url_prefix='/api')
app.register_blueprint(tasks_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
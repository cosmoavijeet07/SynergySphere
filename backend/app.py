from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.tasks import tasks_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(tasks_bp)

if __name__ == '__main__':
    app.run(debug=True) 
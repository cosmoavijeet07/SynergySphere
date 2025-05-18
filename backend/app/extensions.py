from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_mail import Mail
from celery import Celery
from flask import current_app

db = SQLAlchemy()
security = Security()
mail = Mail()

from celery import Celery
from flask import current_app as app

celery = Celery('application jobs')

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__(*args, **kwargs)
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///synergysphere.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Security
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'your-password-salt')
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = True
    SECURITY_USERNAME_ENABLE = False
    SECURITY_USERNAME_REQUIRED = False
    
    # Flask-Mail
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'false').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'no-reply@synergysphere.com'
    
    # Celery
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    
    # Gemini AI
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Timezone
    TIMEZONE = 'Asia/Kolkata'
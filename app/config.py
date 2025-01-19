import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'instance', 'mccrm.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLite specific settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False}
    }
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # Upload config
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Security
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    
    # Admin
    FLASK_ADMIN_SWATCH = 'cerulean' 
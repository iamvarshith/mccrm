from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from app.config import Config
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

# Add this user_loader function
@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None
    from app.models.models import Agent
    return Agent.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Set up login manager
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        # Import models
        from app.models import Agent, Client, Dependent, GlobalPolicy, UserPolicy, AssignedPolicy
        
        # Create tables if they don't exist
        db.create_all()
        
        # Register blueprints - import only once
        from app.routes.auth import auth_bp
        from app.routes.dashboard import dashboard_bp
        from app.routes.clients import clients_bp
        from app.routes.policies import policy_bp
        from app.routes.assigned_policies import assigned_policy_bp

        # Register each blueprint only once
        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(clients_bp)
        app.register_blueprint(policy_bp)
        app.register_blueprint(assigned_policy_bp)

        # Error handlers
        from app.errors import register_error_handlers
        register_error_handlers(app)

    return app 
import os
from app import create_app, db
from app.models.models import Agent, GlobalPolicy, UserPolicy, Client, Dependent, AssignedPolicy

def init_db():
    app = create_app()
    
    with app.app_context():
        # Create database directory if it doesn't exist
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
        os.makedirs(db_path, exist_ok=True)
        
        print("Creating database tables...")
        db.create_all()
        
        # Check if admin user exists
        admin = Agent.query.filter_by(email='admin@example.com').first()
        if not admin:
            print("Creating admin user...")
            admin = Agent(
                email='admin@example.com',
                name='Admin User',
                is_admin=True
            )
            admin.password = 'admin123'  # In production, use proper password hashing
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        
        print("Database initialization completed!")

if __name__ == '__main__':
    # Delete existing database file
    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'mccrm.db')
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed existing database: {db_file}")
    
    init_db() 
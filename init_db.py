from app import create_app, db
from app.models import Agent, Client, Dependent, GlobalPolicy, UserPolicy, AssignedPolicy
import os

def init_database():
    app = create_app()
    with app.app_context():
        print("Starting database initialization...")
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Ensure the instance directory exists
        instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
        os.makedirs(instance_path, exist_ok=True)
        
        print("Dropping all existing tables...")
        db.drop_all()
        
        print("Creating all tables...")
        db.create_all()
        
        # Print all created tables
        print("\nCreated tables:")
        for table in db.metadata.tables:
            print(f"- {table}")
        
        # Create a test admin user
        admin = Agent(
            email='admin@example.com',
            name='Admin User',
            is_admin=True,
            password='admin123'  # You should hash this in production
        )
        
        try:
            db.session.add(admin)
            db.session.commit()
            print("\nAdmin user created successfully!")
        except Exception as e:
            print(f"\nError creating admin user: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    init_database()

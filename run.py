from app import create_app, db
from app.models import Agent, Client, Dependent, GlobalPolicy, UserPolicy, AssignedPolicy

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    try:
        with app.app_context():
            print("Dropping all tables...")
            db.drop_all()
            print("Creating all tables...")
            db.create_all()
            print("Tables created:")
            for table in db.metadata.tables.keys():
                print(f"- {table}")
            print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")

@app.cli.command("check-config")
def check_config():
    """Check the application configuration."""
    print("Checking configuration...")
    print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"SECRET_KEY set: {'Yes' if app.config['SECRET_KEY'] else 'No'}")
    print(f"Debug mode: {app.config['DEBUG']}")

if __name__ == '__main__':
    app.run(debug=True) 
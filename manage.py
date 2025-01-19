from flask.cli import FlaskGroup
from app import create_app, db
from app.models import Agent, Client, Dependent, GlobalPolicy, UserPolicy, AssignedPolicy

cli = FlaskGroup(create_app=create_app)

@cli.command("create-tables")
def create_tables():
    """Create database tables."""
    db.create_all()
    print("Tables created successfully!")

@cli.command("drop-tables")
def drop_tables():
    """Drop all database tables."""
    db.drop_all()
    print("Tables dropped successfully!")

@cli.command("recreate-tables")
def recreate_tables():
    """Recreate all database tables."""
    db.drop_all()
    db.create_all()
    print("Tables recreated successfully!")

if __name__ == "__main__":
    cli() 
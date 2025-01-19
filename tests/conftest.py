import pytest
from app import create_app, db
from app.models import Agent, Client, GlobalPolicy, UserPolicy
from flask_login import login_user

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })
    
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()
        
        # Create test agent
        agent = Agent(
            email='test@example.com',
            password='hashed_password',
            name='Test Agent'
        )
        db.session.add(agent)
        
        # Create test global policy
        global_policy = GlobalPolicy(
            name='Test Global Policy',
            category='Health',
            provider='Test Provider'
        )
        db.session.add(global_policy)
        
        db.session.commit()
        
        yield db
        
        db.drop_all()

@pytest.fixture
def auth_client(client, init_database):
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    return client 
from datetime import datetime, timedelta
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from app import db

# Make sure db is properly imported
if not db:
    raise ImportError("Database instance not found. Check your imports.")

class Agent(UserMixin, db.Model):
    """Agent model for storing agent/user related details"""
    __tablename__ = 'agent'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    custom_policies = db.relationship('UserPolicy', backref='agent', lazy=True)
    clients = db.relationship('Client', backref='agent', lazy=True)
    assigned_policies = db.relationship('AssignedPolicy', backref='agent', lazy=True)

    def __repr__(self):
        return f'<Agent {self.email}>'

class GlobalPolicy(db.Model):
    """Global Policy model for storing system-wide policies"""
    __tablename__ = 'global_policy'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    provider = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_group_policy = db.Column(db.Boolean, default=False)
    document_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    assigned_policies = db.relationship('AssignedPolicy', 
                                      backref='global_policy',
                                      lazy=True,
                                      foreign_keys='AssignedPolicy.global_policy_id')

    def __repr__(self):
        return f'<GlobalPolicy {self.name}>'

class UserPolicy(db.Model):
    """User Policy model for storing agent-specific policies"""
    __tablename__ = 'user_policy'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    provider = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_group_policy = db.Column(db.Boolean, default=False)
    document_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    
    # Add these new fields for client policies
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    policy_number = db.Column(db.String(50))
    sum_assured = db.Column(db.Float)
    premium_amount = db.Column(db.Float)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # Relationships
    client = db.relationship('Client', backref='custom_policies', lazy=True)
    assigned_policies = db.relationship('AssignedPolicy', 
                                      backref='user_policy',
                                      lazy=True,
                                      foreign_keys='AssignedPolicy.user_policy_id')
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<UserPolicy {self.name}>'

class Client(db.Model):
    """Client model for storing client related details"""
    __tablename__ = 'client'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    
    # Relationships
    dependents = db.relationship('Dependent', backref='client', lazy=True, cascade='all, delete-orphan')
    assigned_policies = db.relationship('AssignedPolicy', backref='client', lazy=True)

    def __repr__(self):
        return f'<Client {self.name}>'

class Dependent(db.Model):
    """Dependent model for storing client dependents"""
    __tablename__ = 'dependent'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    def __repr__(self):
        return f'<Dependent {self.name}>'

class AssignedPolicy(db.Model):
    """Assigned Policy model for storing policies assigned to clients"""
    __tablename__ = 'assigned_policy'
    
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    premium_amount = db.Column(db.Float, nullable=False)
    payment_cycle_months = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    global_policy_id = db.Column(db.Integer, db.ForeignKey('global_policy.id'))
    user_policy_id = db.Column(db.Integer, db.ForeignKey('user_policy.id'))

    def __repr__(self):
        return f'<AssignedPolicy {self.id}>'

    def get_policy(self):
        """Returns the associated policy (either global or user policy)"""
        return self.global_policy or self.user_policy

    @property
    def expiry_date(self):
        return self.start_date + timedelta(days=self.duration_months * 30)

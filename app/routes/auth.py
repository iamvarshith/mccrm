from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Agent
from app import db, bcrypt

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_bp.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        agent = Agent.query.filter_by(email=email).first()
        if agent and bcrypt.check_password_hash(agent.password, password):
            login_user(agent, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard_bp.index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_bp.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if Agent.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth_bp.register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        agent = Agent(email=email, password=hashed_password, name=name)
        
        db.session.add(agent)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth_bp.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        if request.form.get('password'):
            current_user.password = bcrypt.generate_password_hash(
                request.form.get('password')).decode('utf-8')
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('auth_bp.profile'))
    
    return render_template('auth/profile.html')

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import Client, Dependent
from app import db

clients_bp = Blueprint('clients_bp', __name__)

@clients_bp.route('/clients')
@login_required
def list():
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    
    query = Client.query
    if search:
        query = query.filter(Client.name.ilike(f'%{search}%'))
    
    clients = query.paginate(page=page, per_page=10)
    return render_template('clients/list.html', clients=clients, search=search)

@clients_bp.route('/clients/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        client = Client(
            name=request.form['name'],
            phone=request.form['phone'],
            address=request.form['address'],
            age=request.form.get('age', type=int),
            sex=request.form['sex'],
            agent_id=current_user.id
        )
        db.session.add(client)
        db.session.commit()
        flash('Client created successfully', 'success')
        return redirect(url_for('clients_bp.list'))
    
    return render_template('clients/form.html')

@clients_bp.route('/clients/<int:id>')
@login_required
def detail(id):
    client = Client.query.get_or_404(id)
    return render_template('clients/detail.html', client=client)

@clients_bp.route('/clients/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    client = Client.query.get_or_404(id)
    
    if request.method == 'POST':
        client.name = request.form['name']
        client.phone = request.form['phone']
        client.address = request.form['address']
        client.age = request.form.get('age', type=int)
        client.sex = request.form['sex']
        db.session.commit()
        flash('Client updated successfully', 'success')
        return redirect(url_for('clients_bp.detail', id=client.id))
    
    return render_template('clients/form.html', client=client)

# Add these new routes for dependents
@clients_bp.route('/clients/<int:id>/dependents/add', methods=['POST'])
@login_required
def add_dependent(id):
    client = Client.query.get_or_404(id)
    
    dependent = Dependent(
        name=request.form['name'],
        relationship=request.form['relationship'],
        age=request.form.get('age', type=int),
        client_id=client.id
    )
    db.session.add(dependent)
    db.session.commit()
    flash('Dependent added successfully', 'success')
    return redirect(url_for('clients_bp.detail', id=client.id))

@clients_bp.route('/clients/dependents/<int:id>/delete', methods=['POST'])
@login_required
def delete_dependent(id):
    dependent = Dependent.query.get_or_404(id)
    client_id = dependent.client_id
    db.session.delete(dependent)
    db.session.commit()
    flash('Dependent removed successfully', 'success')
    return redirect(url_for('clients_bp.detail', id=client_id)) 
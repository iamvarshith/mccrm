from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import Client, Dependent
from app import db
from app.utils import check_owner, paginate, search_filter

# Change the blueprint name to be unique
clients_bp = Blueprint('clients_bp', __name__, url_prefix='/clients')

@clients_bp.route('/')
@login_required
def list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Client.query.filter_by(agent_id=current_user.id)
    if search:
        query = search_filter(query, Client, search, ['name', 'phone'])
    
    clients = paginate(query.order_by(Client.created_at.desc()), page)
    return render_template('clients/list.html', clients=clients, search=search)

@clients_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        client = Client(
            name=request.form['name'],
            phone=request.form['phone'],
            age=request.form['age'],
            sex=request.form['sex'],
            address=request.form['address'],
            agent_id=current_user.id
        )
        db.session.add(client)
        db.session.commit()
        flash('Client added successfully', 'success')
        return redirect(url_for('clients_bp.list'))
    
    return render_template('clients/form.html')

@clients_bp.route('/<int:id>')
@login_required
def detail(id):
    client = Client.query.get_or_404(id)
    check_owner(client)
    return render_template('clients/detail.html', client=client)

@clients_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    client = Client.query.get_or_404(id)
    check_owner(client)
    
    if request.method == 'POST':
        client.name = request.form['name']
        client.phone = request.form['phone']
        client.age = request.form['age']
        client.sex = request.form['sex']
        client.address = request.form['address']
        db.session.commit()
        flash('Client updated successfully', 'success')
        return redirect(url_for('clients_bp.detail', id=client.id))
    
    return render_template('clients/form.html', client=client) 
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import AssignedPolicy, Client, GlobalPolicy, UserPolicy
from app import db
from app.utils import paginate, search_filter
from datetime import datetime

assigned_policy_bp = Blueprint('assigned_policy_bp', __name__, url_prefix='/assigned-policies')

@assigned_policy_bp.route('/')
@login_required
def list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', 'active')
    
    query = AssignedPolicy.query.filter_by(agent_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    
    if search:
        # Join with Client to search by client name
        query = query.join(Client).filter(Client.name.ilike(f'%{search}%'))
    
    assigned_policies = paginate(query.order_by(AssignedPolicy.created_at.desc()), page)
    
    return render_template('assigned_policies/list.html',
                         assigned_policies=assigned_policies,
                         search=search,
                         status=status)

@assigned_policy_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        # Get the selected policy based on type
        policy_type = request.form['policy_type']
        policy_id = int(request.form['policy_id'])
        
        assigned_policy = AssignedPolicy(
            policy_type=policy_type,
            policy_id=policy_id,
            client_id=int(request.form['client_id']),
            agent_id=current_user.id,
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            duration_months=int(request.form['duration_months']),
            payment_cycle_months=int(request.form['payment_cycle_months']),
            premium_amount=float(request.form['premium_amount']),
            status='active'
        )
        
        db.session.add(assigned_policy)
        db.session.commit()
        flash('Policy assigned successfully', 'success')
        return redirect(url_for('assigned_policy_bp.list'))
    
    # Get available policies and clients for the form
    global_policies = GlobalPolicy.query.all()
    user_policies = UserPolicy.query.filter_by(agent_id=current_user.id).all()
    clients = Client.query.filter_by(agent_id=current_user.id).all()
    
    return render_template('assigned_policies/form.html',
                         global_policies=global_policies,
                         user_policies=user_policies,
                         clients=clients)

@assigned_policy_bp.route('/<int:id>')
@login_required
def detail(id):
    assigned_policy = AssignedPolicy.query.filter_by(
        id=id, agent_id=current_user.id
    ).first_or_404()
    
    return render_template('assigned_policies/detail.html',
                         assigned_policy=assigned_policy)

@assigned_policy_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    assigned_policy = AssignedPolicy.query.filter_by(
        id=id, agent_id=current_user.id
    ).first_or_404()
    
    if request.method == 'POST':
        assigned_policy.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        assigned_policy.duration_months = int(request.form['duration_months'])
        assigned_policy.payment_cycle_months = int(request.form['payment_cycle_months'])
        assigned_policy.premium_amount = float(request.form['premium_amount'])
        assigned_policy.status = request.form['status']
        
        db.session.commit()
        flash('Assigned policy updated successfully', 'success')
        return redirect(url_for('assigned_policy_bp.detail', id=assigned_policy.id))
    
    return render_template('assigned_policies/form.html',
                         assigned_policy=assigned_policy)

@assigned_policy_bp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    assigned_policy = AssignedPolicy.query.filter_by(
        id=id, agent_id=current_user.id
    ).first_or_404()
    
    assigned_policy.status = 'cancelled'
    db.session.commit()
    flash('Policy cancelled successfully', 'success')
    return redirect(url_for('assigned_policy_bp.list')) 
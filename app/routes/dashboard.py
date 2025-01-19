from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Client, AssignedPolicy
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.sql import extract

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    # Calculate the date 30 days from now
    thirty_days_from_now = datetime.now() + timedelta(days=30)
    
    # Get basic stats
    stats = {
        'total_clients': Client.query.filter_by(agent_id=current_user.id).count(),
        'active_policies': AssignedPolicy.query.filter_by(
            agent_id=current_user.id,
            status='active'
        ).count(),
        'monthly_revenue': AssignedPolicy.query.filter_by(
            agent_id=current_user.id,
            status='active'
        ).with_entities(func.sum(AssignedPolicy.premium_amount)).scalar() or 0,
        'expiring_soon': AssignedPolicy.query.filter(
            AssignedPolicy.agent_id == current_user.id,
            AssignedPolicy.status == 'active'
        ).filter(
            AssignedPolicy.start_date <= thirty_days_from_now
        ).count()
    }
    
    # Get recent clients (last 5)
    recent_clients = Client.query.filter_by(agent_id=current_user.id)\
        .order_by(Client.created_at.desc())\
        .limit(5)\
        .all()
    
    # Get policies expiring soon (next 30 days)
    expiring_policies = AssignedPolicy.query.filter(
        AssignedPolicy.agent_id == current_user.id,
        AssignedPolicy.status == 'active',
        AssignedPolicy.start_date <= thirty_days_from_now
    ).order_by(
        AssignedPolicy.start_date.asc()
    ).limit(5).all()
    
    return render_template('dashboard.html',
                         stats=stats,
                         recent_clients=recent_clients,
                         expiring_policies=expiring_policies,
                         current_time=datetime.now()) 
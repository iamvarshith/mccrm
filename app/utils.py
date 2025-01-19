from functools import wraps
from flask import abort
from flask_login import current_user
from app.config import Config

def check_owner(obj):
    """Check if current user owns the object"""
    if not hasattr(obj, 'agent_id') or obj.agent_id != current_user.id:
        abort(403)

def owner_required(f):
    """Decorator to check resource ownership"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

def paginate(query, page):
    """Paginate query results"""
    return query.paginate(
        page=page, 
        per_page=Config.ITEMS_PER_PAGE,
        error_out=False
    )

def search_filter(query, model, search_term, fields):
    """Apply search filter to query"""
    if not search_term:
        return query
    
    filters = []
    for field in fields:
        attr = getattr(model, field)
        filters.append(attr.ilike(f'%{search_term}%'))
    
    return query.filter(db.or_(*filters))

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function 
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from app.models import Agent, GlobalPolicy, UserPolicy, Client, Dependent, AssignedPolicy  # Import models here

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('auth.login'))
        return super(SecureAdminIndexView, self).index()

def setup_admin(app):
    from app import db  # Move the import here to avoid circular import

    # Ensure the admin instance is created only once
    if not hasattr(app, 'admin'):
        app.admin = Admin(app, 
                          name='Insurance CRM Admin',
                          template_mode='bootstrap4',
                          index_view=SecureAdminIndexView())
        
        # Add model views
        app.admin.add_view(SecureModelView(Agent, db.session))
        app.admin.add_view(SecureModelView(GlobalPolicy, db.session))
        app.admin.add_view(SecureModelView(UserPolicy, db.session))
        app.admin.add_view(SecureModelView(Client, db.session))
        app.admin.add_view(SecureModelView(Dependent, db.session))
        app.admin.add_view(SecureModelView(AssignedPolicy, db.session))
    
    return app.admin 
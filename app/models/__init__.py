from app.models.models import Agent, Client, Dependent, GlobalPolicy, UserPolicy, AssignedPolicy

# This ensures all models are imported when 'app.models' is imported
__all__ = ['Agent', 'Client', 'Dependent', 'GlobalPolicy', 'UserPolicy', 'AssignedPolicy']

import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, send_file
from flask_login import login_required, current_user
from app.models import Policy
from app import db

policy_bp = Blueprint('policy_bp', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

@policy_bp.route('/policies')
@login_required
def list():
    page = request.args.get('page', 1, type=int)
    policies = Policy.query.paginate(page=page, per_page=10)
    return render_template('policies/list.html', policies=policies)

@policy_bp.route('/policies/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('policy_bp.list'))

    if request.method == 'POST':
        policy = Policy(
            name=request.form['name'],
            provider=request.form['provider'],
            category=request.form['category'],
            description=request.form.get('description'),
            is_group_policy=bool(request.form.get('is_group_policy')),
            agent_id=current_user.id
        )
        db.session.add(policy)
        db.session.commit()
        flash('Policy created successfully', 'success')
        return redirect(url_for('policy_bp.list'))
    
    return render_template('policies/form.html')

@policy_bp.route('/policies/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('policy_bp.list'))

    if request.method == 'POST':
        if 'document' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['document']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            policy = Policy.query.get_or_404(request.form['policy_id'])
            
            # Create uploads directory if it doesn't exist
            uploads_dir = os.path.join(current_app.root_path, 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            
            # Save file
            filename = secure_filename(f"policy_{policy.id}_{file.filename}")
            file.save(os.path.join(uploads_dir, filename))
            
            # Update policy
            policy.document_path = filename
            db.session.commit()
            
            flash('Document uploaded successfully', 'success')
            return redirect(url_for('policy_bp.detail', id=policy.id))
        
        flash('Invalid file type. Please upload a PDF.', 'error')
        return redirect(request.url)
    
    policies = Policy.query.all()
    return render_template('policies/upload.html', policies=policies)

@policy_bp.route('/policies/<int:id>/document')
@login_required
def download_doc(id):
    policy = Policy.query.get_or_404(id)
    if not policy.document_path:
        flash('No document available', 'error')
        return redirect(url_for('policy_bp.detail', id=policy.id))
    
    uploads_dir = os.path.join(current_app.root_path, 'uploads')
    return send_file(
        os.path.join(uploads_dir, policy.document_path),
        download_name=policy.document_path,
        as_attachment=True
    ) 
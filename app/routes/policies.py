import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, send_file
from flask_login import login_required, current_user
from app.models import GlobalPolicy, UserPolicy, Client
from app import db
from app.utils import paginate, search_filter
from datetime import datetime

policy_bp = Blueprint('policy_bp', __name__, url_prefix='/policies')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'doc', 'docx'}

@policy_bp.route('/')
@login_required
def list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    # Get global policies
    global_policies = GlobalPolicy.query.paginate(page=page, per_page=10, error_out=False)
    
    # Get user policies
    user_policies = UserPolicy.query.filter_by(client_id=current_user.id).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('policies/list.html',
                         global_policies=global_policies,
                         user_policies=user_policies,
                         search=search)

@policy_bp.route('/upload', methods=['GET', 'POST'])
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
            # Try to find in global policies first
            policy = GlobalPolicy.query.get(request.form['policy_id'])
            if policy is None:
                # If not found, look in user policies
                policy = UserPolicy.query.get_or_404(request.form['policy_id'])
            
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
    
    global_policies = GlobalPolicy.query.all()
    user_policies = UserPolicy.query.filter_by(agent_id=current_user.id).all()
    return render_template('policies/upload.html', 
                         global_policies=global_policies,
                         user_policies=user_policies)

@policy_bp.route('/<int:id>/document')
@login_required
def download_doc(id):
    # Try to find in global policies first
    policy = GlobalPolicy.query.get(id)
    if policy is None:
        # If not found, look in user policies
        policy = UserPolicy.query.filter_by(id=id, agent_id=current_user.id).first_or_404()
    
    if not policy.document_path:
        flash('No document available', 'error')
        return redirect(url_for('policy_bp.detail', id=policy.id))
    
    uploads_dir = os.path.join(current_app.root_path, 'uploads')
    return send_file(
        os.path.join(uploads_dir, policy.document_path),
        download_name=policy.document_path,
        as_attachment=True
    )

@policy_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        try:
            policy = UserPolicy(
                name=request.form['name'],
                category=request.form['category'],
                provider=request.form['provider'],
                description=request.form.get('description', ''),
                policy_number=request.form['policy_number'],
                sum_assured=float(request.form['sum_assured']),
                premium_amount=float(request.form['premium_amount']),
                start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
                end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d').date(),
                client_id=current_user.id,
                agent_id=current_user.id,
                is_active=True
            )

            # Handle file upload
            if 'document' in request.files:
                file = request.files['document']
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{current_user.id}_{file.filename}")
                    upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
                    os.makedirs(upload_folder, exist_ok=True)
                    file.save(os.path.join(upload_folder, filename))
                    policy.document_path = filename

            db.session.add(policy)
            db.session.commit()
            flash('Policy uploaded successfully!', 'success')
            return redirect(url_for('policy_bp.list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error uploading policy: {str(e)}', 'error')

    return render_template('policies/client_upload.html')

@policy_bp.route('/<int:id>')
@login_required
def detail(id):
    # Try to find in global policies first
    policy = GlobalPolicy.query.get(id)
    if policy is None:
        # If not found, look in user policies
        policy = UserPolicy.query.filter_by(id=id, agent_id=current_user.id).first_or_404()
    
    return render_template('policies/detail.html', policy=policy)

@policy_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    policy = UserPolicy.query.filter_by(id=id, agent_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        policy.name = request.form['name']
        policy.category = request.form['category']
        policy.provider = request.form['provider']
        policy.description = request.form['description']
        policy.is_group_policy = bool(request.form.get('is_group_policy'))
        db.session.commit()
        flash('Policy updated successfully', 'success')
        return redirect(url_for('policy_bp.detail', id=policy.id))
    
    return render_template('policies/form.html', policy=policy)

@policy_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    policy = UserPolicy.query.filter_by(id=id, agent_id=current_user.id).first_or_404()
    db.session.delete(policy)
    db.session.commit()
    flash('Policy deleted successfully', 'success')
    return redirect(url_for('policy_bp.list'))

@policy_bp.route('/client/<int:client_id>/upload', methods=['GET', 'POST'])
@login_required
def client_upload(client_id):
    # Verify client belongs to current agent
    client = Client.query.filter_by(id=client_id, agent_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        # Handle policy details
        policy = UserPolicy(
            name=request.form['name'],
            category=request.form['category'],
            provider=request.form['provider'],
            description=request.form.get('description'),
            is_group_policy=False,  # Client policies are individual
            agent_id=current_user.id,
            client_id=client.id,  # Add this field to UserPolicy model
            policy_number=request.form.get('policy_number'),
            sum_assured=float(request.form.get('sum_assured', 0)),
            premium_amount=float(request.form.get('premium_amount', 0)),
            start_date=request.form.get('start_date'),
            end_date=request.form.get('end_date'),
            
        )
        
        # Handle document upload
        if 'document' in request.files:
            file = request.files['document']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"client_{client_id}_policy_{file.filename}")
                uploads_dir = os.path.join(current_app.root_path, 'uploads')
                os.makedirs(uploads_dir, exist_ok=True)
                file.save(os.path.join(uploads_dir, filename))
                policy.document_path = filename
        
        db.session.add(policy)
        db.session.commit()
        
        flash('Policy uploaded successfully', 'success')
        return redirect(url_for('policy_bp.client_policies', client_id=client_id))
    
    return render_template('policies/client_upload.html', client=client)

@policy_bp.route('/client/<int:client_id>/policies')
@login_required
def client_policies(client_id):
    client = Client.query.filter_by(id=client_id, agent_id=current_user.id).first_or_404()
    policies = UserPolicy.query.filter_by(client_id=client_id).all()
    return render_template('policies/client_list.html', client=client, policies=policies)

@policy_bp.route('/client-upload', endpoint='policy_client_upload')
@login_required
def client_upload():
    if request.method == 'POST':
        try:
            # Create new policy
            policy = UserPolicy(
                name=request.form['name'],
                category=request.form['category'],
                provider=request.form['provider'],
                description=request.form.get('description', ''),
                policy_number=request.form['policy_number'],
                sum_assured=float(request.form['sum_assured']),
                premium_amount=float(request.form['premium_amount']),
                start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
                end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d').date(),
                client_id=current_user.id
            )
            policy.is_active = True

            # Handle file upload
            if 'document' in request.files:
                file = request.files['document']
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{current_user.id}_{file.filename}")
                    upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
                    os.makedirs(upload_folder, exist_ok=True)
                    file.save(os.path.join(upload_folder, filename))
                    policy.document_path = filename

            db.session.add(policy)
            db.session.commit()
            flash('Policy uploaded successfully!', 'success')
            return redirect(url_for('policy_bp.list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error uploading policy: {str(e)}', 'error')

    return render_template('policies/client_upload.html')

@policy_bp.route('/download/<int:id>', endpoint='policy_download_doc')
@login_required
def download_doc(id):
    policy = UserPolicy.query.get_or_404(id)
    if policy.client_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('policy_bp.list'))
    
    if not policy.document_path:
        flash('No document available', 'error')
        return redirect(url_for('policy_bp.list'))
    
    upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
    return send_file(
        os.path.join(upload_folder, policy.document_path),
        as_attachment=True,
        download_name=policy.document_path
    ) 
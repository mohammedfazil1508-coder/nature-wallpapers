from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.models import db, User
from werkzeug.security import generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect('/')
        else:
            flash('Please check your login details and try again.', 'error')
            
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email address already exists', 'error')
            return redirect('/register')
            
        new_user = User(email=email, name=name, password_hash=generate_password_hash(password))
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect('/')

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@auth.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email, is_admin=True).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect('/admin')
        else:
            flash('Invalid admin credentials', 'error')
            
    return render_template('admin/login.html')

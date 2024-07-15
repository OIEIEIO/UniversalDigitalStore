from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from UniversalDigitalStore.data.models import User, SessionLocal  # Correct import path
import bcrypt

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session = SessionLocal()
        data = request.form
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Ensure the hashed password is stored as a string
        new_user = User(username=data['username'], password=hashed_password, email=data['email'])
        session.add(new_user)
        session.commit()
        session.close()
        return redirect(url_for('user_bp.login'))
    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session = SessionLocal()
        data = request.form
        user = session.query(User).filter_by(username=data['username']).first()
        print(f"Fetched user: {user}")
        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):  # Decode the stored hashed password to compare correctly
            print("Password matches.")
            login_user(user)
            session.close()
            return redirect(url_for('user_bp.dashboard'))
        print("Invalid credentials.")
        session.close()
        return "Invalid credentials", 401
    return render_template('login.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_bp.login'))

@user_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

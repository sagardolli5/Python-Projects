from datetime import datetime, timezone
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

# -------------------- DATABASE SETUP --------------------
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# LOGIN MANAGER SETUP
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# -------------------- DATABASE MODELS --------------------
class User(UserMixin,db.Model):
    __tablename__ = "users"

    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    tasks    = db.relationship("Task", backref="user", lazy=True)

class Task(db.Model):
    __tablename__ = "tasks"

    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name    = db.Column(db.String(250), nullable=False)
    created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- ROUTES --------------------
@app.route('/')
def home():
    return render_template("index.html", show_footer=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please log in.", "error")
            return redirect(url_for('login'))

        # Hash password and add user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template("login.html")  # login.html contains both forms

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password", "error")
            return redirect(url_for('login'))

        login_user(user)
        flash(f"Welcome, {user.name}!", "success")
        return redirect(url_for('dashboard'))

    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", tasks=user_tasks, user=current_user, show_footer=True)

@app.route('/delete/<int:task_id>', methods=["POST"])
@login_required
def delete(task_id):
    task = db.get_or_404(Task, task_id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add', methods=["POST"])
@login_required
def add():
    task_name = request.form.get('task')
    if task_name:
        new_task = Task(
            name=task_name,
            user_id=current_user.id,  # use logged-in user
        )
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)

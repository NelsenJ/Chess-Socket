from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import json
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'secret!')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///chess_game.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Room(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(20), nullable=False, default='public')
    password = db.Column(db.String(255), nullable=True)
    mode = db.Column(db.String(20), nullable=False, default='pvp')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

# Routes
@app.route("/")
def landing():
    try:
        # Initialize database only when needed
        with app.app_context():
            db.create_all()
        
        if "username" in session:
            return redirect(url_for("dashboard"))
        return render_template('landing.html')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            username = request.form["username"].strip()
            password = request.form["password"]
            
            if not username or not password:
                flash("Username dan password tidak boleh kosong", "error")
                return render_template("login.html")
            
            user = User.query.filter_by(username=username).first()
            if not user:
                flash("Username tidak terdaftar", "error")
                return render_template("login.html")
            
            if not user.check_password(password):
                flash("Password salah", "error")
                return render_template("login.html")
            
            session["username"] = user.username
            session["user_id"] = user.id
            return redirect(url_for("dashboard"))
        return render_template("login.html")
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        if request.method == "POST":
            username = request.form["username"].strip()
            password = request.form["password"]
            
            if not username or not password:
                flash("Username dan password tidak boleh kosong", "error")
                return render_template("register.html")
            
            if User.query.filter_by(username=username).first():
                flash("Username sudah ada", "error")
                return render_template("register.html")
            
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash("Registrasi berhasil! Silakan login", "success")
            return redirect(url_for("login"))
        return render_template("register.html")
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/dashboard")
def dashboard():
    try:
        if "username" not in session:
            return redirect(url_for("landing"))
        
        rooms = Room.query.all()
        return render_template("dashboard.html", rooms=rooms, username=session["username"])
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/create_room", methods=["POST"])
def create_room():
    try:
        if "username" not in session:
            return redirect(url_for("landing"))
        
        name = request.form.get("name")
        room_type = request.form.get("type", "public")
        mode = request.form.get("mode", "pvp")
        password = request.form.get("password") if room_type == "private" else None
        
        if not name:
            flash("Nama room tidak boleh kosong", "error")
            return redirect(url_for("dashboard"))
        
        room_id = str(uuid.uuid4())
        room = Room(
            id=room_id,
            name=name,
            type=room_type,
            password=password,
            mode=mode,
            created_by=session["user_id"]
        )
        
        db.session.add(room)
        db.session.commit()
        
        flash("Room berhasil dibuat!", "success")
        return redirect(url_for("game", room_id=room_id))
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/game/<room_id>")
def game(room_id):
    try:
        if "username" not in session:
            return redirect(url_for("landing"))
        
        room = Room.query.filter_by(id=room_id).first()
        if not room:
            flash("Room tidak ditemukan", "error")
            return redirect(url_for("dashboard"))
        
        return render_template("game.html", room=room, username=session["username"])
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/logout")
def logout():
    try:
        session.clear()
        return redirect(url_for("landing"))
    except Exception as e:
        return f"Error: {str(e)}", 500

# Export for Vercel
app.debug = False

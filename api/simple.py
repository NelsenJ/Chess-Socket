from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
import os

app = Flask(__name__)  # Use default folders (api/templates and api/static)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'secret!')

# Simple in-memory storage (for testing)
users = {}
rooms = {}

# Routes
@app.route("/")
def landing():
    try:
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
            
            if username not in users:
                flash("Username tidak terdaftar", "error")
                return render_template("login.html")
            
            if users[username] != password:  # Simple password check
                flash("Password salah", "error")
                return render_template("login.html")
            
            session["username"] = username
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
            
            if username in users:
                flash("Username sudah ada", "error")
                return render_template("register.html")
            
            users[username] = password
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
        
        return render_template("dashboard.html", rooms=rooms, username=session["username"])
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/create_room", methods=["POST"])
def create_room():
    try:
        if "username" not in session:
            return redirect(url_for("landing"))
        
        name = request.form.get("name")
        if not name:
            flash("Nama room tidak boleh kosong", "error")
            return redirect(url_for("dashboard"))
        
        room_id = str(len(rooms) + 1)
        rooms[room_id] = {
            'name': name,
            'creator': session["username"],
            'players': [session["username"]]
        }
        
        flash("Room berhasil dibuat!", "success")
        return redirect(url_for("game", room_id=room_id))
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/game/<room_id>")
def game(room_id):
    try:
        if "username" not in session:
            return redirect(url_for("landing"))
        
        if room_id not in rooms:
            flash("Room tidak ditemukan", "error")
            return redirect(url_for("dashboard"))
        
        room = rooms[room_id]
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

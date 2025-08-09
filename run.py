from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Simpan user dan room di memory (sementara)
users = {}  # username: password
rooms = {}  # room_id: {"name": str, "type": "public"/"private", "password": str or None, "members": []}

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username not in users:
            users[username] = password
            session["username"] = username  # langsung login setelah registrasi
            return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        room_name = request.form["room_name"]
        room_type = request.form["room_type"]
        password = request.form.get("password") if room_type == "private" else None
        room_id = str(uuid.uuid4())
        rooms[room_id] = {
            "name": room_name,
            "type": room_type,
            "password": password,
            "members": []
        }
        return redirect(url_for("game", room_id=room_id))
    return render_template("dashboard.html", rooms=rooms)

@app.route("/game/<room_id>")
def game(room_id):
    if "username" not in session:
        return redirect(url_for("login"))
    if room_id not in rooms:
        return redirect(url_for("dashboard"))
    return render_template("game.html", room_id=room_id, username=session["username"])

@socketio.on("join_room")
def handle_join(data):
    room_id = data["room_id"]
    username = session["username"]
    if rooms[room_id]["type"] == "private":
        if data.get("password") != rooms[room_id]["password"]:
            emit("error", {"message": "Wrong room password"})
            return
    join_room(room_id)
    rooms[room_id]["members"].append(username)
    emit("user_joined", {"username": username}, room=room_id)

@socketio.on("move_circle")
def handle_move(data):
    emit("update_circle", data, room=data["room_id"], include_self=False)

if __name__ == "__main__":
    socketio.run(app, debug=True)

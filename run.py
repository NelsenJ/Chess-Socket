from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess_game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode='eventlet', manage_session=False, cors_allowed_origins="*")


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
    type = db.Column(db.String(20), nullable=False, default='public')  # public/private
    password = db.Column(db.String(255), nullable=True)  # store hashed or plain for demo
    mode = db.Column(db.String(20), nullable=False, default='pvp')  # pvp / bot
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)


# In-memory active room state for TicTacToe
active_rooms = {}
# active_rooms[room_id] = {
#   'members': set([username,...]),
#   'mode': 'pvp'|'bot',
#   'players': {'X': username_or_COMPUTER, 'O': username_or_COMPUTER},
#   'board': ['','','','','','','','',''],
#   'turn': 'X' or 'O',
#   'winner': None | 'X' | 'O' | 'draw',
#   'rematch_votes': set(['X','O']),
#   'rematch_requested': False,
#   'rematch_pending': set(),
#   'room_creator': username
# }

# Store connected users for realtime updates
connected_users = set()

def init_database():
    """Initialize database with proper migration"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database initialized successfully")

init_database()

@app.route("/")
def landing():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template('landing.html')

@app.route("/login", methods=["GET", "POST"])
def login():
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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        
        if not username:
            flash("Username tidak boleh kosong", "error")
            return render_template("register.html")
        
        if not password:
            flash("Password tidak boleh kosong", "error")
            return render_template("register.html")
        
        if User.query.filter_by(username=username).first():
            flash("Username sudah dipakai", "error")
            return render_template("register.html")
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        session["username"] = user.username
        session["user_id"] = user.id
        flash("Akun berhasil dibuat! Selamat datang!", "success")
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        room_name = request.form["room_name"].strip()
        room_type = request.form["room_type"]
        mode = request.form.get("room_mode", "pvp")
        password = request.form.get("password") if room_type == "private" else None
        room_id = str(uuid.uuid4())

        new_room = Room(
            id=room_id,
            name=room_name,
            type=room_type,
            password=password,
            mode=mode,
            created_by=session.get("user_id"),
            created_at=datetime.utcnow()
        )
        db.session.add(new_room)
        db.session.commit()

        # initialize in-memory state for TicTacToe
        active_rooms[room_id] = {
            'members': set(),
            'mode': mode,
            'players': {'X': None, 'O': None},
            'board': [''] * 9,
            'turn': 'X',
            'winner': None,
            'rematch_votes': set(),
            'rematch_requested': False,
            'rematch_pending': set(),
            'room_creator': session["username"]
        }
        
        # Emit realtime room update to all connected users
        socketio.emit('room_created', {
            'room': {
                'id': room_id,
                'name': room_name,
                'type': room_type,
                'mode': mode,
                'players': 0,
                'created_by': session["username"]
            }
        })
        
        return redirect(url_for("game", room_id=room_id))
    
    # list rooms with simple counts from in-memory when available
    try:
        all_rooms = Room.query.all()
        room_list = []
        for r in all_rooms:
            count = len(active_rooms.get(r.id, {}).get('members', set()))
            creator_name = "Unknown"
            if r.created_by:
                creator = User.query.get(r.created_by)
                if creator:
                    creator_name = creator.username
            
            room_list.append({
                'id': r.id,
                'name': r.name,
                'type': r.type,
                'mode': r.mode,
                'players': count,
                'created_by': creator_name
            })
    except Exception as e:
        print(f"Error loading rooms: {e}")
        room_list = []
    
    return render_template("dashboard.html", rooms=room_list)

@app.route("/game/<room_id>")
def game(room_id):
    if "username" not in session:
        return redirect(url_for("login"))
    room = Room.query.filter_by(id=room_id).first()
    if not room:
        return redirect(url_for("dashboard"))

    # private room: require password once, then mark access in session
    if room.type == 'private':
        # Check if user is the room creator - they get immediate access
        if room.created_by == session.get("user_id"):
            # Room creator gets immediate access
            ra = session.get('room_access', {})
            ra[room_id] = True
            session['room_access'] = ra
        else:
            # Other users need password
            allowed = session.get('room_access', {}).get(room_id)
            if not allowed:
                supplied = request.args.get('password') or request.form.get('password')
                if not supplied:
                    flash('Masukkan password untuk room private', 'error')
                    return redirect(url_for('dashboard'))
                if room.password != supplied:
                    flash('Password salah untuk room ini', 'error')
                    return redirect(url_for('dashboard'))
                # mark access
                ra = session.get('room_access', {})
                ra[room_id] = True
                session['room_access'] = ra

    # ensure in-memory state exists
    if room_id not in active_rooms:
        creator_name = "Unknown"
        if room.created_by:
            creator = User.query.get(room.created_by)
            if creator:
                creator_name = creator.username
        
        active_rooms[room_id] = {
            'members': set(),
            'mode': room.mode,
            'players': {'X': None, 'O': None},
            'board': [''] * 9,
            'turn': 'X',
            'winner': None,
            'rematch_votes': set(),
            'rematch_requested': False,
            'rematch_pending': set(),
            'room_creator': creator_name
        }
    return render_template("game.html", room_id=room_id, username=session["username"])

@socketio.on("connect")
def handle_connect():
    username = session.get("username")
    if username:
        connected_users.add(username)
        emit('user_connected', {'username': username})

@socketio.on("disconnect")
def handle_disconnect():
    username = session.get("username")
    if username:
        connected_users.discard(username)
        emit('user_disconnected', {'username': username})

@socketio.on("join_room")
def handle_join(data):
    room_id = data.get("room_id") or data.get("room")
    if not room_id:
        emit("error", {"message": "room_id required"})
        return
    username = session.get("username")
    if not username:
        emit("error", {"message": "Not authenticated"})
        return

    room = Room.query.filter_by(id=room_id).first()
    if not room:
        emit("error", {"message": "Room not found"})
        return

    # private room access check
    if room.type == 'private':
        # Check if user is the room creator - they get immediate access
        if room.created_by == session.get("user_id"):
            # Room creator gets immediate access
            ra = session.get('room_access', {})
            ra[room_id] = True
            session['room_access'] = ra
        else:
            # Other users need password
            allowed = session.get('room_access', {}).get(room_id)
            supplied = data.get('password')
            if not allowed and (not supplied or supplied != room.password):
                emit("error", {"message": "Wrong room password"})
                return

    # initialize state if needed
    state = active_rooms.get(room_id)
    if not state:
        creator_name = "Unknown"
        if room.created_by:
            creator = User.query.get(room.created_by)
            if creator:
                creator_name = creator.username
        
        state = {
            'members': set(),
            'mode': room.mode,
            'players': {'X': None, 'O': None},
            'board': [''] * 9,
            'turn': 'X',
            'winner': None,
            'rematch_votes': set(),
            'rematch_requested': False,
            'rematch_pending': set(),
            'room_creator': creator_name
        }
        active_rooms[room_id] = state

    # enforce player limit
    current_players = state['members']
    if room.mode == 'bot':
        if len(current_players) >= 1 and username not in current_players:
            emit("error", {"message": "Room full (vs computer)"})
            return
    else:
        if len(current_players) >= 2 and username not in current_players:
            emit("error", {"message": "Room full (2 players max)"})
            return

    join_room(room_id)
    state['members'].add(username)
    
    # assign marks X/O
    your_mark = None
    if state['players']['X'] is None:
        state['players']['X'] = username
        your_mark = 'X'
        if room.mode == 'bot':
            state['players']['O'] = 'COMPUTER'
    elif state['players']['O'] is None and room.mode == 'pvp':
        state['players']['O'] = username
        your_mark = 'O'
    elif room.mode == 'bot':
        # already has X human and O = COMPUTER
        your_mark = 'X' if state['players']['X'] == username else None

    # Emit realtime room update to dashboard
    socketio.emit('room_updated', {
        'room_id': room_id,
        'players': len(state['members'])
    })

    # notify the joiner with game state
    emit('ttt_init', {
        'board': state['board'],
        'turn': state['turn'],
        'winner': state['winner'],
        'you': your_mark,
        'players': state['players'],
        'mode': state['mode'],
        'room_creator': state['room_creator'],
        'is_creator': username == state['room_creator']
    })
    
    # notify room about players update
    emit("players_update", {
        "players": state['players'],
        "members": list(state['members']),
        "room_creator": state['room_creator']
    }, room=room_id)

def _check_winner(board):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(cell for cell in board):
        return 'draw'
    return None

def _bot_move(board):
    import random
    empties = [i for i,v in enumerate(board) if not v]
    return random.choice(empties) if empties else None

@socketio.on('ttt_move')
def on_ttt_move(data):
    room_id = data.get('room_id')
    index = data.get('index')
    username = session.get('username')
    if room_id not in active_rooms or index is None or username is None:
        return
    state = active_rooms[room_id]
    board = state['board']
    if state['winner']:
        return
    # Determine player's mark
    mark = 'X' if state['players'].get('X') == username else ('O' if state['players'].get('O') == username else None)
    if mark is None:
        emit('error', {'message': 'You are a spectator'})
        return
    if state['turn'] != mark:
        return
    if index < 0 or index > 8 or board[index]:
        return
    # apply move
    board[index] = mark
    state['winner'] = _check_winner(board)
    if not state['winner']:
        state['turn'] = 'O' if state['turn'] == 'X' else 'X'

    emit('ttt_update', {
        'board': board,
        'turn': state['turn'],
        'winner': state['winner'],
        'last': {'index': index, 'mark': mark}
    }, room=room_id)

    # bot move if needed
    if not state['winner'] and state['mode'] == 'bot':
        bot_mark = 'O' if mark == 'X' else 'X'
        # ensure bot is assigned that mark
        if state['players'].get(bot_mark) == 'COMPUTER' and state['turn'] == bot_mark:
            bi = _bot_move(board)
            if bi is not None:
                board[bi] = bot_mark
                state['winner'] = _check_winner(board)
                if not state['winner']:
                    state['turn'] = 'O' if state['turn'] == 'X' else 'X'
                emit('ttt_update', {
                    'board': board,
                    'turn': state['turn'],
                    'winner': state['winner'],
                    'last': {'index': bi, 'mark': bot_mark}
                }, room=room_id)

@socketio.on('ttt_rematch_request')
def on_ttt_rematch_request(data):
    room_id = data.get('room_id')
    username = session.get('username')
    if not room_id or room_id not in active_rooms or not username:
        return
    
    state = active_rooms[room_id]
    
    # Only room creator can request rematch
    if username != state['room_creator']:
        emit('error', {'message': 'Hanya pembuat room yang bisa request rematch'})
        return
    
    # Only allow when game is over
    if not state.get('winner'):
        emit('error', {'message': 'Game belum selesai'})
        return
    
    # Set rematch as requested
    state['rematch_requested'] = True
    state['rematch_pending'] = set()
    
    # Add creator's vote
    mark = 'X' if state['players'].get('X') == username else ('O' if state['players'].get('O') == username else None)
    if mark:
        state['rematch_votes'].add(mark)
    
    # Notify other players about rematch request
    emit('rematch_requested', {
        'requested_by': username,
        'creator_vote': mark
    }, room=room_id)

@socketio.on('ttt_rematch_response')
def on_ttt_rematch_response(data):
    room_id = data.get('room_id')
    response = data.get('response')  # 'accept' or 'decline'
    username = session.get('username')
    
    if not room_id or room_id not in active_rooms or not username:
        return
    
    state = active_rooms[room_id]
    
    if not state.get('rematch_requested'):
        emit('error', {'message': 'Tidak ada request rematch'})
        return
    
    if username == state['room_creator']:
        emit('error', {'message': 'Anda adalah pembuat room'})
        return
    
    if response == 'accept':
        # Add player's vote
        mark = 'X' if state['players'].get('X') == username else ('O' if state['players'].get('O') == username else None)
        if mark:
            state['rematch_votes'].add(mark)
            state['rematch_pending'].add(username)
        
        # Check if both players voted
        if len(state['rematch_votes']) >= 2:
            # Reset game
            state['board'] = [''] * 9
            state['winner'] = None
            state['turn'] = 'O' if state['turn'] == 'X' else 'X'
            state['rematch_votes'].clear()
            state['rematch_requested'] = False
            state['rematch_pending'].clear()
            
            emit('ttt_reset', {
                'board': state['board'],
                'turn': state['turn']
            }, room=room_id)
        else:
            emit('rematch_status', {
                'votes': list(state['rematch_votes']),
                'pending': list(state['rematch_pending'])
            }, room=room_id)
    
    elif response == 'decline':
        # Reset rematch state
        state['rematch_requested'] = False
        state['rematch_votes'].clear()
        state['rematch_pending'].clear()
        
        emit('rematch_declined', {
            'declined_by': username
        }, room=room_id)

@socketio.on('dissolve_room')
def on_dissolve_room(data):
    room_id = data.get('room_id')
    username = session.get('username')
    
    if not room_id or not username:
        return
    
    state = active_rooms.get(room_id)
    if not state:
        return
    
    # Only room creator can dissolve room
    if username != state['room_creator']:
        emit('error', {'message': 'Hanya pembuat room yang bisa dissolve room'})
        return
    
    # Emit realtime room update to dashboard
    socketio.emit('room_dissolved', {'room_id': room_id})
    
    # delete from memory and database if exists
    active_rooms.pop(room_id, None)
    room = Room.query.filter_by(id=room_id).first()
    if room:
        db.session.delete(room)
        db.session.commit()
    
    emit('room_dissolved', {'room_id': room_id}, room=room_id)

@socketio.on("leave_room")
def on_leave(data):
    room_id = data.get('room_id') or data.get('room')
    username = session.get('username')
    if not room_id or not username:
        return
    
    leave_room(room_id)
    state = active_rooms.get(room_id)
    if state and username in state['members']:
        state['members'].remove(username)
        
        # Emit realtime room update to dashboard
        socketio.emit('room_updated', {
            'room_id': room_id,
            'players': len(state['members'])
        })
        
        emit("user_left", {
            "username": username, 
            "players": list(state['members'])
        }, room=room_id)
        
        # cleanup if empty
        if not state['members']:
            active_rooms.pop(room_id, None)
            room = Room.query.filter_by(id=room_id).first()
            if room:
                db.session.delete(room)
                db.session.commit()
            
            # Emit realtime room update to dashboard
            socketio.emit('room_dissolved', {'room_id': room_id})

if __name__ == "__main__":
    socketio.run(app, debug=True)

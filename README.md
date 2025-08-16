# Socket-Game - Real-time TicTacToe Game

A real-time multiplayer TicTacToe game built with Flask, Socket.IO, and SQLAlchemy.

## ✨ Features

### 🚀 Real-time Updates
- **Instant Room Creation**: New rooms appear immediately on all connected dashboards
- **Live Player Count**: Player counts update in real-time as users join/leave
- **Real-time Game State**: Game board updates instantly across all players
- **Live Room Management**: Rooms are removed instantly when dissolved

### 🎮 Enhanced Game Experience
- **Smart Rematch System**: Only room creator can request rematch
- **Player Response System**: Non-creators get accept/decline buttons for rematch requests
- **Role-based Controls**: Room creator has exclusive access to dissolve room and request rematch
- **Player Information Display**: Shows current player turn and player names
- **Visual Turn Indicator**: Highlights current player's turn

### 🔐 Improved Authentication
- **Better Error Messages**: Specific feedback for username not found vs password incorrect
- **Registration Validation**: Clear feedback when username already exists
- **Flash Message System**: Auto-dismissing notifications for better UX

### 🏠 Room Management
- **Public & Private Rooms**: Support for both room types
- **Password Protection**: Secure private rooms with password authentication
- **Player vs Computer**: Single-player mode against AI
- **Player vs Player**: Classic multiplayer experience

## 🛠️ Technology Stack

- **Backend**: Flask, Flask-SocketIO, Flask-SQLAlchemy
- **Database**: SQLite with SQLAlchemy ORM
- **Real-time**: Socket.IO for bidirectional communication
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Authentication**: Werkzeug password hashing

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone (https://github.com/NelsenJ/Socket-Game.git)
   cd Chess-Socket
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 How to Play

### Creating a Room
1. Login/Register to access dashboard
2. Fill in room details (name, type, mode)
3. Click "Create Room" to start

### Joining a Room
1. Browse available rooms on dashboard
2. Click "Join" for public rooms
3. Enter password for private rooms

### Gameplay
- **X always goes first**
- Click on empty cells to make moves
- Game automatically detects wins/draws
- Only room creator can request rematch or dissolve room

### Rematch System
- **Room Creator**: Can request rematch after game ends
- **Other Players**: Receive popup to accept/decline rematch
- **Auto-reset**: Game resets when rematch is accepted

## 🔧 Configuration

The application uses the following default settings:
- **Port**: 5000
- **Database**: SQLite (app.db)
- **Secret Key**: 'secret!' (change in production)
- **Async Mode**: eventlet

## 📱 Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Known Issues

- None currently reported

## 🔮 Future Enhancements

- [ ] Chat system between players
- [ ] Game history and statistics
- [ ] Tournament mode
- [ ] Mobile app version
- [ ] More game variants

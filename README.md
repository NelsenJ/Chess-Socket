# Socket-Game - Real-time TicTacToe Game

A real-time multiplayer TicTacToe game built with Flask, Socket.IO, and SQLAlchemy. Play with friends online or challenge the computer in this modern web-based game.

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
- **Async Support**: Eventlet for Socket.IO

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/NelsenJ/Socket-Game.git
   cd Socket-Game
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows:
   source .venv/Scripts/activate
   
   # On macOS/Linux:
   source .venv/bin/activate
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

### Getting Started
1. **Register/Login**: Create an account or sign in to access the game
2. **Dashboard**: View available rooms and create new ones
3. **Game Modes**: Choose between Player vs Player or Player vs Computer

### Creating a Room
1. Login to access dashboard
2. Fill in room details:
   - **Room Name**: Choose a descriptive name
   - **Room Type**: Public (anyone can join) or Private (password protected)
   - **Game Mode**: PvP (Player vs Player) or Bot (Player vs Computer)
3. Click "Create Room" to start

### Joining a Room
1. Browse available rooms on dashboard
2. **Public Rooms**: Click "Join" to enter immediately
3. **Private Rooms**: Click "Join" and enter the password

### Gameplay Rules
- **X always goes first** (first player to join)
- Click on empty cells to make moves
- Game automatically detects wins, draws, and invalid moves
- **Room Creator Privileges**: Only room creator can request rematch or dissolve room

### Rematch System
- **Room Creator**: Can request rematch after game ends
- **Other Players**: Receive popup to accept/decline rematch
- **Auto-reset**: Game resets when rematch is accepted

## 🔧 Configuration

The application uses the following default settings:
- **Port**: 5000
- **Database**: SQLite (chess_game.db)
- **Secret Key**: 'secret!' (change in production)
- **Async Mode**: eventlet
- **CORS**: All origins allowed (configurable)

### Environment Variables
Create a `.env` file in the root directory:
```env
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

## 📱 Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
- Mobile browsers (responsive design)

## 🧪 Testing

Run the test suite:
```bash
python test_private_room.py
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Submit a pull request**

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Known Issues

- None currently reported

## 🔮 Future Enhancements

- [ ] Chat system between players
- [ ] Game history and statistics
- [ ] Tournament mode
- [ ] Mobile app version
- [ ] More game variants (Connect Four, Checkers)
- [ ] User profiles and achievements
- [ ] Spectator mode
- [ ] Game replay functionality

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the existing issues for solutions
- Review the code documentation

## 🙏 Acknowledgments

- Built with Flask and Socket.IO
- Inspired by classic TicTacToe gameplay
- Community contributions and feedback

---

**Happy Gaming! 🎮**

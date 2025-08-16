# 🚀 Deploying to Vercel

## ⚠️ Important Notes

**Vercel has limitations for Flask apps with WebSockets:**
- Vercel doesn't support persistent WebSocket connections
- Your real-time game features will need to be adapted
- Consider using alternative platforms for full WebSocket support

## 🎯 Alternative Deployment Options

### 1. **Heroku** (Recommended for WebSocket apps)
- Full WebSocket support
- Easy Flask deployment
- Free tier available

### 2. **Railway**
- Good WebSocket support
- Simple deployment
- Reasonable pricing

### 3. **DigitalOcean App Platform**
- Full WebSocket support
- Scalable
- Professional hosting

## 📋 Vercel Deployment Steps

### Prerequisites
1. Install [Vercel CLI](https://vercel.com/cli)
2. Have a GitHub account
3. Your code pushed to GitHub

### Step 1: Install Vercel CLI
```bash
npm i -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
vercel
```

### Step 4: Follow the prompts
- Set up and deploy? `Y`
- Which scope? `Select your account`
- Link to existing project? `N`
- Project name? `socket-game-tictactoe`
- In which directory is your code located? `./`
- Want to override the settings? `N`

### Step 5: Set Environment Variables
In Vercel dashboard:
1. Go to your project
2. Settings → Environment Variables
3. Add:
   - `FLASK_SECRET_KEY`: Your secret key
   - `FLASK_ENV`: `production`

## 🔧 Post-Deployment

### Check Your App
- Visit the provided Vercel URL
- Test basic functionality (login, register, dashboard)

### Monitor Logs
```bash
vercel logs
```

### Update Domain (Optional)
- Go to Vercel dashboard
- Settings → Domains
- Add custom domain

## 🚨 Limitations & Workarounds

### WebSocket Issues
Since Vercel doesn't support WebSockets, you'll need to:

1. **Remove Socket.IO dependencies** from `requirements-vercel.txt`
2. **Adapt your game logic** to work without real-time updates
3. **Use polling** or **Server-Sent Events** as alternatives

### Database Issues
- Vercel uses serverless functions
- SQLite won't work (no persistent storage)
- Consider using:
  - **Supabase** (PostgreSQL)
  - **PlanetScale** (MySQL)
  - **MongoDB Atlas**

## 🎮 Making It Work on Vercel

### Option 1: Static Game (No Multiplayer)
- Remove all WebSocket code
- Make it single-player only
- Use localStorage for game state

### Option 2: Hybrid Approach
- Keep basic Flask routes
- Use external WebSocket service (like Ably)
- Integrate with your game logic

### Option 3: Alternative Platform
- Deploy to Heroku instead
- Keep all WebSocket functionality
- Better for multiplayer games

## 📱 Testing Your Deployment

1. **Basic Routes**: `/`, `/login`, `/register`
2. **Authentication**: User registration and login
3. **Dashboard**: Room listing
4. **Game**: Basic game functionality

## 🆘 Troubleshooting

### Common Issues
- **Import errors**: Check `requirements-vercel.txt`
- **Template not found**: Ensure templates are in the right location
- **Database errors**: Check environment variables
- **WebSocket errors**: Expected on Vercel

### Get Help
- Vercel documentation: [vercel.com/docs](https://vercel.com/docs)
- Flask documentation: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- GitHub issues: Check your repository

## 🎯 Next Steps

1. **Test basic deployment** on Vercel
2. **Evaluate limitations** for your use case
3. **Consider alternatives** if WebSockets are essential
4. **Adapt code** based on chosen platform

---

**Remember**: Vercel is great for static sites and simple APIs, but for real-time multiplayer games, you might want to consider other platforms that fully support WebSockets! 🎮

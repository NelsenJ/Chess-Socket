#!/bin/bash

echo "🚀 Deploying Socket-Game to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if user is logged in
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel..."
    vercel login
fi

# Deploy to Vercel
echo "📦 Deploying..."
vercel --prod

echo "✅ Deployment complete!"
echo "🌐 Check your Vercel dashboard for the live URL"
echo "📝 Don't forget to set environment variables in Vercel dashboard:"
echo "   - FLASK_SECRET_KEY"
echo "   - FLASK_ENV=production"
echo "   - DATABASE_URL (if using external database)"

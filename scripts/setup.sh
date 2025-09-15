#!/bin/bash

# Campus AI Assistant Setup Script
echo "🚀 Setting up Campus AI Assistant..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Create virtual environment for backend
echo "📦 Setting up Python virtual environment..."
cd backend
python3 -m venv venv

# Activate virtual environment (Linux/Mac)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created .env file. Please update it with your configuration."
fi

cd ..

# Setup frontend
echo "📦 Setting up Frontend..."
cd frontend
npm install
cd ..

# Setup widget
echo "📦 Setting up Chat Widget..."
cd chatbot-widget
npm install
npm run build
cd ..

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update backend/.env with your database and API keys"
echo "2. Start PostgreSQL and Redis services"
echo "3. Run: npm run dev (from project root)"
echo ""
echo "🌐 The application will be available at:"
echo "   - Backend API: http://localhost:8000"
echo "   - Admin Panel: http://localhost:3000"
echo "   - Widget Demo: http://localhost:8080"
echo ""
echo "📖 See README.md for detailed instructions."
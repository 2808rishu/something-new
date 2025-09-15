# Setup Guide

## Prerequisites

- Python 3.9+ with pip
- Node.js 16+ with npm
- PostgreSQL 12+
- Redis 6+
- Git

## Quick Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/campus-ai-assistant.git
cd campus-ai-assistant
```

### 2. Run Setup Script
```bash
# Linux/Mac
chmod +x scripts/setup.sh
./scripts/setup.sh

# Windows
scripts\setup.bat
```

### 3. Configure Environment
Edit `backend/.env`:
```env
DATABASE_URL=postgresql://postgres:password@localhost/campus_ai
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-super-secret-key
OPENAI_API_KEY=your-openai-key
```

### 4. Start Services
```bash
# Start database and cache
docker-compose up postgres redis -d

# Start backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload

# Start frontend (new terminal)
cd frontend
npm start

# Build widget (new terminal)
cd chatbot-widget
npm run build
```

## Manual Setup

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env file
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Widget Setup
```bash
cd chatbot-widget
npm install
npm run build
```

## Database Setup

### Using Docker
```bash
docker-compose up postgres -d
```

### Manual PostgreSQL
```sql
CREATE DATABASE campus_ai;
CREATE USER campus_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE campus_ai TO campus_user;
```

## Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost/campus_ai
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
WHATSAPP_TOKEN=your-whatsapp-token
TELEGRAM_TOKEN=your-telegram-token

# Features
SUPPORTED_LANGUAGES=en,hi,mr,ta,te
CONFIDENCE_THRESHOLD=0.7
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Database connection error:**
- Check PostgreSQL is running
- Verify credentials in .env
- Check firewall settings

**Python package installation fails:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

**Node modules installation fails:**
```bash
# Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## Production Deployment

See [Deployment Guide](deployment.md) for production setup instructions.
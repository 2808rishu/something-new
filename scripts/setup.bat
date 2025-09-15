@echo off
echo 🚀 Setting up Campus AI Assistant...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is required but not installed.
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is required but not installed.
    exit /b 1
)

REM Create virtual environment for backend
echo 📦 Setting up Python virtual environment...
cd backend
python -m venv venv

REM Activate virtual environment (Windows)
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Copy environment file
if not exist .env (
    copy .env.example .env
    echo 📝 Created .env file. Please update it with your configuration.
)

cd ..

REM Setup frontend
echo 📦 Setting up Frontend...
cd frontend
npm install
cd ..

REM Setup widget
echo 📦 Setting up Chat Widget...
cd chatbot-widget
npm install
npm run build
cd ..

echo ✅ Setup complete!
echo.
echo 📋 Next steps:
echo 1. Update backend/.env with your database and API keys
echo 2. Start PostgreSQL and Redis services
echo 3. Run: npm run dev (from project root)
echo.
echo 🌐 The application will be available at:
echo    - Backend API: http://localhost:8000
echo    - Admin Panel: http://localhost:3000
echo    - Widget Demo: http://localhost:8080
echo.
echo 📖 See README.md for detailed instructions.

pause
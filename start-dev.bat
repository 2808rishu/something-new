@echo off
echo 🚀 Starting Campus AI Assistant Development Environment...
echo.

echo 📦 Installing dependencies...
call npm install
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo 🔧 Setting up environment...
call npm run setup:env

echo 🌐 Starting all services...
echo.
echo 📋 Services will be available at:
echo    - Backend API: http://localhost:8000
echo    - Admin Panel: http://localhost:3000
echo    - Widget Demo: Open demo.html in browser
echo.
echo Press Ctrl+C to stop all services
echo.

start /b npm run dev

echo ✅ All services started!
echo.
echo 🎯 Open demo.html in your browser to test the chatbot!
echo.
pause
# 🚀 Local Setup Instructions

## Quick Start (For You)

1. **Open Command Prompt (CMD)**:
   ```
   Windows Key + R → type "cmd" → Press Enter
   ```

2. **Navigate to your project**:
   ```cmd
   cd /d D:\SIH
   ```

3. **Start the demo**:
   ```cmd
   start demo.html
   ```

4. **Or start development server** (if you want the full backend):
   ```cmd
   start-dev.bat
   ```

## 🌐 Live Demo

Your chatbot is now available online at:
**https://2808rishu.github.io/something-new/**

## 👥 For Your Friends to Run Locally

### Step 1: Clone the Repository
```cmd
git clone https://github.com/2808rishu/something-new.git
cd something-new
```

### Step 2: Install Dependencies
```cmd
npm install
```

### Step 3: Start the Application
**Option A - Simple Demo:**
```cmd
start demo.html
```

**Option B - Full Development Environment:**
```cmd
start-dev.bat
```

### Step 4: Access the Application
- **Widget Demo**: Open demo.html in browser
- **GitHub Pages Demo**: https://2808rishu.github.io/something-new/
- **Backend API**: http://localhost:8000 (if running dev environment)
- **Admin Panel**: http://localhost:3000 (if running dev environment)

## 🔧 Using Docker (Alternative)

If they have Docker installed:
```cmd
docker-compose up -d
```

## 📱 Embed on Any Website

Add this to any HTML page:
```html
<script src="https://2808rishu.github.io/something-new/chatbot-widget.min.js" 
        data-api-url="https://your-api-domain.com/api/v1"
        data-language="en">
</script>
```

## 🎯 What Works Right Now

✅ **Working immediately**:
- Widget demo (demo.html)
- GitHub Pages demo 
- Chat interface with 5 languages
- Responsive design

⚙️ **Requires setup for full functionality**:
- Backend API (FastAPI)
- Database (PostgreSQL)
- Admin panel (React)
- Real AI responses

## 🆘 Troubleshooting

If npm commands don't work:
1. Install Node.js from https://nodejs.org/
2. Restart command prompt
3. Try again

If git commands don't work:
1. Install Git from https://git-scm.com/
2. Restart command prompt
3. Try again
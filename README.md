# Campus AI Assistant - Multilingual Chatbot Platform

A comprehensive multilingual conversational AI platform designed to handle student queries across multiple channels (Web, WhatsApp, Telegram) with support for Hindi, English, and regional languages.

## 🏗️ System Architecture

### Core Components
1. **Frontend Channels**: Web Widget, WhatsApp, Telegram, PWA
2. **Input Preprocessing**: ASR, text cleaning, language detection
3. **NLU & Context Core**: Intent recognition, entity extraction, conversation management
4. **Retrieval Pipeline**: Multi-layered approach (L1 Cache + L2 Semantic Search)
5. **Response Generation**: LLM-based summarization with source citations
6. **Admin Panel**: Management interface for staff/volunteers
7. **Human Handoff**: Intelligent escalation system

### Technology Stack
- **Backend**: Python (FastAPI)
- **Database**: PostgreSQL (FAQs) + Redis (Cache) + Pinecone (Vector DB)
- **NLU**: Rasa/Transformers
- **Frontend**: React (Admin Panel) + Vanilla JS (Widget)
- **Deployment**: Docker + GitHub Pages/Actions
- **APIs**: WhatsApp Cloud API, Telegram Bot API

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git
- Docker (optional)

### Installation
```bash
git clone https://github.com/yourusername/campus-ai-assistant.git
cd campus-ai-assistant
./scripts/setup.sh
```

## 📁 Project Structure
```
campus-ai-assistant/
├── backend/                 # FastAPI backend services
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # NLU, retrieval logic
│   │   ├── models/         # Database models
│   │   └── services/       # Business logic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React admin panel
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── Dockerfile
├── chatbot-widget/         # Embeddable widget
│   ├── src/
│   ├── dist/
│   └── package.json
├── docs/                   # Documentation
├── docker/                 # Docker compose configs
├── scripts/               # Setup and utility scripts
└── .github/               # CI/CD workflows
```

## 🎯 Development Phases

### Phase 1: Core MVP (Week 1)
- [x] Project setup
- [ ] Basic FastAPI backend
- [ ] Simple FAQ retrieval
- [ ] Basic web widget
- [ ] PostgreSQL integration

### Phase 2: Advanced Features (Week 2)
- [ ] NLU integration (Rasa)
- [ ] Vector database setup
- [ ] Document OCR pipeline
- [ ] Semantic search
- [ ] LLM integration

### Phase 3: Admin & Management (Week 3)
- [ ] Admin panel (React)
- [ ] Human handoff system
- [ ] Analytics dashboard
- [ ] User management

### Phase 4: Multi-platform & Deployment (Week 4)
- [ ] WhatsApp integration
- [ ] Telegram bot
- [ ] PWA development
- [ ] Docker deployment
- [ ] GitHub Actions CI/CD

## 🌐 Deployment Options

### Option 1: GitHub Pages + External Services
- Frontend: GitHub Pages
- Backend: Railway/Render/Vercel
- Database: PlanetScale/Supabase

### Option 2: Full GitHub + Docker
- Everything containerized
- GitHub Actions for CI/CD
- GitHub Container Registry

## 🔗 Widget Integration

To embed the chatbot on your website, add this single line of code:

```html
<script src="https://yourusername.github.io/campus-ai-assistant/widget.js" data-config="your-config-key"></script>
```

## 📚 Documentation
- [Setup Guide](docs/setup.md)
- [API Documentation](docs/api.md)
- [Widget Integration](docs/widget-integration.md)
- [Deployment Guide](docs/deployment.md)
- [Contributing](docs/contributing.md)

## 🤝 Contributing
Please read our [Contributing Guide](docs/contributing.md) for details on our code of conduct and development process.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
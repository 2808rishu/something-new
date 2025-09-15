from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv

from app.core.database import get_db, engine
from app.models import models
from app.api import chat, admin, auth
from app.core.config import settings

load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Campus AI Assistant API",
    description="Multilingual chatbot API for campus queries",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])

@app.get("/")
async def root():
    return {"message": "Campus AI Assistant API", "version": "1.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected", "supported_languages": settings.SUPPORTED_LANGUAGES}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
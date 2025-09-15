from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import hashlib
from datetime import datetime

from app.core.database import get_db
from app.models.models import Admin
from passlib.context import CryptContext

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "admin"

class AdminResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

@router.post("/admins", response_model=AdminResponse)
async def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    """Create new admin user"""
    # Check if admin already exists
    existing_admin = db.query(Admin).filter(
        (Admin.username == admin.username) | (Admin.email == admin.email)
    ).first()
    
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin already exists")
    
    # Hash password
    hashed_password = pwd_context.hash(admin.password)
    
    # Create admin
    db_admin = Admin(
        username=admin.username,
        email=admin.email,
        hashed_password=hashed_password,
        role=admin.role
    )
    
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    
    return db_admin

@router.get("/admins", response_model=List[AdminResponse])
async def list_admins(db: Session = Depends(get_db)):
    """List all admin users"""
    admins = db.query(Admin).all()
    return admins
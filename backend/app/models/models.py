from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class FAQ(Base):
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, index=True)
    question_en = Column(Text, nullable=False)
    question_hi = Column(Text)
    question_mr = Column(Text)  # Marathi
    question_ta = Column(Text)  # Tamil
    question_te = Column(Text)  # Telugu
    answer_en = Column(Text, nullable=False)
    answer_hi = Column(Text)
    answer_mr = Column(Text)
    answer_ta = Column(Text)
    answer_te = Column(Text)
    category = Column(String(100))
    keywords = Column(JSON)
    priority = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String(50), primary_key=True, index=True)
    user_id = Column(String(100))
    platform = Column(String(20))  # web, whatsapp, telegram
    language = Column(String(5), default="en")
    status = Column(String(20), default="active")  # active, escalated, closed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(50), ForeignKey("conversations.id"))
    sender = Column(String(10))  # user, bot, admin
    message_text = Column(Text)
    intent = Column(String(100))
    confidence = Column(Float)
    response_source = Column(String(20))  # faq, vector, llm, human
    response_time_ms = Column(Integer)
    language = Column(String(5), default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    conversation = relationship("Conversation", back_populates="messages")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(20))
    content = Column(Text)
    metadata = Column(JSON)
    is_processed = Column(Boolean, default=False)
    language = Column(String(5), default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="admin")  # admin, moderator
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(String(50), primary_key=True, index=True)
    user_id = Column(String(100))
    website_domain = Column(String(255))
    language_preference = Column(String(5), default="en")
    session_data = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
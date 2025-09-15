from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, List
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.multilingual_nlu import MultilingualNLU
from app.core.multilingual_retrieval import MultilingualRetrievalPipeline
from app.models.models import Conversation, Message, ChatSession
from app.services.context_manager import ContextManager, ResponseGenerator

router = APIRouter()

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    platform: str = "web"
    user_id: Optional[str] = None
    language: Optional[str] = None
    website_domain: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    confidence: float
    source: str
    language: str
    detected_language: str
    escalate: bool = False
    suggestions: Optional[List[str]] = None
    intent: str

class ConversationHistory(BaseModel):
    conversation_id: str
    messages: List[Dict]
    total_messages: int
    language: str
    status: str

# Initialize services
nlu_engine = MultilingualNLU()
response_generator = ResponseGenerator()

@router.post("/message", response_model=ChatResponse)
async def chat_message(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Process chat message and return multilingual response"""
    
    # Generate conversation ID if not provided
    if not request.conversation_id:
        conversation_id = str(uuid.uuid4())
        # Create new conversation
        conversation = Conversation(
            id=conversation_id,
            user_id=request.user_id or "anonymous",
            platform=request.platform,
            language=request.language or "en"
        )
        db.add(conversation)
        
        # Create chat session for web widget
        if request.platform == "web" and request.website_domain:
            chat_session = ChatSession(
                id=conversation_id,
                user_id=request.user_id or "anonymous",
                website_domain=request.website_domain,
                language_preference=request.language or "en"
            )
            db.add(chat_session)
        
        db.commit()
    else:
        conversation_id = request.conversation_id
    
    # Process with multilingual NLU
    nlu_result = nlu_engine.process_query(request.message, request.language)
    
    # Get context
    context_manager = ContextManager(db, conversation_id)
    context = context_manager.get_context()
    
    # Retrieve answer with multilingual support
    retrieval_pipeline = MultilingualRetrievalPipeline(db)
    search_result = retrieval_pipeline.search(
        query=nlu_result["text_en"],  # Use English for search
        intent=nlu_result["intent"],
        language=nlu_result["language"]  # Return response in user's language
    )
    
    # Generate final response
    final_response = response_generator.generate_response(
        search_result=search_result,
        context=context,
        nlu_result=nlu_result
    )
    
    # Save user message
    user_message = Message(
        conversation_id=conversation_id,
        sender="user",
        message_text=request.message,
        intent=nlu_result["intent"],
        confidence=nlu_result["confidence"],
        language=nlu_result["language"]
    )
    db.add(user_message)
    
    # Save bot response
    bot_message = Message(
        conversation_id=conversation_id,
        sender="bot",
        message_text=final_response["response"],
        intent=nlu_result["intent"],
        confidence=search_result["confidence"],
        response_source=search_result["source"],
        language=nlu_result["language"]
    )
    db.add(bot_message)
    
    db.commit()
    
    # Update context in background
    background_tasks.add_task(
        context_manager.update_context,
        nlu_result,
        search_result
    )
    
    return ChatResponse(
        response=final_response["response"],
        conversation_id=conversation_id,
        confidence=search_result["confidence"],
        source=search_result["source"],
        language=nlu_result["language"],
        detected_language=nlu_result["detected_language"],
        escalate=search_result.get("escalate", False),
        suggestions=final_response.get("suggestions"),
        intent=nlu_result["intent"]
    )

@router.get("/conversation/{conversation_id}", response_model=ConversationHistory)
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get conversation history"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = [
        {
            "id": msg.id,
            "sender": msg.sender,
            "message": msg.message_text,
            "intent": msg.intent,
            "confidence": msg.confidence,
            "source": msg.response_source,
            "timestamp": msg.created_at.isoformat(),
            "language": msg.language
        }
        for msg in conversation.messages
    ]
    
    return ConversationHistory(
        conversation_id=conversation_id,
        messages=messages,
        total_messages=len(messages),
        language=conversation.language,
        status=conversation.status
    )

@router.post("/feedback")
async def submit_feedback(
    conversation_id: str,
    message_id: int,
    rating: int,
    feedback: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Submit feedback for bot response"""
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    # Store feedback logic here
    # This could be stored in a separate Feedback table
    
    return {"status": "feedback recorded", "message": "Thank you for your feedback!"}

@router.post("/escalate")
async def escalate_conversation(
    conversation_id: str,
    reason: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Escalate conversation to human agent"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversation.status = "escalated"
    db.commit()
    
    # Here you would implement notification logic to alert human agents
    # Could integrate with email, Slack, WhatsApp etc.
    
    return {"status": "escalated", "message": "Your query has been escalated to our support team. You will be contacted shortly."}

@router.get("/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    from app.core.config import settings
    
    languages = {
        "en": {"name": "English", "native_name": "English"},
        "hi": {"name": "Hindi", "native_name": "हिन्दी"},
        "mr": {"name": "Marathi", "native_name": "मराठी"},
        "ta": {"name": "Tamil", "native_name": "தமிழ்"},
        "te": {"name": "Telugu", "native_name": "తెలుగు"}
    }
    
    return {
        "supported_languages": [
            {
                "code": lang,
                "name": languages[lang]["name"],
                "native_name": languages[lang]["native_name"]
            }
            for lang in settings.SUPPORTED_LANGUAGES
            if lang in languages
        ]
    }

@router.post("/translate")
async def translate_message(
    text: str,
    target_language: str,
    source_language: Optional[str] = None
):
    """Translate message to target language"""
    try:
        translated = nlu_engine.translate_text(text, target_language)
        return {
            "original_text": text,
            "translated_text": translated,
            "source_language": source_language,
            "target_language": target_language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@router.get("/stats")
async def get_chat_stats(db: Session = Depends(get_db)):
    """Get basic chat statistics"""
    from sqlalchemy import func
    
    total_conversations = db.query(func.count(Conversation.id)).scalar()
    total_messages = db.query(func.count(Message.id)).scalar()
    
    # Language distribution
    language_stats = db.query(
        Conversation.language, 
        func.count(Conversation.language)
    ).group_by(Conversation.language).all()
    
    # Intent distribution
    intent_stats = db.query(
        Message.intent,
        func.count(Message.intent)
    ).filter(Message.sender == "user").group_by(Message.intent).all()
    
    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "language_distribution": {lang: count for lang, count in language_stats},
        "popular_intents": {intent: count for intent, count in intent_stats}
    }
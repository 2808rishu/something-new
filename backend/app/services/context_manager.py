from typing import Dict, List, Optional
import json
from app.core.database import redis_client

class ContextManager:
    def __init__(self, db, conversation_id: str):
        self.db = db
        self.conversation_id = conversation_id
        self.redis_client = redis_client
        
    def _get_context_key(self) -> str:
        return f"context:{self.conversation_id}"
    
    def get_context(self) -> Dict:
        """Get conversation context"""
        try:
            context_data = self.redis_client.get(self._get_context_key())
            if context_data:
                return json.loads(context_data)
        except Exception as e:
            print(f"Context retrieval error: {e}")
        
        # Default context
        return {
            "conversation_id": self.conversation_id,
            "recent_intents": [],
            "entities": {},
            "language": "en",
            "escalated": False,
            "turn_count": 0
        }
    
    def update_context(self, nlu_result: Dict, search_result: Dict):
        """Update conversation context"""
        try:
            context = self.get_context()
            
            # Update recent intents (keep last 5)
            recent_intents = context.get("recent_intents", [])
            recent_intents.append(nlu_result["intent"])
            context["recent_intents"] = recent_intents[-5:]
            
            # Update entities
            if nlu_result.get("entities"):
                context["entities"].update(nlu_result["entities"])
            
            # Update language preference
            context["language"] = nlu_result["language"]
            
            # Update escalation status
            if search_result.get("escalate"):
                context["escalated"] = True
            
            # Increment turn count
            context["turn_count"] = context.get("turn_count", 0) + 1
            
            # Cache for 1 hour
            self.redis_client.setex(
                self._get_context_key(),
                3600,
                json.dumps(context, ensure_ascii=False)
            )
            
        except Exception as e:
            print(f"Context update error: {e}")
    
    def clear_context(self):
        """Clear conversation context"""
        try:
            self.redis_client.delete(self._get_context_key())
        except Exception as e:
            print(f"Context clear error: {e}")


class ResponseGenerator:
    def __init__(self):
        self.suggestion_templates = {
            "en": {
                "fees": ["What are the fee payment methods?", "When is the fee deadline?", "Can I pay fees in installments?"],
                "scholarship": ["What documents are required for scholarship?", "When do scholarship applications open?", "Am I eligible for scholarship?"],
                "timetable": ["Where can I download the timetable?", "Are there any schedule changes?", "What are the exam timings?"],
                "admission": ["What is the admission process?", "What documents are needed?", "When do admissions close?"],
                "exam": ["Where can I check my results?", "What is the exam schedule?", "How to apply for revaluation?"],
                "hostel": ["How to apply for hostel accommodation?", "What are the hostel fees?", "What facilities are available?"],
                "library": ["What are the library timings?", "How to renew books online?", "What databases are available?"]
            },
            "hi": {
                "fees": ["फीस भुगतान के तरीके क्या हैं?", "फीस की अंतिम तारीख कब है?", "क्या मैं किस्तों में फीस दे सकता हूं?"],
                "scholarship": ["छात्रवृत्ति के लिए कौन से दस्तावेज चाहिए?", "छात्रवृत्ति आवेदन कब खुलते हैं?", "क्या मैं छात्रवृत्ति के लिए योग्य हूं?"],
                "timetable": ["समय सारणी कहां से डाउनलोड करें?", "क्या कोई शेड्यूल में बदलाव है?", "परीक्षा का समय क्या है?"],
                "admission": ["प्रवेश प्रक्रिया क्या है?", "कौन से दस्तावेज चाहिए?", "प्रवेश कब बंद होते हैं?"],
                "exam": ["मैं अपना परिणाम कहां देख सकता हूं?", "परीक्षा का शेड्यूल क्या है?", "पुनर्मूल्यांकन के लिए कैसे आवेदन करें?"],
                "hostel": ["छात्रावास के लिए कैसे आवेदन करें?", "छात्रावास की फीस क्या है?", "कौन सी सुविधाएं उपलब्ध हैं?"],
                "library": ["पुस्तकालय का समय क्या है?", "ऑनलाइन किताबें कैसे नवीकृत करें?", "कौन से डेटाबेस उपलब्ध हैं?"]
            }
        }
    
    def generate_response(self, search_result: Dict, context: Dict, nlu_result: Dict) -> Dict:
        """Generate final response with suggestions"""
        response = {
            "response": search_result["answer"],
            "confidence": search_result["confidence"],
            "source": search_result["source"],
            "escalate": search_result.get("escalate", False)
        }
        
        # Add suggestions based on intent
        intent = nlu_result["intent"]
        language = nlu_result["language"]
        
        suggestions = self.suggestion_templates.get(language, self.suggestion_templates["en"])
        if intent in suggestions:
            response["suggestions"] = suggestions[intent]
        else:
            # Default suggestions
            if language == "hi":
                response["suggestions"] = ["मुझे और जानकारी चाहिए", "किसी व्यक्ति से बात करना चाहते हैं", "धन्यवाद"]
            else:
                response["suggestions"] = ["I need more information", "Talk to a human", "Thank you"]
        
        return response
from typing import List, Dict, Optional, Tuple
import json
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, text
import hashlib
from googletrans import Translator

from app.models.models import FAQ, Document
from app.core.database import redis_client
from app.core.config import settings

class MultilingualRetrievalPipeline:
    def __init__(self, db: Session):
        self.db = db
        self.redis_client = redis_client
        self.translator = Translator()
        
    def _get_cache_key(self, query: str, language: str = "en") -> str:
        """Generate cache key for query"""
        content = f"{query}:{language}"
        return f"query:{hashlib.md5(content.encode()).hexdigest()}"
    
    def _cache_response(self, key: str, response: Dict, ttl: int = 3600):
        """Cache response for quick retrieval"""
        try:
            self.redis_client.setex(key, ttl, json.dumps(response, ensure_ascii=False))
        except Exception as e:
            print(f"Cache error: {e}")
    
    def _get_cached_response(self, key: str) -> Optional[Dict]:
        """Get cached response"""
        try:
            cached = self.redis_client.get(key)
            if cached:
                return json.loads(cached)
        except Exception as e:
            print(f"Cache retrieval error: {e}")
        return None
    
    def _get_language_column(self, language: str, question: bool = True) -> str:
        """Get appropriate database column for language"""
        if question:
            return {
                'en': 'question_en',
                'hi': 'question_hi', 
                'mr': 'question_mr',
                'ta': 'question_ta',
                'te': 'question_te'
            }.get(language, 'question_en')
        else:
            return {
                'en': 'answer_en',
                'hi': 'answer_hi',
                'mr': 'answer_mr', 
                'ta': 'answer_ta',
                'te': 'answer_te'
            }.get(language, 'answer_en')
    
    def l1_faq_search(self, query: str, intent: str, language: str = "en") -> Optional[Dict]:
        """Level 1: Search curated FAQs with multilingual support"""
        cache_key = self._get_cache_key(f"faq:{query}", language)
        cached = self._get_cached_response(cache_key)
        if cached:
            return cached
        
        query_lower = query.lower()
        
        # Get appropriate language columns
        question_col = self._get_language_column(language, True)
        answer_col = self._get_language_column(language, False)
        
        # Build multilingual search query
        search_conditions = [
            func.lower(getattr(FAQ, question_col)).contains(query_lower),
            func.lower(FAQ.question_en).contains(query_lower)  # Always search English as fallback
        ]
        
        # Add keyword search
        search_conditions.append(FAQ.keywords.op('?')(query_lower))
        
        # Execute search
        faq_query = self.db.query(FAQ).filter(
            FAQ.is_active == True,
            or_(*search_conditions)
        )
        
        # Order by priority and limit results
        faqs = faq_query.order_by(FAQ.priority.desc()).limit(5).all()
        
        if faqs:
            best_faq = faqs[0]
            
            # Get answer in requested language, fallback to English
            answer = getattr(best_faq, answer_col) or best_faq.answer_en
            question = getattr(best_faq, question_col) or best_faq.question_en
            
            response = {
                "source": "faq",
                "confidence": 0.9,
                "answer": answer,
                "question": question,
                "category": best_faq.category,
                "faq_id": best_faq.id,
                "language": language
            }
            
            self._cache_response(cache_key, response)
            return response
        
        return None
    
    def l2_semantic_search(self, query: str, language: str = "en") -> Optional[Dict]:
        """Level 2: Semantic search through document corpus"""
        cache_key = self._get_cache_key(f"semantic:{query}", language)
        cached = self._get_cached_response(cache_key)
        if cached:
            return cached
        
        # Search through processed documents
        documents = self.db.query(Document).filter(
            Document.is_processed == True,
            or_(
                func.lower(Document.content).contains(query.lower()),
                Document.language == language
            )
        ).limit(3).all()
        
        if documents:
            # Simple relevance scoring based on keyword frequency
            best_doc = documents[0]
            content = best_doc.content[:500] + "..." if len(best_doc.content) > 500 else best_doc.content
            
            # Translate content if needed
            if language != 'en' and best_doc.language == 'en':
                try:
                    translated = self.translator.translate(content, dest=language)
                    content = translated.text
                except:
                    pass  # Keep original if translation fails
            
            response = {
                "source": "semantic",
                "confidence": 0.7,
                "answer": content,
                "document_id": best_doc.id,
                "filename": best_doc.filename,
                "language": language
            }
            
            self._cache_response(cache_key, response)
            return response
        
        return None
    
    def fallback_response(self, query: str, intent: str, language: str = "en") -> Dict:
        """Generate fallback response when no good match found"""
        fallback_messages = {
            "en": {
                "default": "I couldn't find a specific answer to your question. Let me connect you with our support team who can help you better. You can also call our helpline at +91-XXX-XXXXXXX or email at support@college.edu",
                "greeting": "Hello! I'm here to help you with your campus-related queries. What would you like to know about?",
                "fees": "For specific fee information, please contact the accounts office at accounts@college.edu or visit the admin building during office hours (9 AM - 5 PM).",
                "scholarship": "For scholarship queries, please visit the student welfare office or check our scholarship portal at portal.college.edu/scholarships",
                "timetable": "For the latest timetable, please check the academic portal or contact your department office.",
                "admission": "For admission information, please visit the admission office or check our website at college.edu/admissions",
                "exam": "For exam schedules and results, please check the academic portal or contact the examination cell.",
                "hostel": "For hostel accommodation, please contact the hostel office at hostel@college.edu or visit the hostel administration.",
                "library": "For library services, please visit the library or contact them at library@college.edu"
            },
            "hi": {
                "default": "मुझे आपके प्रश्न का विशिष्ट उत्तर नहीं मिला। आइए मैं आपको हमारी सहायता टीम से जोड़ता हूं जो आपकी बेहतर सहायता कर सकती है। आप हमारी हेल्पलाइन +91-XXX-XXXXXXX पर कॉल कर सकते हैं या support@college.edu पर ईमेल कर सकते हैं।",
                "greeting": "नमस्ते! मैं आपके कैंपस संबंधी प्रश्नों में सहायता के लिए यहाँ हूँ। आप क्या जानना चाहते हैं?",
                "fees": "फीस की विशिष्ट जानकारी के लिए, कृपया accounts@college.edu पर संपर्क करें या कार्यालयीन समय (सुबह 9 से शाम 5 बजे) में प्रशासन भवन में जाएं।",
                "scholarship": "छात्रवृत्ति संबंधी प्रश्नों के लिए, कृपया छात्र कल्याण कार्यालय में जाएं या हमारे छात्रवृत्ति पोर्टल portal.college.edu/scholarships की जांच करें।",
                "timetable": "नवीनतम समय सारणी के लिए, कृपया शैक्षणिक पोर्टल की जांच करें या अपने विभाग कार्यालय से संपर्क करें।",
                "admission": "प्रवेश की जानकारी के लिए, कृपया प्रवेश कार्यालय में जाएं या हमारी वेबसाइट college.edu/admissions देखें।",
                "exam": "परीक्षा कार्यक्रम और परिणामों के लिए, कृपया शैक्षणिक पोर्टल की जांच करें या परीक्षा सेल से संपर्क करें।",
                "hostel": "छात्रावास आवास के लिए, कृपया hostel@college.edu पर छात्रावास कार्यालय से संपर्क करें या छात्रावास प्रशासन में जाएं।",
                "library": "पुस्तकालय सेवाओं के लिए, कृपया पुस्तकालय में जाएं या library@college.edu पर संपर्क करें।"
            },
            "mr": {
                "default": "मला तुमच्या प्रश्नाचे विशिष्ट उत्तर सापडले नाही. मी तुम्हाला आमच्या सहाय्य संघाशी जोडतो जे तुम्हाला चांगली मदत करू शकतात. तुम्ही आमच्या हेल्पलाइनवर +91-XXX-XXXXXXX कॉल करू शकता किंवा support@college.edu वर ईमेल करू शकता.",
                "greeting": "नमस्कार! मी तुमच्या कॅम्पस संबंधित प्रश्नांमध्ये मदत करण्यासाठी येथे आहे. तुम्हाला काय जाणून घ्यायचे आहे?",
                "fees": "शुल्काच्या विशिष्ट माहितीसाठी, कृपया accounts@college.edu वर संपर्क साधा किंवा कार्यालयीन वेळेत (सकाळी 9 ते संध्याकाळी 5) प्रशासन इमारतीत जा.",
                "scholarship": "शिष्यवृत्ती संबंधी प्रश्नांसाठी, कृपया विद्यार्थी कल्याण कार्यालयात जा किंवा आमचे शिष्यवृत्ती पोर्टल portal.college.edu/scholarships तपासा.",
                "timetable": "नवीनतम वेळापत्रकासाठी, कृपया शैक्षणिक पोर्टल तपासा किंवा तुमच्या विभागाच्या कार्यालयाशी संपर्क साधा.",
                "admission": "प्रवेशाच्या माहितीसाठी, कृपया प्रवेश कार्यालयात जा किंवा आमची वेबसाइट college.edu/admissions पहा.",
                "exam": "परीक्षा वेळापत्रक आणि निकालांसाठी, कृपया शैक्षणिक पोर्टल तपासा किंवा परीक्षा सेलशी संपर्क साधा.",
                "hostel": "वसतिगृह निवासासाठी, कृपया hostel@college.edu वर वसतिगृह कार्यालयाशी संपर्क साधा किंवा वसतिगृह प्रशासनात जा.",
                "library": "वाचनालय सेवांसाठी, कृपया वाचनालयात जा किंवा library@college.edu वर संपर्क साधा."
            },
            "ta": {
                "default": "உங்கள் கேள்விக்கு குறிப்பிட்ட பதில் கிடைக்கவில்லை. எங்கள் ஆதரவு குழுவுடன் உங்களை இணைக்கிறேன், அவர்கள் உங்களுக்கு சிறந்த உதவி செய்ய முடியும். நீங்கள் எங்கள் உதவி எண் +91-XXX-XXXXXXX-ல் அழைக்கலாம் அல்லது support@college.edu-க்கு மின்னஞ்சல் அனுப்பலாம்.",
                "greeting": "வணக்கம்! உங்கள் கல்லூரி தொடர்பான கேள்விகளுக்கு உதவ நான் இங்கே இருக்கிறேன். நீங்கள் என்ன தெரிந்துகொள்ள விரும்புகிறீர்கள்?",
                "fees": "கட்டணம் பற்றிய குறிப்பிட்ட தகவலுக்கு, accounts@college.edu-ல் தொடர்பு கொள்ளுங்கள் அல்லது அலுவலக நேரத்தில் (காலை 9 முதல் மாலை 5 வரை) நிர்வாக கட்டடத்திற்கு செல்லுங்கள்.",
                "scholarship": "உதவித்தொகை கேள்விகளுக்கு, மாணவர் நல அலுவலகத்திற்கு செல்லுங்கள் அல்லது எங்கள் உதவித்தொகை போர்ட்டல் portal.college.edu/scholarships-ஐ சரிபார்க்கவும்.",
                "timetable": "சமீபத்திய நேர அட்டவணைக்கு, கல்வி போர்ட்டலை சரிபார்க்கவும் அல்லது உங்கள் துறை அலுவலகத்தை தொடர்பு கொள்ளுங்கள்.",
                "admission": "சேர்க்கை தகவலுக்கு, சேர்க்கை அலுவலகத்திற்கு செல்லுங்கள் அல்லது எங்கள் வலைத்தளம் college.edu/admissions-ஐ பார்க்கவும்.",
                "exam": "தேர்வு அட்டவணை மற்றும் முடிவுகளுக்கு, கல்வி போர்ட்டலை சரிபார்க்கவும் அல்லது தேர்வுப் பிரிவை தொடர்பு கொள்ளுங்கள்.",
                "hostel": "விடுதி தங்குமிடத்திற்கு, hostel@college.edu-ல் விடுதி அலுவலகத்தை தொடர்பு கொள்ளுங்கள் அல்லது விடுதி நிர்வாகத்திற்கு செல்லுங்கள்.",
                "library": "நூலக சேவைகளுக்கு, நூலகத்திற்கு செல்லுங்கள் அல்லது library@college.edu-ல் தொடர்பு கொள்ளுங்கள்."
            },
            "te": {
                "default": "మీ ప్రశ్నకు నిర్దిష్ట సమాధానం దొరకలేదు. మీకు మెరుగైన సహాయం చేయగల మా సపోర్ట్ టీమ్‌తో మిమ్మల్ని కనెక్ట్ చేస్తున్నాను. మీరు మా హెల్ప్‌లైన్ +91-XXX-XXXXXXX కు కాల్ చేయవచ్చు లేదా support@college.edu కు ఇమెయిల్ చేయవచ్చు.",
                "greeting": "నమస్కారం! మీ క్యాంపస్ సంబంధిత ప్రశ్నలకు సహాయం చేయడానికి నేను ఇక్కడ ఉన్నాను. మీరు ఏమి తెలుసుకోవాలని అనుకుంటున్నారు?",
                "fees": "ఫీజుల నిర్దిష్ట సమాచారం కోసం, accounts@college.edu కు సంప్రదించండి లేదా కార్యాలయ వేళలలో (ఉదయం 9 నుండి సాయంత్రం 5 వరకు) అడ్మిన్ భవనానికి వెళ్లండి.",
                "scholarship": "స్కాలర్‌షిప్ ప్రశ్నల కోసం, విద్యార్థి సంక్షేమ కార్యాలయానికి వెళ్లండి లేదా మా స్కాలర్‌షిప్ పోర్టల్ portal.college.edu/scholarships చూడండి.",
                "timetable": "తాజా టైమ్‌టేబుల్ కోసం, అకడమిక్ పోర్టల్ చూడండి లేదా మీ విభాగ కార్యాలయాన్ని సంప్రదించండి.",
                "admission": "అడ్మిషన్ సమాచారం కోసం, అడ్మిషన్ కార్యాలయానికి వెళ్లండి లేదా మా వెబ్‌సైట్ college.edu/admissions చూడండి.",
                "exam": "పరీక్ష షెడ్యూల్స్ మరియు రిజల్ట్స్ కోసం, అకడమిక్ పోర్టల్ చూడండి లేదా ఎగ్జామినేషన్ సెల్‌ను సంప్రదించండి.",
                "hostel": "హాస్టల్ వసతి కోసం, hostel@college.edu వద్ద హాస్టల్ కార్యాలయాన్ని సంప్రదించండి లేదా హాస్టల్ అడ్మినిస్ట్రేషన్‌కు వెళ్లండి.",
                "library": "లైబ్రరీ సేవల కోసం, లైబ్రరీకి వెళ్లండి లేదా library@college.edu వద్ద సంప్రదించండి."
            }
        }
        
        messages = fallback_messages.get(language, fallback_messages["en"])
        message = messages.get(intent, messages["default"])
        
        return {
            "source": "fallback",
            "confidence": 0.3,
            "answer": message,
            "escalate": True,
            "language": language
        }
    
    def search(self, query: str, intent: str, language: str = "en") -> Dict:
        """Main search function that tries L1, then L2, then fallback"""
        # Try L1 FAQ search first
        result = self.l1_faq_search(query, intent, language)
        if result and result["confidence"] >= settings.CONFIDENCE_THRESHOLD:
            return result
        
        # Try L2 semantic search
        result = self.l2_semantic_search(query, language)
        if result and result["confidence"] >= settings.FALLBACK_THRESHOLD:
            return result
        
        # Fallback response
        return self.fallback_response(query, intent, language)
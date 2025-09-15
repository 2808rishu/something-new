from typing import Dict, List, Tuple, Optional
import re
from langdetect import detect
import json
from googletrans import Translator

class MultilingualNLU:
    def __init__(self):
        self.translator = Translator()
        
        # Enhanced intent patterns for multiple languages
        self.intent_patterns = {
            "greeting": {
                "en": [r"(hello|hi|hey|good morning|good afternoon|good evening)", r"(how are you|what's up)"],
                "hi": [r"(नमस्ते|नमस्कार|हैलो|हाय)", r"(क्या हाल है|कैसे हैं आप)"],
                "mr": [r"(नमस्कार|नमस्ते|हॅलो)", r"(कसे आहात|काय चालू आहे)"],
                "ta": [r"(வணக்கம்|ஹலோ)", r"(எப்படி இருக்கீங்க|என்ன நடக்குது)"],
                "te": [r"(నమస్కారం|హలో)", r"(ఎలా ఉన్నారు|ఏమి జరుగుతోంది)"]
            },
            "fees": {
                "en": [r"(fee|fees|payment|tuition|cost|charges|amount)", r"(how much|price|expense)"],
                "hi": [r"(शुल्क|फीस|भुगतान|पैसा)", r"(कितना|दाम|खर्च)"],
                "mr": [r"(शुल्क|फी|पैसे|खर्च)", r"(किती|दर|पेमेंट)"],
                "ta": [r"(கட்டணம்|பணம்|செலுத்த)", r"(எவ்வளவு|விலை|செலவு)"],
                "te": [r"(ఫీజు|డబ్బు|చెల్లింపు)", r"(ఎంత|ధర|ఖర్చు)"]
            },
            "scholarship": {
                "en": [r"(scholarship|scholership|financial aid|grant|stipend)", r"(free education|merit)"],
                "hi": [r"(छात्रवृत्ति|वजीफा|सहायता)", r"(मुफ्त शिक्षा|मेरिट)"],
                "mr": [r"(शिष्यवृत्ती|वजीफा|मदत)", r"(मोफत शिक्षण|गुणवत्ता)"],
                "ta": [r"(உதவித்தொகை|கல்வி உதவி)", r"(இலவச கல்வி|தகுதி)"],
                "te": [r"(స్కాలర్‌షిప్|విద్య సహాయం)", r"(ఉచిత విద్య|మెరిట్)"]
            },
            "timetable": {
                "en": [r"(timetable|schedule|class timing|lecture|time)", r"(when|what time|timing)"],
                "hi": [r"(समय सारणी|कक्षा का समय|लेक्चर)", r"(कब|क्या समय|टाइमिंग)"],
                "mr": [r"(वेळापत्रक|वर्गाचा वेळ|व्याख्यान)", r"(केव्हा|काय वेळ|टाइमिंग)"],
                "ta": [r"(நேர அட்டவணை|வகுப்பு நேரம்|விரிவுரை)", r"(எப்போது|என்ன நேரம்|டைமிங்)"],
                "te": [r"(టైం టేబుల్|క్లాస్ టైమ్|లెక్చర్)", r"(ఎప్పుడు|ఏ సమయం|టైమింగ్)"]
            },
            "admission": {
                "en": [r"(admission|admision|enrollment|registration|apply)", r"(join|entry|application)"],
                "hi": [r"(प्रवेश|दाखिला|रजिस्ट्रेशन)", r"(आवेदन|एप्लीकेशन|जॉइन)"],
                "mr": [r"(प्रवेश|दाखला|नोंदणी)", r"(अर्ज|अप्लिकेशन|सामील)"],
                "ta": [r"(சேர்க்கை|பதிவு|விண்ணப்பம்)", r"(சேர|நுழைவு|அப்ளிகேஷன்)"],
                "te": [r"(అడ్మిషన్|ప్రవేశం|రిజిస్ట్రేషన్)", r"(చేరడం|ఎంట్రీ|అప్లికేషన్)"]
            },
            "exam": {
                "en": [r"(exam|examination|test|result|marks|grade)", r"(score|assessment|evaluation)"],
                "hi": [r"(परीक्षा|इम्तिहान|टेस्ट|नतीजा|अंक)", r"(स्कोर|मूल्यांकन|ग्रेड)"],
                "mr": [r"(परीक्षा|चाचणी|निकाल|गुण)", r"(स्कोअर|मूल्यमापन|ग्रेड)"],
                "ta": [r"(தேர்வு|பரீட்சை|டெஸ்ட்|முடிவு|மதிப்பெண்)", r"(ஸ்கோர்|மதிப்பீடு|கிரேடு)"],
                "te": [r"(పరీక్ష|టెస్ట్|రిజల్ట్|మార్కులు)", r"(స్కోర్|అసెస్మెంట్|గ్రేడ్)"]
            },
            "hostel": {
                "en": [r"(hostel|accommodation|room|dormitory|stay)", r"(residence|housing|lodge)"],
                "hi": [r"(छात्रावास|कमरा|निवास|रहना)", r"(आवास|हाउसिंग|लॉज)"],
                "mr": [r"(वसतिगृह|खोली|निवास|राहणे)", r"(आवास|हाउसिंग|लॉज)"],
                "ta": [r"(விடுதி|அறை|தங்குமிடம்|தங்க)", r"(குடியிருப்பு|வீட்டுவசதி|லாஜ்)"],
                "te": [r"(హాస్టల్|గది|నివాసం|ఉండటం)", r"(వసతి|హౌసింగ్|లాడ్జ్)"]
            },
            "library": {
                "en": [r"(library|books|issue|return|borrow)", r"(reading|study|reference)"],
                "hi": [r"(पुस्तकालय|किताब|इश्यू|वापसी)", r"(पढ़ना|अध्ययन|संदर्भ)"],
                "mr": [r"(वाचनालय|पुस्तक|इश्यू|परतावा)", r"(वाचन|अभ्यास|संदर्भ)"],
                "ta": [r"(நூலகம்|புத்தகம்|வழங்க|திரும்ப)", r"(படிக்க|படிப்பு|குறிப்பு)"],
                "te": [r"(లైబ్రరీ|పుస్తకం|ఇష్యూ|రిటర్న్)", r"(చదవడం|చదువు|రిఫరెన్స్)"]
            }
        }
        
    def detect_language(self, text: str) -> str:
        """Enhanced language detection"""
        try:
            lang = detect(text)
            # Map various Indian language codes to supported ones
            lang_mapping = {
                'hi': 'hi', 'mr': 'mr', 'ta': 'ta', 'te': 'te',
                'bn': 'hi', 'gu': 'hi', 'kn': 'hi', 'ml': 'hi',
                'pa': 'hi', 'or': 'hi', 'as': 'hi', 'ur': 'hi'
            }
            return lang_mapping.get(lang, 'en')
        except:
            # Fallback: detect based on script
            if any('\u0900' <= char <= '\u097F' for char in text):  # Devanagari
                return 'hi'
            elif any('\u0B80' <= char <= '\u0BFF' for char in text):  # Tamil
                return 'ta'
            elif any('\u0C00' <= char <= '\u0C7F' for char in text):  # Telugu
                return 'te'
            return 'en'
    
    def extract_intent(self, text: str, language: str = 'en') -> Tuple[str, float]:
        """Extract intent with multilingual support"""
        text_lower = text.lower()
        best_intent = "general"
        best_confidence = 0.0
        
        for intent, lang_patterns in self.intent_patterns.items():
            patterns = lang_patterns.get(language, lang_patterns.get('en', []))
            for pattern in patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    confidence = len(matches) * 0.3 + 0.4  # Base confidence
                    if confidence > best_confidence:
                        best_intent = intent
                        best_confidence = min(confidence, 0.95)
        
        return best_intent, best_confidence
    
    def extract_entities(self, text: str, intent: str, language: str = 'en') -> Dict:
        """Extract entities based on intent and language"""
        entities = {}
        
        if intent == "fees":
            # Extract academic year, semester, course
            year_patterns = {
                'en': [r'(20\d{2})', r'(first|second|third|fourth)', r'(1st|2nd|3rd|4th)'],
                'hi': [r'(पहला|दूसरा|तीसरा|चौथा)', r'(प्रथम|द्वितीय|तृतीय|चतुर्थ)'],
                'mr': [r'(पहिला|दुसरा|तिसरा|चौथा)', r'(प्रथम|द्वितीय|तृतीय|चतुर्थ)']
            }
            
            patterns = year_patterns.get(language, year_patterns['en'])
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    entities['academic_year'] = match.group(1)
                    break
                    
        elif intent == "exam":
            exam_patterns = {
                'en': [r'(mid|final|internal|external|practical|theory)'],
                'hi': [r'(मध्यावधि|अंतिम|आंतरिक|बाहरी|प्रैक्टिकल|सिद्धांत)'],
                'mr': [r'(मध्यावधी|अंतिम|अंतर्गत|बाह्य|प्रात्यक्षिक|सिद्धांत)']
            }
            
            patterns = exam_patterns.get(language, exam_patterns['en'])
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    entities['exam_type'] = match.group(1)
                    break
        
        return entities
    
    def translate_text(self, text: str, target_lang: str) -> str:
        """Translate text to target language"""
        try:
            if target_lang == 'en':
                return text
            
            # Map our language codes to Google Translate codes
            lang_map = {'hi': 'hi', 'mr': 'mr', 'ta': 'ta', 'te': 'te'}
            target = lang_map.get(target_lang, 'en')
            
            result = self.translator.translate(text, dest=target)
            return result.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def process_query(self, text: str, preferred_language: str = None) -> Dict:
        """Complete multilingual NLU processing pipeline"""
        detected_language = self.detect_language(text)
        language = preferred_language or detected_language
        
        intent, confidence = self.extract_intent(text, language)
        entities = self.extract_entities(text, intent, language)
        
        # Translate to English for backend processing if needed
        text_en = text if language == 'en' else self.translate_text(text, 'en')
        
        return {
            "original_text": text,
            "text_en": text_en,
            "detected_language": detected_language,
            "language": language,
            "intent": intent,
            "confidence": confidence,
            "entities": entities
        }
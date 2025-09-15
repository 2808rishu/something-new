/**
 * Campus AI Assistant - Embeddable Chat Widget
 * A multilingual chatbot widget that can be embedded on any website
 */

class CampusAIChatWidget {
    constructor(config = {}) {
        this.config = {
            apiBaseUrl: config.apiBaseUrl || 'http://localhost:8000/api/v1',
            theme: config.theme || 'light',
            position: config.position || 'bottom-right',
            language: config.language || 'en',
            welcomeMessage: config.welcomeMessage || null,
            ...config
        };
        
        this.conversationId = null;
        this.currentLanguage = this.config.language;
        this.isOpen = false;
        this.isTyping = false;
        this.messageHistory = [];
        
        this.init();
    }
    
    init() {
        this.createWidgetHTML();
        this.attachEventListeners();
        this.loadLanguage(this.currentLanguage);
        this.setupKeyboardShortcuts();
    }
    
    createWidgetHTML() {
        // Check if widget already exists
        if (document.getElementById('campus-chatbot-widget')) {
            return;
        }
        
        const widgetHTML = `
            <div id="campus-chatbot-widget" class="widget-container">
                <div id="widget-button" class="widget-button">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
                    </svg>
                    <span class="widget-badge" id="unread-count" style="display: none;">1</span>
                </div>

                <div id="chat-window" class="chat-window hidden">
                    <div class="chat-header">
                        <div class="header-info">
                            <div class="header-title">
                                <h3>Campus Assistant</h3>
                                <div class="language-selector">
                                    <select id="language-select">
                                        <option value="en">English</option>
                                        <option value="hi">हिन्दी</option>
                                        <option value="mr">मराठी</option>
                                        <option value="ta">தமிழ்</option>
                                        <option value="te">తెలుగు</option>
                                    </select>
                                </div>
                            </div>
                            <span class="status online">Online</span>
                        </div>
                        <div class="header-controls">
                            <button id="minimize-btn" class="control-btn" title="Minimize">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M6 19h12v2H6z"/>
                                </svg>
                            </button>
                            <button id="close-btn" class="control-btn" title="Close">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div class="messages-container" id="messages-container">
                        <div class="welcome-message">
                            <div class="bot-message">
                                <div class="message-avatar">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                                    </svg>
                                </div>
                                <div class="message-content">
                                    <p id="welcome-text">Hello! I'm here to help with your campus queries. Ask me about fees, admissions, schedules, and more!</p>
                                    <div class="message-time">Now</div>
                                </div>
                            </div>
                        </div>
                        <div class="suggestions-container" id="suggestions-container">
                            <div class="suggestion-chip" data-text="What are the admission requirements?">Admission Requirements</div>
                            <div class="suggestion-chip" data-text="How much are the fees?">Fee Information</div>
                            <div class="suggestion-chip" data-text="Show me the timetable">Class Schedule</div>
                            <div class="suggestion-chip" data-text="Scholarship information">Scholarships</div>
                        </div>
                    </div>

                    <div class="typing-indicator" id="typing-indicator" style="display: none;">
                        <div class="typing-avatar">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                            </svg>
                        </div>
                        <div class="typing-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>

                    <div class="input-area">
                        <div class="input-container">
                            <input 
                                type="text" 
                                id="message-input" 
                                placeholder="Type your question here..." 
                                maxlength="500"
                            />
                            <button id="send-btn" class="send-btn" disabled>
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                                </svg>
                            </button>
                        </div>
                        <div class="input-footer">
                            <span class="powered-by">Powered by Campus AI Assistant</span>
                            <button id="escalate-btn" class="escalate-btn" title="Talk to human">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Inject CSS
        this.injectCSS();
        
        // Add widget to page
        document.body.insertAdjacentHTML('beforeend', widgetHTML);
    }
    
    injectCSS() {
        if (document.getElementById('campus-widget-styles')) {
            return;
        }
        
        const link = document.createElement('link');
        link.id = 'campus-widget-styles';
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/gh/yourusername/campus-ai-assistant@main/chatbot-widget/dist/styles.css';
        document.head.appendChild(link);
    }
    
    attachEventListeners() {
        const widgetButton = document.getElementById('widget-button');
        const closeBtn = document.getElementById('close-btn');
        const minimizeBtn = document.getElementById('minimize-btn');
        const sendBtn = document.getElementById('send-btn');
        const messageInput = document.getElementById('message-input');
        const languageSelect = document.getElementById('language-select');
        const escalateBtn = document.getElementById('escalate-btn');
        
        // Widget toggle
        widgetButton.addEventListener('click', () => this.toggleWidget());
        closeBtn.addEventListener('click', () => this.closeWidget());
        minimizeBtn.addEventListener('click', () => this.minimizeWidget());
        
        // Message handling
        sendBtn.addEventListener('click', () => this.sendMessage());
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        messageInput.addEventListener('input', () => {
            sendBtn.disabled = !messageInput.value.trim();
        });
        
        // Language change
        languageSelect.addEventListener('change', (e) => {
            this.changeLanguage(e.target.value);
        });
        
        // Suggestion chips
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('suggestion-chip')) {
                const text = e.target.dataset.text;
                this.sendMessage(text);
            }
        });
        
        // Escalate to human
        escalateBtn.addEventListener('click', () => this.escalateToHuman());
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Alt + C to toggle widget
            if (e.altKey && e.key === 'c') {
                e.preventDefault();
                this.toggleWidget();
            }
            
            // Escape to close widget
            if (e.key === 'Escape' && this.isOpen) {
                this.closeWidget();
            }
        });
    }
    
    toggleWidget() {
        const chatWindow = document.getElementById('chat-window');
        
        if (this.isOpen) {
            this.closeWidget();
        } else {
            chatWindow.classList.remove('hidden');
            this.isOpen = true;
            document.getElementById('message-input').focus();
            this.hideUnreadBadge();
        }
    }
    
    closeWidget() {
        const chatWindow = document.getElementById('chat-window');
        chatWindow.classList.add('hidden');
        this.isOpen = false;
    }
    
    minimizeWidget() {
        this.closeWidget();
        this.showUnreadBadge();
    }
    
    showUnreadBadge() {
        document.getElementById('unread-count').style.display = 'flex';
    }
    
    hideUnreadBadge() {
        document.getElementById('unread-count').style.display = 'none';
    }
    
    async sendMessage(text = null) {
        const messageInput = document.getElementById('message-input');
        const message = text || messageInput.value.trim();
        
        if (!message) return;
        
        // Clear input
        messageInput.value = '';
        document.getElementById('send-btn').disabled = true;
        
        // Add user message to chat
        this.addMessage('user', message);
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await this.callAPI('/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversation_id: this.conversationId,
                    platform: 'web',
                    language: this.currentLanguage,
                    website_domain: window.location.hostname
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.conversationId = data.conversation_id;
                
                // Add bot response
                this.addMessage('bot', data.response, {
                    confidence: data.confidence,
                    source: data.source,
                    suggestions: data.suggestions
                });
                
                // Update language if detected differently
                if (data.detected_language !== this.currentLanguage) {
                    this.currentLanguage = data.detected_language;
                    document.getElementById('language-select').value = this.currentLanguage;
                }
                
                // Handle escalation
                if (data.escalate) {
                    this.handleEscalation();
                }
                
            } else {
                this.addMessage('bot', 'Sorry, I encountered an error. Please try again.', {
                    isError: true
                });
            }
        } catch (error) {
            console.error('Chat API Error:', error);
            this.addMessage('bot', 'Sorry, I\'m having trouble connecting. Please check your internet connection and try again.', {
                isError: true
            });
        } finally {
            this.hideTypingIndicator();
        }
    }
    
    addMessage(sender, text, metadata = {}) {
        const messagesContainer = document.getElementById('messages-container');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message fade-in`;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                ${sender === 'bot' ? 
                    '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>' :
                    '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>'
                }
            </div>
            <div class="message-content">
                <p>${this.escapeHtml(text)}</p>
                <div class="message-time">${timeString}</div>
                ${metadata.confidence ? `<div class="confidence-score">Confidence: ${Math.round(metadata.confidence * 100)}%</div>` : ''}
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        
        // Add suggestions if provided
        if (metadata.suggestions && metadata.suggestions.length > 0) {
            this.updateSuggestions(metadata.suggestions);
        }
        
        // Scroll to bottom
        this.scrollToBottom();
        
        // Store in history
        this.messageHistory.push({
            sender,
            text,
            timestamp: now,
            metadata
        });
    }
    
    updateSuggestions(suggestions) {
        const suggestionsContainer = document.getElementById('suggestions-container');
        suggestionsContainer.innerHTML = '';
        
        suggestions.forEach(suggestion => {
            const chip = document.createElement('div');
            chip.className = 'suggestion-chip';
            chip.dataset.text = suggestion;
            chip.textContent = suggestion;
            suggestionsContainer.appendChild(chip);
        });
    }
    
    showTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        indicator.style.display = 'flex';
        this.isTyping = true;
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        indicator.style.display = 'none';
        this.isTyping = false;
    }
    
    scrollToBottom() {
        const container = document.getElementById('messages-container');
        container.scrollTop = container.scrollHeight;
    }
    
    async changeLanguage(language) {
        this.currentLanguage = language;
        await this.loadLanguage(language);
        
        // Update welcome message
        const welcomeMessages = {
            'en': 'Hello! I\'m here to help with your campus queries. Ask me about fees, admissions, schedules, and more!',
            'hi': 'नमस्ते! मैं आपके कैंपस संबंधी प्रश्नों में सहायता के लिए यहाँ हूँ। फीस, प्रवेश, समय सारणी आदि के बारे में पूछें!',
            'mr': 'नमस्कार! मी तुमच्या कॅम्पस संबंधित प्रश्नांमध्ये मदत करण्यासाठी येथे आहे. शुल्क, प्रवेश, वेळापत्रक इत्यादीबद्दल विचारा!',
            'ta': 'வணக்கம்! உங்கள் கல்லூரி தொடர்பான கேள்விகளுக்கு உதவ நான் இங்கே இருக்கிறேன். கட்டணம், சேர்க்கை, அட்டவணை போன்றவற்றைப் பற்றி கேளுங்கள்!',
            'te': 'నమస్కారం! మీ క్యాంపస్ సంబంధిత ప్రశ్నలకు సహాయం చేయడానికి నేను ఇక్కడ ఉన్నాను. ఫీజులు, అడ్మిషన్లు, షెడ్యూల్స్ గురించి అడగండి!'
        };
        
        document.getElementById('welcome-text').textContent = welcomeMessages[language] || welcomeMessages['en'];
        
        // Update input placeholder
        const placeholders = {
            'en': 'Type your question here...',
            'hi': 'यहाँ अपना प्रश्न लिखें...',
            'mr': 'तुमचा प्रश्न येथे लिहा...',
            'ta': 'உங்கள் கேள்வியை இங்கே தட்டச்சு செய்யுங்கள்...',
            'te': 'మీ ప్రశ్నను ఇక్కడ టైప్ చేయండి...'
        };
        
        document.getElementById('message-input').placeholder = placeholders[language] || placeholders['en'];
    }
    
    async loadLanguage(language) {
        // This could load language-specific content, suggestions, etc.
        // For now, we'll just update the UI elements
    }
    
    async escalateToHuman() {
        if (!this.conversationId) {
            this.addMessage('bot', 'Please start a conversation first before requesting human assistance.');
            return;
        }
        
        try {
            const response = await this.callAPI('/chat/escalate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    conversation_id: this.conversationId,
                    reason: 'User requested human assistance'
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.addMessage('bot', data.message);
            } else {
                this.addMessage('bot', 'Sorry, I couldn\'t escalate your request right now. Please try again later.');
            }
        } catch (error) {
            console.error('Escalation Error:', error);
            this.addMessage('bot', 'Sorry, I couldn\'t escalate your request right now. Please try again later.');
        }
    }
    
    handleEscalation() {
        // Add a special message indicating escalation
        this.addMessage('bot', 'I\'ve escalated your query to our support team. They will contact you shortly. Is there anything else I can help you with in the meantime?');
    }
    
    async callAPI(endpoint, options = {}) {
        const url = `${this.config.apiBaseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        return fetch(url, { ...defaultOptions, ...options });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Public methods for external integration
    open() {
        if (!this.isOpen) {
            this.toggleWidget();
        }
    }
    
    close() {
        if (this.isOpen) {
            this.closeWidget();
        }
    }
    
    sendPredefinedMessage(message) {
        if (!this.isOpen) {
            this.open();
        }
        setTimeout(() => {
            this.sendMessage(message);
        }, 300);
    }
    
    setLanguage(language) {
        this.changeLanguage(language);
    }
    
    getConversationHistory() {
        return this.messageHistory;
    }
}

// Auto-initialize widget if script has data attributes
document.addEventListener('DOMContentLoaded', () => {
    const scripts = document.querySelectorAll('script[src*="chatbot-widget.js"]');
    const script = scripts[scripts.length - 1]; // Get the current script
    
    if (script && (script.dataset.autoInit !== 'false')) {
        const config = {
            apiBaseUrl: script.dataset.apiUrl || 'http://localhost:8000/api/v1',
            language: script.dataset.language || 'en',
            theme: script.dataset.theme || 'light'
        };
        
        window.campusAIWidget = new CampusAIChatWidget(config);
    }
});

// Expose class globally for manual initialization
window.CampusAIChatWidget = CampusAIChatWidget;/**
 * Campus AI Assistant - Embeddable Chat Widget
 * A multilingual chatbot widget that can be embedded on any website
 */

class CampusAIChatWidget {
    constructor(config = {}) {
        this.config = {
            apiBaseUrl: config.apiBaseUrl || 'http://localhost:8000/api/v1',
            theme: config.theme || 'light',
            position: config.position || 'bottom-right',
            language: config.language || 'en',
            welcomeMessage: config.welcomeMessage || null,
            ...config
        };
        
        this.conversationId = null;
        this.currentLanguage = this.config.language;
        this.isOpen = false;
        this.isTyping = false;
        this.messageHistory = [];
        
        this.init();
    }
    
    init() {
        this.createWidgetHTML();
        this.attachEventListeners();
        this.loadLanguage(this.currentLanguage);
        this.setupKeyboardShortcuts();
    }
    
    createWidgetHTML() {
        // Check if widget already exists
        if (document.getElementById('campus-chatbot-widget')) {
            return;
        }
        
        const widgetHTML = `
            <div id="campus-chatbot-widget" class="widget-container">
                <div id="widget-button" class="widget-button">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
                    </svg>
                    <span class="widget-badge" id="unread-count" style="display: none;">1</span>
                </div>

                <div id="chat-window" class="chat-window hidden">
                    <div class="chat-header">
                        <div class="header-info">
                            <div class="header-title">
                                <h3>Campus Assistant</h3>
                                <div class="language-selector">
                                    <select id="language-select">
                                        <option value="en">English</option>
                                        <option value="hi">हिन्दी</option>
                                        <option value="mr">मराठी</option>
                                        <option value="ta">தமிழ்</option>
                                        <option value="te">తెలుగు</option>
                                    </select>
                                </div>
                            </div>
                            <span class="status online">Online</span>
                        </div>
                        <div class="header-controls">
                            <button id="minimize-btn" class="control-btn" title="Minimize">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M6 19h12v2H6z"/>
                                </svg>
                            </button>
                            <button id="close-btn" class="control-btn" title="Close">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div class="messages-container" id="messages-container">
                        <div class="welcome-message">
                            <div class="bot-message">
                                <div class="message-avatar">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                                    </svg>
                                </div>
                                <div class="message-content">
                                    <p id="welcome-text">Hello! I'm here to help with your campus queries. Ask me about fees, admissions, schedules, and more!</p>
                                    <div class="message-time">Now</div>
                                </div>
                            </div>
                        </div>
                        <div class="suggestions-container" id="suggestions-container">
                            <div class="suggestion-chip" data-text="What are the admission requirements?">Admission Requirements</div>
                            <div class="suggestion-chip" data-text="How much are the fees?">Fee Information</div>
                            <div class="suggestion-chip" data-text="Show me the timetable">Class Schedule</div>
                            <div class="suggestion-chip" data-text="Scholarship information">Scholarships</div>
                        </div>
                    </div>

                    <div class="typing-indicator" id="typing-indicator" style="display: none;">
                        <div class="typing-avatar">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                            </svg>
                        </div>
                        <div class="typing-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>

                    <div class="input-area">
                        <div class="input-container">
                            <input 
                                type="text" 
                                id="message-input" 
                                placeholder="Type your question here..." 
                                maxlength="500"
                            />
                            <button id="send-btn" class="send-btn" disabled>
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                                </svg>
                            </button>
                        </div>
                        <div class="input-footer">
                            <span class="powered-by">Powered by Campus AI Assistant</span>
                            <button id="escalate-btn" class="escalate-btn" title="Talk to human">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Inject CSS
        this.injectCSS();
        
        // Add widget to page
        document.body.insertAdjacentHTML('beforeend', widgetHTML);
    }
    
    injectCSS() {
        if (document.getElementById('campus-widget-styles')) {
            return;
        }
        
        const link = document.createElement('link');
        link.id = 'campus-widget-styles';
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/gh/yourusername/campus-ai-assistant@main/chatbot-widget/dist/styles.css';
        document.head.appendChild(link);
    }
    
    attachEventListeners() {
        const widgetButton = document.getElementById('widget-button');
        const closeBtn = document.getElementById('close-btn');
        const minimizeBtn = document.getElementById('minimize-btn');
        const sendBtn = document.getElementById('send-btn');
        const messageInput = document.getElementById('message-input');
        const languageSelect = document.getElementById('language-select');
        const escalateBtn = document.getElementById('escalate-btn');
        
        // Widget toggle
        widgetButton.addEventListener('click', () => this.toggleWidget());
        closeBtn.addEventListener('click', () => this.closeWidget());
        minimizeBtn.addEventListener('click', () => this.minimizeWidget());
        
        // Message handling
        sendBtn.addEventListener('click', () => this.sendMessage());
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        messageInput.addEventListener('input', () => {
            sendBtn.disabled = !messageInput.value.trim();
        });
        
        // Language change
        languageSelect.addEventListener('change', (e) => {
            this.changeLanguage(e.target.value);
        });
        
        // Suggestion chips
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('suggestion-chip')) {
                const text = e.target.dataset.text;
                this.sendMessage(text);
            }
        });
        
        // Escalate to human
        escalateBtn.addEventListener('click', () => this.escalateToHuman());
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Alt + C to toggle widget
            if (e.altKey && e.key === 'c') {
                e.preventDefault();
                this.toggleWidget();
            }
            
            // Escape to close widget
            if (e.key === 'Escape' && this.isOpen) {
                this.closeWidget();
            }
        });
    }
    
    toggleWidget() {
        const chatWindow = document.getElementById('chat-window');
        
        if (this.isOpen) {
            this.closeWidget();
        } else {
            chatWindow.classList.remove('hidden');
            this.isOpen = true;
            document.getElementById('message-input').focus();
            this.hideUnreadBadge();
        }
    }
    
    closeWidget() {
        const chatWindow = document.getElementById('chat-window');
        chatWindow.classList.add('hidden');
        this.isOpen = false;
    }
    
    minimizeWidget() {
        this.closeWidget();
        this.showUnreadBadge();
    }
    
    showUnreadBadge() {
        document.getElementById('unread-count').style.display = 'flex';
    }
    
    hideUnreadBadge() {
        document.getElementById('unread-count').style.display = 'none';
    }
    
    async sendMessage(text = null) {
        const messageInput = document.getElementById('message-input');
        const message = text || messageInput.value.trim();
        
        if (!message) return;
        
        // Clear input
        messageInput.value = '';
        document.getElementById('send-btn').disabled = true;
        
        // Add user message to chat
        this.addMessage('user', message);
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await this.callAPI('/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversation_id: this.conversationId,
                    platform: 'web',
                    language: this.currentLanguage,
                    website_domain: window.location.hostname
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.conversationId = data.conversation_id;
                
                // Add bot response
                this.addMessage('bot', data.response, {
                    confidence: data.confidence,
                    source: data.source,
                    suggestions: data.suggestions
                });
                
                // Update language if detected differently
                if (data.detected_language !== this.currentLanguage) {
                    this.currentLanguage = data.detected_language;
                    document.getElementById('language-select').value = this.currentLanguage;
                }
                
                // Handle escalation
                if (data.escalate) {
                    this.handleEscalation();
                }
                
            } else {
                this.addMessage('bot', 'Sorry, I encountered an error. Please try again.', {
                    isError: true
                });
            }
        } catch (error) {
            console.error('Chat API Error:', error);
            this.addMessage('bot', 'Sorry, I\'m having trouble connecting. Please check your internet connection and try again.', {
                isError: true
            });
        } finally {
            this.hideTypingIndicator();
        }
    }
    
    addMessage(sender, text, metadata = {}) {
        const messagesContainer = document.getElementById('messages-container');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message fade-in`;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                ${sender === 'bot' ? 
                    '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>' :
                    '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>'
                }
            </div>
            <div class="message-content">
                <p>${this.escapeHtml(text)}</p>
                <div class="message-time">${timeString}</div>
                ${metadata.confidence ? `<div class="confidence-score">Confidence: ${Math.round(metadata.confidence * 100)}%</div>` : ''}
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        
        // Add suggestions if provided
        if (metadata.suggestions && metadata.suggestions.length > 0) {
            this.updateSuggestions(metadata.suggestions);
        }
        
        // Scroll to bottom
        this.scrollToBottom();
        
        // Store in history
        this.messageHistory.push({
            sender,
            text,
            timestamp: now,
            metadata
        });
    }
    
    updateSuggestions(suggestions) {
        const suggestionsContainer = document.getElementById('suggestions-container');
        suggestionsContainer.innerHTML = '';
        
        suggestions.forEach(suggestion => {
            const chip = document.createElement('div');
            chip.className = 'suggestion-chip';
            chip.dataset.text = suggestion;
            chip.textContent = suggestion;
            suggestionsContainer.appendChild(chip);
        });
    }
    
    showTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        indicator.style.display = 'flex';
        this.isTyping = true;
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        indicator.style.display = 'none';
        this.isTyping = false;
    }
    
    scrollToBottom() {
        const container = document.getElementById('messages-container');
        container.scrollTop = container.scrollHeight;
    }
    
    async changeLanguage(language) {
        this.currentLanguage = language;
        await this.loadLanguage(language);
        
        // Update welcome message
        const welcomeMessages = {
            'en': 'Hello! I\'m here to help with your campus queries. Ask me about fees, admissions, schedules, and more!',
            'hi': 'नमस्ते! मैं आपके कैंपस संबंधी प्रश्नों में सहायता के लिए यहाँ हूँ। फीस, प्रवेश, समय सारणी आदि के बारे में पूछें!',
            'mr': 'नमस्कार! मी तुमच्या कॅम्पस संबंधित प्रश्नांमध्ये मदत करण्यासाठी येथे आहे. शुल्क, प्रवेश, वेळापत्रक इत्यादीबद्दल विचारा!',
            'ta': 'வணக்கம்! உங்கள் கல்லூரி தொடர்பான கேள்விகளுக்கு உதவ நான் இங்கே இருக்கிறேன். கட்டணம், சேர்க்கை, அட்டவணை போன்றவற்றைப் பற்றி கேளுங்கள்!',
            'te': 'నమస్కారం! మీ క్యాంపస్ సంబంధిత ప్రశ్నలకు సహాయం చేయడానికి నేను ఇక్కడ ఉన్నాను. ఫీజులు, అడ్మిషన్లు, షెడ్యూల్స్ గురించి అడగండి!'
        };
        
        document.getElementById('welcome-text').textContent = welcomeMessages[language] || welcomeMessages['en'];
        
        // Update input placeholder
        const placeholders = {
            'en': 'Type your question here...',
            'hi': 'यहाँ अपना प्रश्न लिखें...',
            'mr': 'तुमचा प्रश्न येथे लिहा...',
            'ta': 'உங்கள் கேள்வியை இங்கே தட்டச்சு செய்யுங்கள்...',
            'te': 'మీ ప్రశ్నను ఇక్కడ టైప్ చేయండి...'
        };
        
        document.getElementById('message-input').placeholder = placeholders[language] || placeholders['en'];
    }
    
    async loadLanguage(language) {
        // This could load language-specific content, suggestions, etc.
        // For now, we'll just update the UI elements
    }
    
    async escalateToHuman() {
        if (!this.conversationId) {
            this.addMessage('bot', 'Please start a conversation first before requesting human assistance.');
            return;
        }
        
        try {
            const response = await this.callAPI('/chat/escalate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    conversation_id: this.conversationId,
                    reason: 'User requested human assistance'
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.addMessage('bot', data.message);
            } else {
                this.addMessage('bot', 'Sorry, I couldn\'t escalate your request right now. Please try again later.');
            }
        } catch (error) {
            console.error('Escalation Error:', error);
            this.addMessage('bot', 'Sorry, I couldn\'t escalate your request right now. Please try again later.');
        }
    }
    
    handleEscalation() {
        // Add a special message indicating escalation
        this.addMessage('bot', 'I\'ve escalated your query to our support team. They will contact you shortly. Is there anything else I can help you with in the meantime?');
    }
    
    async callAPI(endpoint, options = {}) {
        const url = `${this.config.apiBaseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        return fetch(url, { ...defaultOptions, ...options });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Public methods for external integration
    open() {
        if (!this.isOpen) {
            this.toggleWidget();
        }
    }
    
    close() {
        if (this.isOpen) {
            this.closeWidget();
        }
    }
    
    sendPredefinedMessage(message) {
        if (!this.isOpen) {
            this.open();
        }
        setTimeout(() => {
            this.sendMessage(message);
        }, 300);
    }
    
    setLanguage(language) {
        this.changeLanguage(language);
    }
    
    getConversationHistory() {
        return this.messageHistory;
    }
}

// Auto-initialize widget if script has data attributes
document.addEventListener('DOMContentLoaded', () => {
    const scripts = document.querySelectorAll('script[src*="chatbot-widget.js"]');
    const script = scripts[scripts.length - 1]; // Get the current script
    
    if (script && (script.dataset.autoInit !== 'false')) {
        const config = {
            apiBaseUrl: script.dataset.apiUrl || 'http://localhost:8000/api/v1',
            language: script.dataset.language || 'en',
            theme: script.dataset.theme || 'light'
        };
        
        window.campusAIWidget = new CampusAIChatWidget(config);
    }
});

// Expose class globally for manual initialization
window.CampusAIChatWidget = CampusAIChatWidget;
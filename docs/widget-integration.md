# Widget Integration Guide

## Quick Integration

Add this single line to your website:

```html
<script src="https://cdn.jsdelivr.net/gh/yourusername/campus-ai-assistant@main/chatbot-widget/dist/chatbot-widget.min.js" 
        data-api-url="https://your-api-domain.com/api/v1"
        data-language="en">
</script>
```

## Configuration Options

### Basic Configuration
```html
<script src="widget-url" 
        data-api-url="https://api.yoursite.com/api/v1"
        data-language="hi"
        data-theme="light">
</script>
```

### Advanced Configuration
```html
<script src="widget-url" data-auto-init="false"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    window.campusAIWidget = new CampusAIChatWidget({
        apiBaseUrl: 'https://api.yoursite.com/api/v1',
        language: 'hi',
        theme: 'light',
        position: 'bottom-right',
        welcomeMessage: 'Welcome to XYZ College! How can I help you?'
    });
});
</script>
```

## Platform-Specific Integration

### WordPress
Add to your theme's `footer.php`:

```php
<script src="https://cdn.jsdelivr.net/gh/yourusername/campus-ai-assistant@main/chatbot-widget/dist/chatbot-widget.min.js" 
        data-api-url="<?php echo get_option('campus_ai_api_url', 'https://your-api.com/api/v1'); ?>"
        data-language="<?php echo substr(get_locale(), 0, 2); ?>">
</script>
```

### Drupal
Create a custom block or add to footer template:

```html
<script src="widget-url"
        data-api-url="{{ base_url }}/api/v1"
        data-language="{{ language.id }}">
</script>
```

### Static HTML
```html
<!DOCTYPE html>
<html>
<head>
    <title>Your College Website</title>
</head>
<body>
    <!-- Your content -->
    
    <!-- Campus AI Widget -->
    <script src="https://cdn.jsdelivr.net/gh/yourusername/campus-ai-assistant@main/chatbot-widget/dist/chatbot-widget.min.js" 
            data-api-url="https://your-api.com/api/v1">
    </script>
</body>
</html>
```

### React Application
```jsx
import { useEffect } from 'react';

function App() {
    useEffect(() => {
        const script = document.createElement('script');
        script.src = 'widget-url';
        script.dataset.apiUrl = 'https://your-api.com/api/v1';
        script.dataset.language = 'en';
        document.body.appendChild(script);
        
        return () => document.body.removeChild(script);
    }, []);
    
    return <div>Your App</div>;
}
```

## Customization

### Custom Styling
```css
/* Override widget colors */
#campus-chatbot-widget .widget-button {
    background: linear-gradient(135deg, #your-primary, #your-secondary);
}

#campus-chatbot-widget .chat-header {
    background: linear-gradient(135deg, #your-primary, #your-secondary);
}

/* Custom positioning */
#campus-chatbot-widget {
    bottom: 100px; /* Adjust position */
    right: 30px;
}
```

### Custom Welcome Message
```javascript
window.campusAIWidget = new CampusAIChatWidget({
    welcomeMessage: 'Welcome to ABC University! I can help you with admissions, fees, schedules, and more.',
    language: 'en'
});
```

## API Methods

### Open/Close Widget
```javascript
// Open widget
window.campusAIWidget.open();

// Close widget
window.campusAIWidget.close();
```

### Send Messages
```javascript
// Send predefined message
window.campusAIWidget.sendPredefinedMessage("What are the admission requirements?");
```

### Language Control
```javascript
// Change language
window.campusAIWidget.setLanguage('hi');
```

### Get Conversation Data
```javascript
// Get conversation history
const history = window.campusAIWidget.getConversationHistory();
console.log(history);
```

## Events

### Listen to Widget Events
```javascript
// Message received
document.addEventListener('campusAI:messageReceived', function(event) {
    console.log('Bot response:', event.detail.message);
});

// Conversation started
document.addEventListener('campusAI:conversationStarted', function(event) {
    console.log('Conversation ID:', event.detail.conversationId);
});

// Widget opened/closed
document.addEventListener('campusAI:widgetToggled', function(event) {
    console.log('Widget is now:', event.detail.isOpen ? 'open' : 'closed');
});
```

## Keyboard Shortcuts

- `Alt + C`: Toggle widget
- `Escape`: Close widget (when open)
- `Enter`: Send message

## Mobile Optimization

The widget is automatically optimized for mobile devices:

- Responsive design
- Touch-friendly interface
- Fullscreen on small screens
- Swipe gestures support

## Language Detection

The widget automatically:
- Detects user's browser language
- Responds in the same language as user input
- Allows manual language switching
- Supports RTL languages

## Security Features

- XSS protection via content sanitization
- CORS-compliant API requests
- No sensitive data stored locally
- Encrypted communication (HTTPS)

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
- Mobile browsers

## Troubleshooting

### Widget not appearing
1. Check console for JavaScript errors
2. Verify API URL is correct
3. Check CORS settings on your API
4. Ensure script is loaded after DOM

### Styling conflicts
```css
/* Use higher specificity */
#campus-chatbot-widget .widget-button {
    /* Your styles */
    z-index: 10000 !important;
}
```

### CORS errors
Configure your API to allow your domain:
```python
# FastAPI CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-college-website.edu"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
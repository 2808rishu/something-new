# Campus AI Assistant Widget

A multilingual chatbot widget for college websites.

## Quick Start

Add to your website:

```html
<script src="https://cdn.jsdelivr.net/gh/yourusername/campus-ai-assistant@main/chatbot-widget/dist/chatbot-widget.min.js" 
        data-api-url="https://your-api-domain.com/api/v1"
        data-language="en">
</script>
```

## Features

- 🌍 Multilingual (English, Hindi, Marathi, Tamil, Telugu)
- 📱 Mobile responsive
- 🎨 Customizable
- 🚀 Easy integration

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `apiBaseUrl` | `localhost:8000/api/v1` | Backend API URL |
| `language` | `en` | Default language |
| `theme` | `light` | Widget theme |

## API Methods

```javascript
window.campusAIWidget.open();
window.campusAIWidget.close();
window.campusAIWidget.sendPredefinedMessage("Hello");
window.campusAIWidget.setLanguage('hi');
```

## License

MIT
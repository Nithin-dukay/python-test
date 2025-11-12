# AI Chat Application

A modern, real-time chat application built with Flask, Gunicorn, and OpenRouter API.

## Features

- 🤖 **AI-Powered Conversations**: Powered by OpenRouter's GPT-3.5-turbo model
- 💬 **Real-time Streaming**: Server-Sent Events (SSE) for streaming AI responses
- 🎨 **Modern UI**: Beautiful, responsive interface built with Tailwind CSS
- 📝 **Chat History**: Maintains conversation context across messages
- ⚡ **Production-Ready**: Deployed with Gunicorn for high performance
- 🛡️ **Error Handling**: Robust validation and error handling

## Architecture

### Backend (Flask)
- **Framework**: Flask 3.1.2
- **Server**: Gunicorn 23.0.0 with multiple workers
- **API Integration**: OpenAI Python client configured for OpenRouter
- **Streaming**: Server-Sent Events (SSE) for real-time response streaming

### Frontend
- **Styling**: Tailwind CSS via CDN
- **JavaScript**: Vanilla JS with Fetch API and EventSource for SSE
- **Design**: Clean, modern chat interface with message bubbles

## File Structure

```
/vercel/sandbox/
├── app.py                  # Flask application with API endpoints
├── gunicorn_config.py      # Gunicorn server configuration
├── index.html              # Chat interface frontend
├── requirements.txt        # Python dependencies
└── README_CHAT_APP.md      # This file
```

## Installation

1. **Install Dependencies**:
```bash
python3 -m pip install -r requirements.txt
```

2. **Set Environment Variable**:
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

## Running the Application

### Development Mode (Flask)
```bash
python3 app.py
```

### Production Mode (Gunicorn)
```bash
python3 -m gunicorn -c gunicorn_config.py app:app
```

The application will be available at: **http://localhost:5000**

## API Endpoints

### `GET /`
Serves the chat interface HTML page.

### `GET /health`
Health check endpoint.
- **Response**: `{"status": "healthy", "message": "Chat app is running!"}`

### `POST /api/chat`
Handles chat requests with streaming responses.

**Request Body**:
```json
{
  "message": "Your message here",
  "history": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ]
}
```

**Response**: Server-Sent Events stream
```
data: {"content": "Hello"}
data: {"content": " there"}
data: {"done": true}
```

**Error Responses**:
- `400`: Missing or empty message
- `500`: Server error

## Testing

### API Testing (curl)
```bash
# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is 2+2?"}' \
  -N

# Test health endpoint
curl http://localhost:5000/health

# Test error handling (empty message)
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":""}'
```

### Browser Testing
1. Navigate to http://localhost:5000
2. Type a message in the input field
3. Click "Send" or press Enter
4. Watch the AI response stream in real-time

## Configuration

### Gunicorn Settings (gunicorn_config.py)
- **Workers**: `CPU cores * 2 + 1`
- **Timeout**: 120 seconds (for streaming)
- **Bind**: `0.0.0.0:5000`
- **Worker Class**: sync

### OpenRouter Settings (app.py)
- **Model**: `openai/gpt-3.5-turbo`
- **Temperature**: 0.7
- **Max Tokens**: 1000
- **Streaming**: Enabled

## Features in Detail

### Real-time Streaming
The application uses Server-Sent Events (SSE) to stream AI responses token-by-token, providing a smooth, real-time chat experience.

### Chat History
Conversation context is maintained client-side and sent with each request, allowing the AI to understand follow-up questions and maintain coherent conversations.

### Error Handling
- Client-side validation prevents empty messages
- Server-side validation with appropriate HTTP status codes
- User-friendly error messages displayed in the UI

### Responsive Design
The interface adapts to different screen sizes with:
- Flexible message bubbles (max 80% width)
- Scrollable chat container
- Mobile-friendly input controls

## Environment Variables

- `OPENROUTER_API_KEY`: Required. Your OpenRouter API key for authentication.

## Dependencies

### Python Packages
- `flask>=2.0.0` - Web framework
- `gunicorn>=21.2.0` - WSGI HTTP server
- `openai>=1.0.0` - OpenAI/OpenRouter API client
- `requests>=2.25.0` - HTTP library

### Frontend Libraries
- Tailwind CSS 3.x (CDN)
- Google Fonts (Inter)

## Production Deployment

For production deployment:

1. Use environment variables for sensitive data
2. Enable HTTPS/SSL
3. Configure proper CORS if needed
4. Set up monitoring and logging
5. Use a reverse proxy (nginx/Apache)
6. Consider rate limiting

## Troubleshooting

### Server won't start
- Check if port 5000 is available
- Verify Python 3.9+ is installed
- Ensure all dependencies are installed

### API errors
- Verify OPENROUTER_API_KEY is set correctly
- Check network connectivity
- Review server logs for detailed error messages

### Streaming not working
- Ensure browser supports EventSource API
- Check for proxy/firewall blocking SSE
- Verify Content-Type headers are correct

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions, please refer to:
- OpenRouter Documentation: https://openrouter.ai/docs
- Flask Documentation: https://flask.palletsprojects.com/
- Gunicorn Documentation: https://docs.gunicorn.org/

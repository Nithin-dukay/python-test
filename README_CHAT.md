# AI Chat Application

A modern, real-time chat application built with Flask, Gunicorn, and OpenRouter API integration.

## Features

- 🚀 **Real-time Streaming**: Messages stream in real-time using Server-Sent Events (SSE)
- 🤖 **Multiple AI Models**: Choose from 5 different AI models including:
  - Llama 3.2 3B (Free)
  - Gemini Flash 1.5
  - Claude 3.5 Sonnet
  - GPT-4o Mini
  - Mistral 7B (Free)
- 💬 **Modern UI**: Clean, responsive chat interface built with Tailwind CSS
- ⚡ **Production Ready**: Powered by Gunicorn WSGI server
- 🔄 **Conversation History**: Maintains chat context throughout the conversation

## Tech Stack

- **Backend**: Flask (Python)
- **WSGI Server**: Gunicorn
- **AI API**: OpenRouter
- **Frontend**: HTML, JavaScript, Tailwind CSS
- **Streaming**: Server-Sent Events (SSE)

## Prerequisites

- Python 3.9+
- OpenRouter API Key

## Installation

1. **Install dependencies**:
```bash
python3 -m pip install -r requirements.txt
```

2. **Set up environment variables**:
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
OPENROUTER_API_KEY=your-api-key-here
```

## Running the Application

### Development Mode (Flask)
```bash
python3 app.py
```
Access at: http://localhost:5000

### Production Mode (Gunicorn)
```bash
gunicorn -c gunicorn_config.py app:app
```
Access at: http://localhost:8000

## API Endpoints

### GET `/`
Serves the chat interface

### GET `/health`
Health check endpoint
```json
{
  "status": "healthy",
  "message": "Chat app is running!"
}
```

### GET `/api/models`
Returns available AI models
```json
{
  "models": [
    {
      "id": "meta-llama/llama-3.2-3b-instruct:free",
      "name": "Llama 3.2 3B (Free)"
    },
    ...
  ]
}
```

### POST `/api/chat`
Send chat messages and receive AI responses

**Request Body**:
```json
{
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "model": "meta-llama/llama-3.2-3b-instruct:free",
  "stream": true
}
```

**Response** (Streaming):
```
data: {"content": "Hello"}
data: {"content": "!"}
data: {"done": true}
```

## Configuration

### Gunicorn Configuration (`gunicorn_config.py`)

- **Workers**: `(CPU cores * 2) + 1`
- **Bind**: `0.0.0.0:8000`
- **Timeout**: 120 seconds
- **Worker Class**: sync

Modify `gunicorn_config.py` to adjust these settings.

## Project Structure

```
.
├── app.py                  # Flask application with API endpoints
├── gunicorn_config.py      # Gunicorn server configuration
├── index.html              # Chat interface frontend
├── requirements.txt        # Python dependencies
└── README_CHAT.md         # This file
```

## Usage

1. Open the application in your browser
2. Select an AI model from the dropdown (top right)
3. Type your message in the input field
4. Press Enter or click "Send"
5. Watch the AI response stream in real-time

## Features in Detail

### Real-time Streaming
Messages are streamed token-by-token using Server-Sent Events, providing a smooth, ChatGPT-like experience.

### Model Selection
Switch between different AI models on-the-fly. Each model has different capabilities and pricing:
- **Free models**: Llama 3.2 3B, Mistral 7B
- **Premium models**: GPT-4o Mini, Claude 3.5 Sonnet, Gemini Flash 1.5

### Conversation Context
The application maintains conversation history, allowing for contextual follow-up questions.

## Testing

### Test Health Endpoint
```bash
curl http://localhost:8000/health
```

### Test Models Endpoint
```bash
curl http://localhost:8000/api/models
```

### Test Chat (Non-streaming)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "model": "meta-llama/llama-3.2-3b-instruct:free",
    "stream": false
  }'
```

### Test Chat (Streaming)
```bash
curl -N -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Count to 5"}],
    "model": "meta-llama/llama-3.2-3b-instruct:free",
    "stream": true
  }'
```

## Troubleshooting

### Rate Limiting
Free models may be rate-limited. If you encounter rate limit errors:
1. Wait a few moments and retry
2. Switch to a different model
3. Add your own API key at https://openrouter.ai/settings/integrations

### Connection Issues
- Ensure the OPENROUTER_API_KEY environment variable is set
- Check your internet connection
- Verify the Gunicorn server is running

### Port Already in Use
If port 8000 is already in use, modify the `bind` setting in `gunicorn_config.py`:
```python
bind = "0.0.0.0:8080"  # Use a different port
```

## License

MIT License

## Credits

- Built with [Flask](https://flask.palletsprojects.com/)
- Powered by [OpenRouter](https://openrouter.ai/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Served by [Gunicorn](https://gunicorn.org/)

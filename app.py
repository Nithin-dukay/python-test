from flask import Flask, request, Response, send_from_directory, jsonify, stream_with_context
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client with OpenRouter configuration
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Available models on OpenRouter
AVAILABLE_MODELS = [
    {"id": "meta-llama/llama-3.2-3b-instruct:free", "name": "Llama 3.2 3B (Free)"},
    {"id": "google/gemini-flash-1.5", "name": "Gemini Flash 1.5"},
    {"id": "anthropic/claude-3.5-sonnet", "name": "Claude 3.5 Sonnet"},
    {"id": "openai/gpt-4o-mini", "name": "GPT-4o Mini"},
    {"id": "mistralai/mistral-7b-instruct:free", "name": "Mistral 7B (Free)"},
]

@app.route('/')
def index():
    """Serve the chat interface"""
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'Chat app is running!'}

@app.route('/api/models', methods=['GET'])
def get_models():
    """Return available models"""
    return jsonify({"models": AVAILABLE_MODELS})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests with streaming support"""
    try:
        data = request.json
        messages = data.get('messages', [])
        model = data.get('model', 'meta-llama/llama-3.2-3b-instruct:free')
        stream = data.get('stream', True)
        
        if not messages:
            return jsonify({"error": "No messages provided"}), 400
        
        if not stream:
            # Non-streaming response
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return jsonify({
                "message": response.choices[0].message.content,
                "model": model
            })
        
        # Streaming response using Server-Sent Events
        def generate():
            try:
                stream_response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True,
                )
                
                for chunk in stream_response:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        yield f"data: {json.dumps({'content': content})}\n\n"
                
                yield f"data: {json.dumps({'done': True})}\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

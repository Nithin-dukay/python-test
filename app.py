from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
import os
import json
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client with OpenRouter configuration
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

@app.route('/')
def index():
    """Serve the chat interface"""
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'Chat app is running!'}

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests with streaming support"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get chat history from request (optional)
        history = data.get('history', [])
        
        # Build messages array
        messages = []
        
        # Add system message
        messages.append({
            "role": "system",
            "content": "You are a helpful AI assistant. Provide clear, concise, and friendly responses."
        })
        
        # Add history
        for msg in history:
            messages.append(msg)
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        def generate():
            """Generator function for streaming responses"""
            try:
                # Create streaming completion
                stream = client.chat.completions.create(
                    model="openai/gpt-3.5-turbo",
                    messages=messages,
                    stream=True,
                    temperature=0.7,
                    max_tokens=1000
                )
                
                # Stream the response
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        # Send as Server-Sent Events format
                        yield f"data: {json.dumps({'content': content})}\n\n"
                
                # Send completion signal
                yield f"data: {json.dumps({'done': True})}\n\n"
                
            except Exception as e:
                error_msg = str(e)
                yield f"data: {json.dumps({'error': error_msg})}\n\n"
        
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

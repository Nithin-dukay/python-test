from flask import Flask, render_template, send_from_directory, request, Response, stream_with_context, jsonify
from flask_cors import CORS
import os
import json
import requests

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'Chat server is running!'}

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        if not OPENROUTER_API_KEY:
            return jsonify({'error': 'OpenRouter API key not configured'}), 500
        
        messages = data.get('messages', [])
        messages.append({
            'role': 'user',
            'content': user_message
        })
        
        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost:8000',
            'X-Title': 'Flask Chat App'
        }
        
        payload = {
            'model': 'openai/gpt-3.5-turbo',
            'messages': messages,
            'stream': True
        }
        
        def generate():
            try:
                response = requests.post(
                    OPENROUTER_API_URL,
                    headers=headers,
                    json=payload,
                    stream=True,
                    timeout=60
                )
                
                if response.status_code != 200:
                    error_msg = f"OpenRouter API error: {response.status_code}"
                    try:
                        error_data = response.json()
                        error_msg = error_data.get('error', {}).get('message', error_msg)
                    except:
                        pass
                    yield f"data: {json.dumps({'error': error_msg})}\n\n"
                    return
                
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            data_str = line_str[6:]
                            if data_str.strip() == '[DONE]':
                                yield f"data: {json.dumps({'done': True})}\n\n"
                                break
                            
                            try:
                                chunk_data = json.loads(data_str)
                                if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                                    delta = chunk_data['choices'][0].get('delta', {})
                                    content = delta.get('content', '')
                                    if content:
                                        yield f"data: {json.dumps({'content': content})}\n\n"
                            except json.JSONDecodeError:
                                continue
                
            except requests.exceptions.Timeout:
                yield f"data: {json.dumps({'error': 'Request timeout'})}\n\n"
            except requests.exceptions.RequestException as e:
                yield f"data: {json.dumps({'error': f'Network error: {str(e)}'})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': f'Unexpected error: {str(e)}'})}\n\n"
        
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Connection': 'keep-alive'
            }
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    """Serve the hello world page"""
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'Hello World server is running!'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

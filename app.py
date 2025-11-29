from flask import Flask, render_template, send_from_directory
import os
import logging

# Import logger if available
try:
    from logger import get_logger
    logger = get_logger(name='flask_app', log_dir='logs', log_level=logging.INFO)
except ImportError:
    # Fallback to basic logging if logger module not available
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('flask_app')

app = Flask(__name__)

@app.route('/')
def hello_world():
    """Serve the hello world page"""
    logger.info("Serving hello world page")
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return {'status': 'healthy', 'message': 'Hello World server is running!'}

@app.before_request
def log_request():
    """Log incoming requests"""
    from flask import request
    logger.info(f"Request: {request.method} {request.path}")

@app.after_request
def log_response(response):
    """Log outgoing responses"""
    logger.info(f"Response: {response.status_code}")
    return response

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)

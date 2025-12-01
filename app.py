from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# In-memory storage for todos
todos = []

@app.route('/')
def index():
    """Serve the todo list page"""
    return send_from_directory('.', 'todo.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'Todo List server is running!'}

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    return jsonify(todos), 200

@app.route('/api/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    todo = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/api/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update an existing todo"""
    data = request.get_json()
    
    for todo in todos:
        if todo['id'] == todo_id:
            if 'title' in data:
                todo['title'] = data['title']
            if 'description' in data:
                todo['description'] = data['description']
            if 'completed' in data:
                todo['completed'] = data['completed']
            return jsonify(todo), 200
    
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/api/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    global todos
    
    for i, todo in enumerate(todos):
        if todo['id'] == todo_id:
            deleted_todo = todos.pop(i)
            return jsonify(deleted_todo), 200
    
    return jsonify({'error': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

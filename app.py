from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

NOTES_FILE = 'notes.json'

def load_notes():
    """Load notes from JSON file"""
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_notes(notes):
    """Save notes to JSON file"""
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=2)

@app.route('/')
def index():
    """Serve the note-taking app page"""
    return send_from_directory('.', 'index.html')

@app.route('/api/notes', methods=['GET'])
def get_notes():
    """Get all notes"""
    notes = load_notes()
    return jsonify(notes)

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400
    
    notes = load_notes()
    
    # Generate new ID
    new_id = max([note['id'] for note in notes], default=0) + 1
    
    new_note = {
        'id': new_id,
        'title': data['title'],
        'content': data['content'],
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    notes.append(new_note)
    save_notes(notes)
    
    return jsonify(new_note), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update an existing note"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    notes = load_notes()
    
    for note in notes:
        if note['id'] == note_id:
            if 'title' in data:
                note['title'] = data['title']
            if 'content' in data:
                note['content'] = data['content']
            note['updated_at'] = datetime.now().isoformat()
            
            save_notes(notes)
            return jsonify(note)
    
    return jsonify({'error': 'Note not found'}), 404

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note"""
    notes = load_notes()
    
    for i, note in enumerate(notes):
        if note['id'] == note_id:
            deleted_note = notes.pop(i)
            save_notes(notes)
            return jsonify({'message': 'Note deleted', 'note': deleted_note})
    
    return jsonify({'error': 'Note not found'}), 404

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'Note-taking app is running!'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

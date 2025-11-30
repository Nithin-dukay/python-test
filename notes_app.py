"""
Flask Web Application for Notes Management
Provides REST API endpoints and web interface
"""

from flask import Flask, render_template, request, jsonify, send_file
from database import NotesDatabase
from utils import NotesUtils
import os
import tempfile

app = Flask(__name__)
db = NotesDatabase()
utils = NotesUtils(db)


@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')


@app.route('/api/notes', methods=['GET'])
def get_notes():
    """Get all notes or search/filter notes"""
    search_query = request.args.get('search', '')
    category = request.args.get('category', '')
    tag = request.args.get('tag', '')
    
    try:
        if search_query:
            notes = db.search_notes(search_query)
        elif category:
            notes = db.get_notes_by_category(category)
        elif tag:
            notes = db.get_notes_by_tag(tag)
        else:
            notes = db.get_all_notes()
        
        return jsonify({
            'success': True,
            'notes': notes
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a single note by ID"""
    try:
        note = db.get_note(note_id)
        
        if note:
            return jsonify({
                'success': True,
                'note': note
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Note not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.get_json()
        
        title = data.get('title', 'Untitled Note')
        content = data.get('content', '')
        tags = data.get('tags', [])
        category = data.get('category', '')
        
        note_id = db.create_note(title, content, tags, category)
        note = db.get_note(note_id)
        
        return jsonify({
            'success': True,
            'note': note
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update an existing note"""
    try:
        data = request.get_json()
        
        title = data.get('title')
        content = data.get('content')
        tags = data.get('tags')
        category = data.get('category')
        
        success = db.update_note(note_id, title, content, tags, category)
        
        if success:
            note = db.get_note(note_id)
            return jsonify({
                'success': True,
                'note': note
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Note not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note"""
    try:
        success = db.delete_note(note_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Note deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Note not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    try:
        categories = db.get_all_categories()
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tags', methods=['GET'])
def get_tags():
    """Get all unique tags"""
    try:
        tags = db.get_all_tags()
        return jsonify({
            'success': True,
            'tags': tags
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get statistics about notes"""
    try:
        stats = utils.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export/note/<int:note_id>/<format>', methods=['GET'])
def export_note(note_id, format):
    """Export a single note to txt or markdown"""
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            if format == 'txt':
                file_path = utils.export_note_to_txt(note_id, 
                    os.path.join(tmpdir, 'note.txt'))
            elif format == 'md':
                file_path = utils.export_note_to_markdown(note_id, 
                    os.path.join(tmpdir, 'note.md'))
            else:
                return jsonify({
                    'success': False,
                    'error': 'Invalid format. Use txt or md'
                }), 400
            
            return send_file(file_path, as_attachment=True)
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export/all/<format>', methods=['GET'])
def export_all_notes(format):
    """Export all notes to specified format"""
    try:
        if format == 'json':
            file_path = utils.export_all_notes_to_json('notes_export.json')
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid format. Use json'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/backup', methods=['POST'])
def create_backup():
    """Create a backup of the database"""
    try:
        backup_path = utils.backup_database()
        return jsonify({
            'success': True,
            'message': 'Backup created successfully',
            'backup_path': backup_path
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/import', methods=['POST'])
def import_notes():
    """Import notes from JSON file"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.json') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            imported_count = utils.import_notes_from_json(tmp_path)
            return jsonify({
                'success': True,
                'message': f'Successfully imported {imported_count} notes'
            })
        finally:
            os.unlink(tmp_path)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Notes Application Starting...")
    print("=" * 60)
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

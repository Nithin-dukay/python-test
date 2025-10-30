import sqlite3
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'notes.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS note_tags (
                note_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (note_id) REFERENCES notes (id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE,
                PRIMARY KEY (note_id, tag_id)
            )
        ''')
        
        conn.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
                title, content, content=notes, content_rowid=id
            )
        ''')
        
        conn.execute('''
            CREATE TRIGGER IF NOT EXISTS notes_ai AFTER INSERT ON notes BEGIN
                INSERT INTO notes_fts(rowid, title, content) VALUES (new.id, new.title, new.content);
            END
        ''')
        
        conn.execute('''
            CREATE TRIGGER IF NOT EXISTS notes_ad AFTER DELETE ON notes BEGIN
                DELETE FROM notes_fts WHERE rowid = old.id;
            END
        ''')
        
        conn.execute('''
            CREATE TRIGGER IF NOT EXISTS notes_au AFTER UPDATE ON notes BEGIN
                UPDATE notes_fts SET title = new.title, content = new.content WHERE rowid = new.id;
            END
        ''')
        
        conn.commit()

@app.route('/')
def index():
    with open('templates/notes.html', 'r') as f:
        return render_template_string(f.read())

@app.route('/api/notes', methods=['GET'])
def get_notes():
    tag = request.args.get('tag')
    search = request.args.get('search')
    
    with get_db() as conn:
        if search:
            query = '''
                SELECT DISTINCT n.id, n.title, n.content, n.created_at, n.updated_at
                FROM notes n
                JOIN notes_fts ON notes_fts.rowid = n.id
                WHERE notes_fts MATCH ?
                ORDER BY n.updated_at DESC
            '''
            cursor = conn.execute(query, (search,))
        elif tag:
            query = '''
                SELECT DISTINCT n.id, n.title, n.content, n.created_at, n.updated_at
                FROM notes n
                JOIN note_tags nt ON n.id = nt.note_id
                JOIN tags t ON nt.tag_id = t.id
                WHERE t.name = ?
                ORDER BY n.updated_at DESC
            '''
            cursor = conn.execute(query, (tag,))
        else:
            cursor = conn.execute('SELECT * FROM notes ORDER BY updated_at DESC')
        
        notes = []
        for row in cursor.fetchall():
            note = dict(row)
            tags_cursor = conn.execute('''
                SELECT t.name FROM tags t
                JOIN note_tags nt ON t.id = nt.tag_id
                WHERE nt.note_id = ?
            ''', (note['id'],))
            note['tags'] = [tag['name'] for tag in tags_cursor.fetchall()]
            notes.append(note)
        
        return jsonify(notes)

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    with get_db() as conn:
        cursor = conn.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
        row = cursor.fetchone()
        
        if row is None:
            return jsonify({'error': 'Note not found'}), 404
        
        note = dict(row)
        tags_cursor = conn.execute('''
            SELECT t.name FROM tags t
            JOIN note_tags nt ON t.id = nt.tag_id
            WHERE nt.note_id = ?
        ''', (note_id,))
        note['tags'] = [tag['name'] for tag in tags_cursor.fetchall()]
        
        return jsonify(note)

@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.json
    title = data.get('title', 'Untitled')
    content = data.get('content', '')
    tags = data.get('tags', [])
    
    with get_db() as conn:
        cursor = conn.execute(
            'INSERT INTO notes (title, content) VALUES (?, ?)',
            (title, content)
        )
        note_id = cursor.lastrowid
        
        for tag_name in tags:
            tag_name = tag_name.strip()
            if tag_name:
                conn.execute('INSERT OR IGNORE INTO tags (name) VALUES (?)', (tag_name,))
                tag_cursor = conn.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
                tag_id = tag_cursor.fetchone()['id']
                conn.execute('INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)', (note_id, tag_id))
        
        conn.commit()
        
        return jsonify({'id': note_id, 'title': title, 'content': content, 'tags': tags}), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.json
    title = data.get('title', 'Untitled')
    content = data.get('content', '')
    tags = data.get('tags', [])
    
    with get_db() as conn:
        conn.execute(
            'UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (title, content, note_id)
        )
        
        conn.execute('DELETE FROM note_tags WHERE note_id = ?', (note_id,))
        
        for tag_name in tags:
            tag_name = tag_name.strip()
            if tag_name:
                conn.execute('INSERT OR IGNORE INTO tags (name) VALUES (?)', (tag_name,))
                tag_cursor = conn.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
                tag_id = tag_cursor.fetchone()['id']
                conn.execute('INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)', (note_id, tag_id))
        
        conn.commit()
        
        return jsonify({'id': note_id, 'title': title, 'content': content, 'tags': tags})

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    with get_db() as conn:
        conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        
        return jsonify({'message': 'Note deleted'}), 200

@app.route('/api/tags', methods=['GET'])
def get_tags():
    with get_db() as conn:
        cursor = conn.execute('''
            SELECT t.name, COUNT(nt.note_id) as count
            FROM tags t
            LEFT JOIN note_tags nt ON t.id = nt.tag_id
            GROUP BY t.id, t.name
            ORDER BY t.name
        ''')
        tags = [{'name': row['name'], 'count': row['count']} for row in cursor.fetchall()]
        
        return jsonify(tags)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
Database module for Notes Application
Handles SQLite database operations including CRUD for notes
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional


class NotesDatabase:
    """Manages SQLite database operations for notes"""
    
    def __init__(self, db_path: str = "notes.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Create notes table if it doesn't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_note(self, title: str, content: str, tags: List[str] = None, 
                    category: str = "") -> int:
        """Create a new note and return its ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        tags_json = json.dumps(tags if tags else [])
        
        cursor.execute("""
            INSERT INTO notes (title, content, tags, category, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, content, tags_json, category, datetime.now(), datetime.now()))
        
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return note_id
    
    def get_note(self, note_id: int) -> Optional[Dict]:
        """Get a single note by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def get_all_notes(self) -> List[Dict]:
        """Get all notes ordered by updated_at descending"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM notes ORDER BY updated_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def update_note(self, note_id: int, title: str = None, content: str = None,
                    tags: List[str] = None, category: str = None) -> bool:
        """Update an existing note"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get current note
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        current = cursor.fetchone()
        
        if not current:
            conn.close()
            return False
        
        # Update only provided fields
        new_title = title if title is not None else current['title']
        new_content = content if content is not None else current['content']
        new_tags = json.dumps(tags) if tags is not None else current['tags']
        new_category = category if category is not None else current['category']
        
        cursor.execute("""
            UPDATE notes 
            SET title = ?, content = ?, tags = ?, category = ?, updated_at = ?
            WHERE id = ?
        """, (new_title, new_content, new_tags, new_category, datetime.now(), note_id))
        
        conn.commit()
        conn.close()
        
        return True
    
    def delete_note(self, note_id: int) -> bool:
        """Delete a note by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def search_notes(self, query: str) -> List[Dict]:
        """Search notes by title or content"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT * FROM notes 
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY updated_at DESC
        """, (search_pattern, search_pattern))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_notes_by_category(self, category: str) -> List[Dict]:
        """Get all notes in a specific category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM notes 
            WHERE category = ?
            ORDER BY updated_at DESC
        """, (category,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_notes_by_tag(self, tag: str) -> List[Dict]:
        """Get all notes with a specific tag"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM notes ORDER BY updated_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        # Filter notes that contain the tag
        filtered_notes = []
        for row in rows:
            note = self._row_to_dict(row)
            if tag in note['tags']:
                filtered_notes.append(note)
        
        return filtered_notes
    
    def get_all_categories(self) -> List[str]:
        """Get list of all unique categories"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT category FROM notes WHERE category != ''")
        rows = cursor.fetchall()
        conn.close()
        
        return [row['category'] for row in rows]
    
    def get_all_tags(self) -> List[str]:
        """Get list of all unique tags"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT tags FROM notes")
        rows = cursor.fetchall()
        conn.close()
        
        all_tags = set()
        for row in rows:
            tags = json.loads(row['tags'])
            all_tags.update(tags)
        
        return sorted(list(all_tags))
    
    def _row_to_dict(self, row) -> Dict:
        """Convert SQLite row to dictionary"""
        return {
            'id': row['id'],
            'title': row['title'],
            'content': row['content'],
            'tags': json.loads(row['tags']),
            'category': row['category'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at']
        }

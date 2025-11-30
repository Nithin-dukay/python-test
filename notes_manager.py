#!/usr/bin/env python3
"""
Notes Manager Module
Provides core functionality for creating, managing, and persisting notes.
"""

import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional


class Note:
    """
    Represents a single note with title, content, and metadata.
    """
    
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None, 
                 note_id: Optional[str] = None, created_at: Optional[str] = None,
                 updated_at: Optional[str] = None):
        """
        Initialize a new note.
        
        Args:
            title: The title of the note
            content: The main content of the note
            tags: Optional list of tags for categorization
            note_id: Optional UUID (generated if not provided)
            created_at: Optional creation timestamp (generated if not provided)
            updated_at: Optional update timestamp (generated if not provided)
        """
        self.id = note_id or str(uuid.uuid4())
        self.title = title
        self.content = content
        self.tags = tags or []
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
    
    def update(self, title: Optional[str] = None, content: Optional[str] = None, 
               tags: Optional[List[str]] = None):
        """
        Update note fields and refresh the updated_at timestamp.
        
        Args:
            title: New title (if provided)
            content: New content (if provided)
            tags: New tags list (if provided)
        """
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        if tags is not None:
            self.tags = tags
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """
        Convert note to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the note
        """
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Note':
        """
        Create a Note instance from a dictionary.
        
        Args:
            data: Dictionary containing note data
            
        Returns:
            Note instance
        """
        return cls(
            title=data['title'],
            content=data['content'],
            tags=data.get('tags', []),
            note_id=data['id'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
    
    def __str__(self) -> str:
        """String representation of the note."""
        return f"Note(id={self.id[:8]}..., title='{self.title}')"
    
    def __repr__(self) -> str:
        """Detailed string representation of the note."""
        return self.__str__()


class NotesManager:
    """
    Manages a collection of notes with persistence to JSON file.
    """
    
    def __init__(self, data_dir: str = "notes_data", filename: str = "notes.json"):
        """
        Initialize the notes manager.
        
        Args:
            data_dir: Directory to store notes data
            filename: Name of the JSON file for persistence
        """
        self.data_dir = data_dir
        self.filename = filename
        self.filepath = os.path.join(data_dir, filename)
        self.notes: Dict[str, Note] = {}
        
        self._ensure_data_directory()
        self.load_notes()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist."""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
        except OSError as e:
            raise IOError(f"Failed to create data directory: {e}")
    
    def load_notes(self):
        """
        Load notes from JSON file.
        
        Raises:
            IOError: If file cannot be read
            json.JSONDecodeError: If file contains invalid JSON
        """
        if not os.path.exists(self.filepath):
            self.notes = {}
            return
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.notes = {
                    note_id: Note.from_dict(note_data)
                    for note_id, note_data in data.items()
                }
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Corrupted notes file: {e.msg}", e.doc, e.pos
            )
        except IOError as e:
            raise IOError(f"Failed to load notes: {e}")
    
    def save_notes(self):
        """
        Save all notes to JSON file.
        
        Raises:
            IOError: If file cannot be written
        """
        try:
            data = {
                note_id: note.to_dict()
                for note_id, note in self.notes.items()
            }
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Failed to save notes: {e}")
    
    def create_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> Note:
        """
        Create a new note and save it.
        
        Args:
            title: Note title
            content: Note content
            tags: Optional list of tags
            
        Returns:
            The created Note instance
            
        Raises:
            ValueError: If title or content is empty
        """
        if not title or not title.strip():
            raise ValueError("Note title cannot be empty")
        if not content or not content.strip():
            raise ValueError("Note content cannot be empty")
        
        note = Note(title.strip(), content.strip(), tags)
        self.notes[note.id] = note
        self.save_notes()
        return note
    
    def get_note(self, note_id: str) -> Optional[Note]:
        """
        Retrieve a note by ID.
        
        Args:
            note_id: The unique identifier of the note
            
        Returns:
            Note instance if found, None otherwise
        """
        return self.notes.get(note_id)
    
    def get_all_notes(self, sort_by: str = 'created_at', reverse: bool = True) -> List[Note]:
        """
        Get all notes, optionally sorted.
        
        Args:
            sort_by: Field to sort by ('created_at', 'updated_at', 'title')
            reverse: Sort in descending order if True
            
        Returns:
            List of Note instances
        """
        notes_list = list(self.notes.values())
        
        if sort_by == 'title':
            notes_list.sort(key=lambda n: n.title.lower(), reverse=reverse)
        elif sort_by == 'updated_at':
            notes_list.sort(key=lambda n: n.updated_at, reverse=reverse)
        else:  # default to created_at
            notes_list.sort(key=lambda n: n.created_at, reverse=reverse)
        
        return notes_list
    
    def update_note(self, note_id: str, title: Optional[str] = None, 
                   content: Optional[str] = None, tags: Optional[List[str]] = None) -> bool:
        """
        Update an existing note.
        
        Args:
            note_id: The unique identifier of the note
            title: New title (if provided)
            content: New content (if provided)
            tags: New tags (if provided)
            
        Returns:
            True if note was updated, False if note not found
            
        Raises:
            ValueError: If trying to set empty title or content
        """
        note = self.get_note(note_id)
        if not note:
            return False
        
        if title is not None and not title.strip():
            raise ValueError("Note title cannot be empty")
        if content is not None and not content.strip():
            raise ValueError("Note content cannot be empty")
        
        note.update(
            title=title.strip() if title else None,
            content=content.strip() if content else None,
            tags=tags
        )
        self.save_notes()
        return True
    
    def delete_note(self, note_id: str) -> bool:
        """
        Delete a note by ID.
        
        Args:
            note_id: The unique identifier of the note
            
        Returns:
            True if note was deleted, False if note not found
        """
        if note_id in self.notes:
            del self.notes[note_id]
            self.save_notes()
            return True
        return False
    
    def search_notes(self, query: str, search_in: str = 'both') -> List[Note]:
        """
        Search notes by title and/or content.
        
        Args:
            query: Search query string
            search_in: Where to search ('title', 'content', 'both', 'tags')
            
        Returns:
            List of matching Note instances
        """
        query_lower = query.lower()
        results = []
        
        for note in self.notes.values():
            match = False
            
            if search_in in ('title', 'both'):
                if query_lower in note.title.lower():
                    match = True
            
            if search_in in ('content', 'both'):
                if query_lower in note.content.lower():
                    match = True
            
            if search_in == 'tags':
                if any(query_lower in tag.lower() for tag in note.tags):
                    match = True
            
            if match:
                results.append(note)
        
        return results
    
    def filter_by_tags(self, tags: List[str]) -> List[Note]:
        """
        Filter notes by tags.
        
        Args:
            tags: List of tags to filter by
            
        Returns:
            List of Note instances that have any of the specified tags
        """
        tags_lower = [tag.lower() for tag in tags]
        results = []
        
        for note in self.notes.values():
            note_tags_lower = [tag.lower() for tag in note.tags]
            if any(tag in note_tags_lower for tag in tags_lower):
                results.append(note)
        
        return results
    
    def export_note(self, note_id: str, export_dir: str = "exported_notes") -> Optional[str]:
        """
        Export a note to a text file.
        
        Args:
            note_id: The unique identifier of the note
            export_dir: Directory to export the note to
            
        Returns:
            Path to the exported file if successful, None if note not found
            
        Raises:
            IOError: If file cannot be written
        """
        note = self.get_note(note_id)
        if not note:
            return None
        
        try:
            os.makedirs(export_dir, exist_ok=True)
            
            # Create safe filename from title
            safe_title = "".join(c for c in note.title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title[:50]  # Limit filename length
            filename = f"{safe_title}_{note.id[:8]}.txt"
            filepath = os.path.join(export_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Title: {note.title}\n")
                f.write(f"Created: {note.created_at}\n")
                f.write(f"Updated: {note.updated_at}\n")
                if note.tags:
                    f.write(f"Tags: {', '.join(note.tags)}\n")
                f.write("\n" + "=" * 60 + "\n\n")
                f.write(note.content)
            
            return filepath
        except IOError as e:
            raise IOError(f"Failed to export note: {e}")
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the notes collection.
        
        Returns:
            Dictionary containing statistics
        """
        total_notes = len(self.notes)
        all_tags = set()
        total_chars = 0
        
        for note in self.notes.values():
            all_tags.update(note.tags)
            total_chars += len(note.content)
        
        return {
            'total_notes': total_notes,
            'total_tags': len(all_tags),
            'unique_tags': sorted(list(all_tags)),
            'total_characters': total_chars,
            'average_note_length': total_chars // total_notes if total_notes > 0 else 0
        }

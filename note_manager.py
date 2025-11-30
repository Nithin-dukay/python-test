"""
Note Manager
Handles CRUD operations, file I/O, search, and export functionality for notes.
"""

import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from note import Note


class NoteManager:
    """
    Manages a collection of notes with persistence to JSON file.
    """
    
    def __init__(self, data_file: str = "notes_data.json"):
        """
        Initialize the note manager.
        
        Args:
            data_file: Path to the JSON file for storing notes
        """
        self.data_file = data_file
        self.notes: Dict[str, Note] = {}
        self.load_notes()
    
    def create_note(self, title: str = "Untitled", content: str = "", tags: List[str] = None) -> Note:
        """
        Create a new note and add it to the collection.
        
        Args:
            title: Note title
            content: Note content
            tags: List of tags
            
        Returns:
            The newly created Note instance
        """
        note = Note(title=title, content=content, tags=tags)
        self.notes[note.id] = note
        self.save_notes()
        return note
    
    def get_note(self, note_id: str) -> Optional[Note]:
        """
        Retrieve a note by its ID.
        
        Args:
            note_id: The note's unique identifier
            
        Returns:
            Note instance or None if not found
        """
        return self.notes.get(note_id)
    
    def get_all_notes(self) -> List[Note]:
        """
        Get all notes sorted by modification date (newest first).
        
        Returns:
            List of all Note instances
        """
        notes_list = list(self.notes.values())
        notes_list.sort(key=lambda n: n.modified_at, reverse=True)
        return notes_list
    
    def update_note(self, note_id: str, title: str = None, content: str = None, 
                    tags: List[str] = None) -> bool:
        """
        Update an existing note.
        
        Args:
            note_id: The note's unique identifier
            title: New title (optional)
            content: New content (optional)
            tags: New tags (optional)
            
        Returns:
            True if successful, False if note not found
        """
        note = self.get_note(note_id)
        if note:
            note.update(title=title, content=content, tags=tags)
            self.save_notes()
            return True
        return False
    
    def delete_note(self, note_id: str) -> bool:
        """
        Delete a note from the collection.
        
        Args:
            note_id: The note's unique identifier
            
        Returns:
            True if successful, False if note not found
        """
        if note_id in self.notes:
            del self.notes[note_id]
            self.save_notes()
            return True
        return False
    
    def search_notes(self, query: str) -> List[Note]:
        """
        Search notes by title, content, or tags.
        
        Args:
            query: Search string
            
        Returns:
            List of matching Note instances
        """
        if not query:
            return self.get_all_notes()
        
        matching_notes = [note for note in self.notes.values() 
                         if note.matches_search(query)]
        matching_notes.sort(key=lambda n: n.modified_at, reverse=True)
        return matching_notes
    
    def filter_by_tag(self, tag: str) -> List[Note]:
        """
        Filter notes by a specific tag.
        
        Args:
            tag: Tag to filter by
            
        Returns:
            List of Note instances with the specified tag
        """
        matching_notes = [note for note in self.notes.values() 
                         if tag in note.tags]
        matching_notes.sort(key=lambda n: n.modified_at, reverse=True)
        return matching_notes
    
    def get_all_tags(self) -> List[str]:
        """
        Get all unique tags across all notes.
        
        Returns:
            Sorted list of unique tags
        """
        tags = set()
        for note in self.notes.values():
            tags.update(note.tags)
        return sorted(list(tags))
    
    def save_notes(self) -> bool:
        """
        Save all notes to the JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                'notes': [note.to_dict() for note in self.notes.values()],
                'last_saved': datetime.now().isoformat()
            }
            
            # Create backup if file exists
            if os.path.exists(self.data_file):
                backup_file = f"{self.data_file}.backup"
                try:
                    with open(self.data_file, 'r') as f:
                        backup_data = f.read()
                    with open(backup_file, 'w') as f:
                        f.write(backup_data)
                except Exception as e:
                    print(f"Warning: Could not create backup: {e}")
            
            # Save notes
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving notes: {e}")
            return False
    
    def load_notes(self) -> bool:
        """
        Load notes from the JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(self.data_file):
            # No file exists yet, start with empty collection
            return True
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            notes_data = data.get('notes', [])
            self.notes = {}
            
            for note_dict in notes_data:
                note = Note.from_dict(note_dict)
                self.notes[note.id] = note
            
            return True
        except json.JSONDecodeError as e:
            print(f"Error: Corrupted JSON file: {e}")
            # Try to load backup
            return self._load_backup()
        except Exception as e:
            print(f"Error loading notes: {e}")
            return False
    
    def _load_backup(self) -> bool:
        """
        Attempt to load notes from backup file.
        
        Returns:
            True if successful, False otherwise
        """
        backup_file = f"{self.data_file}.backup"
        if not os.path.exists(backup_file):
            return False
        
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            notes_data = data.get('notes', [])
            self.notes = {}
            
            for note_dict in notes_data:
                note = Note.from_dict(note_dict)
                self.notes[note.id] = note
            
            print("Loaded notes from backup file")
            return True
        except Exception as e:
            print(f"Error loading backup: {e}")
            return False
    
    def export_note(self, note_id: str, file_path: str) -> bool:
        """
        Export a single note to a text file.
        
        Args:
            note_id: The note's unique identifier
            file_path: Path to save the exported file
            
        Returns:
            True if successful, False otherwise
        """
        note = self.get_note(note_id)
        if not note:
            return False
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {note.title}\n")
                f.write(f"Created: {note.created_at}\n")
                f.write(f"Modified: {note.modified_at}\n")
                if note.tags:
                    f.write(f"Tags: {', '.join(note.tags)}\n")
                f.write("\n" + "="*50 + "\n\n")
                f.write(note.content)
            
            return True
        except Exception as e:
            print(f"Error exporting note: {e}")
            return False
    
    def export_all_notes(self, directory: str) -> int:
        """
        Export all notes to text files in a directory.
        
        Args:
            directory: Directory path to save exported files
            
        Returns:
            Number of notes successfully exported
        """
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                print(f"Error creating directory: {e}")
                return 0
        
        count = 0
        for note in self.notes.values():
            # Create safe filename from title
            safe_title = "".join(c for c in note.title if c.isalnum() or c in (' ', '-', '_'))
            safe_title = safe_title[:50]  # Limit length
            if not safe_title:
                safe_title = "untitled"
            
            file_path = os.path.join(directory, f"{safe_title}_{note.id[:8]}.txt")
            
            if self.export_note(note.id, file_path):
                count += 1
        
        return count
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the notes collection.
        
        Returns:
            Dictionary with statistics
        """
        notes_list = list(self.notes.values())
        
        total_notes = len(notes_list)
        total_tags = len(self.get_all_tags())
        
        if total_notes == 0:
            return {
                'total_notes': 0,
                'total_tags': 0,
                'total_characters': 0,
                'average_length': 0
            }
        
        total_chars = sum(len(note.content) for note in notes_list)
        avg_length = total_chars // total_notes if total_notes > 0 else 0
        
        return {
            'total_notes': total_notes,
            'total_tags': total_tags,
            'total_characters': total_chars,
            'average_length': avg_length
        }

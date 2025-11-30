"""
Utility functions for Notes Application
Handles export, backup, and other helper functions
"""

import json
import shutil
import os
from datetime import datetime
from typing import List, Dict
from database import NotesDatabase


class NotesUtils:
    """Utility functions for notes management"""
    
    def __init__(self, db: NotesDatabase):
        """Initialize with database instance"""
        self.db = db
    
    def export_note_to_txt(self, note_id: int, output_path: str = None) -> str:
        """Export a single note to text file"""
        note = self.db.get_note(note_id)
        
        if not note:
            raise ValueError(f"Note with ID {note_id} not found")
        
        if output_path is None:
            safe_title = self._sanitize_filename(note['title'])
            output_path = f"{safe_title}.txt"
        
        content = self._format_note_as_text(note)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path
    
    def export_note_to_markdown(self, note_id: int, output_path: str = None) -> str:
        """Export a single note to markdown file"""
        note = self.db.get_note(note_id)
        
        if not note:
            raise ValueError(f"Note with ID {note_id} not found")
        
        if output_path is None:
            safe_title = self._sanitize_filename(note['title'])
            output_path = f"{safe_title}.md"
        
        content = self._format_note_as_markdown(note)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path
    
    def export_all_notes_to_txt(self, output_dir: str = "exports") -> List[str]:
        """Export all notes to text files in a directory"""
        os.makedirs(output_dir, exist_ok=True)
        
        notes = self.db.get_all_notes()
        exported_files = []
        
        for note in notes:
            safe_title = self._sanitize_filename(note['title'])
            output_path = os.path.join(output_dir, f"{safe_title}.txt")
            
            content = self._format_note_as_text(note)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            exported_files.append(output_path)
        
        return exported_files
    
    def export_all_notes_to_markdown(self, output_dir: str = "exports") -> List[str]:
        """Export all notes to markdown files in a directory"""
        os.makedirs(output_dir, exist_ok=True)
        
        notes = self.db.get_all_notes()
        exported_files = []
        
        for note in notes:
            safe_title = self._sanitize_filename(note['title'])
            output_path = os.path.join(output_dir, f"{safe_title}.md")
            
            content = self._format_note_as_markdown(note)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            exported_files.append(output_path)
        
        return exported_files
    
    def export_all_notes_to_json(self, output_path: str = "notes_export.json") -> str:
        """Export all notes to a single JSON file"""
        notes = self.db.get_all_notes()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(notes, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def backup_database(self, backup_dir: str = "backups") -> str:
        """Create a backup of the database file"""
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"notes_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        shutil.copy2(self.db.db_path, backup_path)
        
        return backup_path
    
    def restore_database(self, backup_path: str) -> bool:
        """Restore database from a backup file"""
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        shutil.copy2(backup_path, self.db.db_path)
        return True
    
    def get_statistics(self) -> Dict:
        """Get statistics about notes"""
        notes = self.db.get_all_notes()
        categories = self.db.get_all_categories()
        tags = self.db.get_all_tags()
        
        total_words = sum(len(note['content'].split()) for note in notes)
        total_chars = sum(len(note['content']) for note in notes)
        
        return {
            'total_notes': len(notes),
            'total_categories': len(categories),
            'total_tags': len(tags),
            'total_words': total_words,
            'total_characters': total_chars,
            'categories': categories,
            'tags': tags
        }
    
    def _format_note_as_text(self, note: Dict) -> str:
        """Format note as plain text"""
        lines = []
        lines.append("=" * 80)
        lines.append(note['title'])
        lines.append("=" * 80)
        lines.append("")
        
        if note['category']:
            lines.append(f"Category: {note['category']}")
        
        if note['tags']:
            lines.append(f"Tags: {', '.join(note['tags'])}")
        
        lines.append(f"Created: {note['created_at']}")
        lines.append(f"Updated: {note['updated_at']}")
        lines.append("")
        lines.append("-" * 80)
        lines.append("")
        lines.append(note['content'])
        lines.append("")
        
        return "\n".join(lines)
    
    def _format_note_as_markdown(self, note: Dict) -> str:
        """Format note as markdown"""
        lines = []
        lines.append(f"# {note['title']}")
        lines.append("")
        
        metadata = []
        if note['category']:
            metadata.append(f"**Category:** {note['category']}")
        
        if note['tags']:
            tags_formatted = ", ".join([f"`{tag}`" for tag in note['tags']])
            metadata.append(f"**Tags:** {tags_formatted}")
        
        metadata.append(f"**Created:** {note['created_at']}")
        metadata.append(f"**Updated:** {note['updated_at']}")
        
        lines.extend(metadata)
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(note['content'])
        lines.append("")
        
        return "\n".join(lines)
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename by removing invalid characters"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename.strip()
    
    def import_notes_from_json(self, json_path: str) -> int:
        """Import notes from a JSON file"""
        with open(json_path, 'r', encoding='utf-8') as f:
            notes_data = json.load(f)
        
        imported_count = 0
        for note_data in notes_data:
            self.db.create_note(
                title=note_data.get('title', 'Untitled'),
                content=note_data.get('content', ''),
                tags=note_data.get('tags', []),
                category=note_data.get('category', '')
            )
            imported_count += 1
        
        return imported_count

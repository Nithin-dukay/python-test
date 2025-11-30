"""
Note Model
Represents a single note with title, content, timestamps, and tags.
"""

from datetime import datetime
from typing import List, Dict, Any
import uuid


class Note:
    """
    A note with title, content, creation/modification timestamps, and tags.
    """
    
    def __init__(self, title: str = "", content: str = "", tags: List[str] = None, 
                 note_id: str = None, created_at: str = None, modified_at: str = None):
        """
        Initialize a new note.
        
        Args:
            title: The note's title
            content: The note's content
            tags: List of tags for organization
            note_id: Unique identifier (auto-generated if not provided)
            created_at: Creation timestamp (auto-generated if not provided)
            modified_at: Last modification timestamp (auto-generated if not provided)
        """
        self.id = note_id if note_id else str(uuid.uuid4())
        self.title = title
        self.content = content
        self.tags = tags if tags else []
        
        # Handle timestamps
        current_time = datetime.now().isoformat()
        self.created_at = created_at if created_at else current_time
        self.modified_at = modified_at if modified_at else current_time
    
    def update(self, title: str = None, content: str = None, tags: List[str] = None):
        """
        Update note fields and refresh the modified timestamp.
        
        Args:
            title: New title (optional)
            content: New content (optional)
            tags: New tags list (optional)
        """
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        if tags is not None:
            self.tags = tags
        
        self.modified_at = datetime.now().isoformat()
    
    def add_tag(self, tag: str):
        """Add a tag to the note if it doesn't already exist."""
        if tag and tag not in self.tags:
            self.tags.append(tag)
            self.modified_at = datetime.now().isoformat()
    
    def remove_tag(self, tag: str):
        """Remove a tag from the note."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.modified_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
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
            'modified_at': self.modified_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Note':
        """
        Create a Note instance from a dictionary.
        
        Args:
            data: Dictionary containing note data
            
        Returns:
            Note instance
        """
        return cls(
            title=data.get('title', ''),
            content=data.get('content', ''),
            tags=data.get('tags', []),
            note_id=data.get('id'),
            created_at=data.get('created_at'),
            modified_at=data.get('modified_at')
        )
    
    def get_preview(self, max_length: int = 100) -> str:
        """
        Get a preview of the note content.
        
        Args:
            max_length: Maximum length of preview
            
        Returns:
            Truncated content string
        """
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."
    
    def matches_search(self, query: str) -> bool:
        """
        Check if the note matches a search query.
        
        Args:
            query: Search string
            
        Returns:
            True if query is found in title, content, or tags
        """
        query_lower = query.lower()
        return (query_lower in self.title.lower() or 
                query_lower in self.content.lower() or
                any(query_lower in tag.lower() for tag in self.tags))
    
    def __str__(self) -> str:
        """String representation of the note."""
        tags_str = f" [{', '.join(self.tags)}]" if self.tags else ""
        return f"{self.title}{tags_str}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Note(id={self.id}, title='{self.title}', tags={self.tags})"

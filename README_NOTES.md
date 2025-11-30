# Notes Application

A comprehensive command-line note-taking application built with Python, featuring persistent storage, search capabilities, and export functionality.

## Features

### Core Functionality
- ✅ **Create Notes**: Add new notes with title, content, and optional tags
- ✅ **View Notes**: List all notes or view individual note details
- ✅ **Edit Notes**: Update existing notes (title, content, or tags)
- ✅ **Delete Notes**: Remove notes with confirmation
- ✅ **Search**: Search notes by title, content, or tags
- ✅ **Export**: Export individual notes to text files
- ✅ **Statistics**: View statistics about your notes collection

### Technical Features
- 📁 **Persistent Storage**: Notes are saved to JSON file automatically
- 🔍 **Case-Insensitive Search**: Find notes easily regardless of case
- 🏷️ **Tagging System**: Organize notes with multiple tags
- ⏰ **Timestamps**: Automatic tracking of creation and modification times
- 🔒 **Error Handling**: Robust error handling for file operations and user input
- 📝 **Input Validation**: Prevents empty notes and invalid operations

## Installation

No additional dependencies required beyond Python 3.6+. The application uses only standard library modules.

## Usage

### Running the Application

```bash
python3 notes_cli.py
```

### Main Menu Options

1. **Create new note**: Add a new note with title, content, and optional tags
2. **List all notes**: View all notes with titles and creation dates
3. **View note**: Display full details of a specific note
4. **Edit note**: Modify an existing note's title, content, or tags
5. **Delete note**: Remove a note (with confirmation)
6. **Search notes**: Find notes by searching title, content, or tags
7. **Export note**: Save a note to a text file
8. **Show statistics**: View statistics about your notes collection
9. **Exit**: Close the application

### Creating a Note

When creating a note:
1. Enter a title
2. Enter content (multi-line supported)
3. Type a single `.` on a new line to finish, or press Ctrl+D
4. Optionally add tags (comma-separated)

Example:
```
Enter note title: My First Note
Enter note content:
(Enter a line with just '.' to finish, or Ctrl+D)
This is the content of my note.
It can span multiple lines.
.
Enter tags (comma-separated, optional): personal, ideas
```

### Searching Notes

You can search in:
- Title only
- Content only
- Both title and content
- Tags

The search is case-insensitive and finds partial matches.

### Exporting Notes

Exported notes are saved to the `exported_notes/` directory as text files with the format:
```
Title: [Note Title]
Created: [Creation Date]
Updated: [Last Update Date]
Tags: [Tag1, Tag2, ...]

============================================================

[Note Content]
```

## File Structure

```
/vercel/sandbox/
├── notes_cli.py           # Interactive CLI interface
├── notes_manager.py       # Core note management logic
├── notes_data/            # Directory for persistent storage
│   └── notes.json         # JSON file containing all notes
└── exported_notes/        # Directory for exported note files
```

## Data Storage

Notes are stored in JSON format in `notes_data/notes.json`. Each note contains:
- `id`: Unique identifier (UUID)
- `title`: Note title
- `content`: Note content
- `tags`: List of tags
- `created_at`: Creation timestamp (ISO format)
- `updated_at`: Last modification timestamp (ISO format)

Example JSON structure:
```json
{
  "509ff93d-0c46-4f31-b046-e65276aeb11c": {
    "id": "509ff93d-0c46-4f31-b046-e65276aeb11c",
    "title": "Test Note 1",
    "content": "This is the content",
    "tags": ["test", "demo"],
    "created_at": "2025-11-30T18:42:52.768040",
    "updated_at": "2025-11-30T18:42:52.768415"
  }
}
```

## API Reference

### NotesManager Class

The `NotesManager` class provides the core functionality:

#### Methods

- `create_note(title, content, tags=None)`: Create a new note
- `get_note(note_id)`: Retrieve a note by ID
- `get_all_notes(sort_by='created_at', reverse=True)`: Get all notes
- `update_note(note_id, title=None, content=None, tags=None)`: Update a note
- `delete_note(note_id)`: Delete a note
- `search_notes(query, search_in='both')`: Search for notes
- `filter_by_tags(tags)`: Filter notes by tags
- `export_note(note_id, export_dir='exported_notes')`: Export a note to file
- `get_statistics()`: Get statistics about the notes collection

### Note Class

The `Note` class represents an individual note:

#### Attributes

- `id`: Unique identifier (UUID string)
- `title`: Note title
- `content`: Note content
- `tags`: List of tags
- `created_at`: Creation timestamp (ISO format string)
- `updated_at`: Last modification timestamp (ISO format string)

#### Methods

- `update(title=None, content=None, tags=None)`: Update note fields
- `to_dict()`: Convert note to dictionary
- `from_dict(data)`: Create note from dictionary (class method)

## Examples

### Programmatic Usage

You can also use the notes manager programmatically:

```python
from notes_manager import NotesManager

# Initialize manager
manager = NotesManager()

# Create a note
note = manager.create_note(
    title="My Note",
    content="This is my note content",
    tags=["important", "work"]
)

# List all notes
notes = manager.get_all_notes()
for note in notes:
    print(f"{note.title}: {note.content[:50]}...")

# Search notes
results = manager.search_notes("important")
print(f"Found {len(results)} notes")

# Update a note
manager.update_note(note.id, content="Updated content")

# Export a note
filepath = manager.export_note(note.id)
print(f"Exported to: {filepath}")

# Delete a note
manager.delete_note(note.id)
```

## Error Handling

The application handles various error scenarios:
- Empty titles or content
- Invalid note IDs
- File I/O errors
- Corrupted JSON data
- Permission issues

All errors are reported with clear, user-friendly messages.

## Best Practices

1. **Regular Backups**: Backup the `notes_data/notes.json` file regularly
2. **Tag Consistently**: Use consistent tag names for better organization
3. **Descriptive Titles**: Use clear, descriptive titles for easy identification
4. **Export Important Notes**: Export critical notes as backup text files

## Troubleshooting

### Notes not persisting
- Check that the `notes_data/` directory exists and is writable
- Verify that `notes.json` is not corrupted (should be valid JSON)

### Cannot find a note
- Use the list function to see all available notes
- Try searching by partial title or content
- Check if the note was accidentally deleted

### Export fails
- Ensure the `exported_notes/` directory exists and is writable
- Check available disk space

## Future Enhancements

Potential features for future versions:
- Note categories/folders
- Rich text formatting
- Attachments support
- Cloud synchronization
- Web interface
- Mobile app
- Encryption for sensitive notes
- Note sharing capabilities
- Version history

## License

This project is open source and available for educational and personal use.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Author

Created as part of a Python project demonstration.

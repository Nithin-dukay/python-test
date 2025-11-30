# Notes Application

A feature-rich note-taking application built with Python and Tkinter, offering a clean GUI for managing your notes with advanced features like search, tags, and export capabilities.

## Features

### Core Functionality
- ✅ **Create Notes**: Create new notes with title, content, and tags
- ✅ **Edit Notes**: Update existing notes with automatic timestamp tracking
- ✅ **Delete Notes**: Remove notes with confirmation dialog
- ✅ **View All Notes**: Browse all notes in a scrollable list
- ✅ **Search/Filter**: Search notes by title, content, or tags in real-time

### Data Management
- ✅ **JSON Storage**: All notes saved to `notes_data.json`
- ✅ **Auto-save**: Changes automatically saved to disk
- ✅ **Backup System**: Automatic backup creation on save
- ✅ **Data Persistence**: Notes load automatically on startup

### Organization
- ✅ **Tags**: Add multiple tags to notes for organization
- ✅ **Timestamps**: Automatic creation and modification timestamps
- ✅ **Sorting**: Notes sorted by modification date (newest first)

### Export Features
- ✅ **Export Single Note**: Export individual notes to text files
- ✅ **Export All Notes**: Batch export all notes to a directory
- ✅ **Statistics**: View collection statistics (total notes, tags, characters)

### User Interface
- ✅ **Clean GUI**: Modern Tkinter interface with intuitive layout
- ✅ **Split View**: Notes list on left, editor on right
- ✅ **Real-time Search**: Instant filtering as you type
- ✅ **Status Bar**: Feedback messages for all actions
- ✅ **Keyboard Shortcuts**: Quick access to common actions

## Installation

### Requirements
- Python 3.6 or higher
- Tkinter (usually included with Python)

### Setup
No additional dependencies required! Tkinter comes bundled with Python.

```bash
# Clone or download the files
# Navigate to the directory
cd /path/to/notes-app

# Run the application
python3 main.py
```

## Usage

### Starting the Application
```bash
python3 main.py
```

### Creating a Note
1. Click the **"New Note"** button in the left panel
2. Enter a title in the title field
3. Add tags (comma-separated) in the tags field
4. Write your content in the main text area
5. Click **"Save"** to save the note

### Editing a Note
1. Select a note from the list on the left
2. Modify the title, tags, or content
3. Click **"Save"** to update the note

### Searching Notes
1. Type in the search box at the top of the left panel
2. Notes are filtered in real-time as you type
3. Search works across titles, content, and tags

### Deleting a Note
1. Select a note from the list
2. Click the **"Delete"** button
3. Confirm the deletion in the dialog

### Exporting Notes
- **Single Note**: Select a note and click **"Export Note"**
- **All Notes**: Click **"Export All"** and choose a directory

### Viewing Statistics
Click the **"Statistics"** button to see:
- Total number of notes
- Total unique tags
- Total characters across all notes
- Average note length

### Keyboard Shortcuts
- `Ctrl+N`: Create new note
- `Ctrl+S`: Save current note
- `Ctrl+F`: Focus search box

## File Structure

```
notes-app/
├── main.py              # Application entry point
├── notes_app.py         # GUI implementation (Tkinter)
├── note_manager.py      # Business logic and data management
├── note.py              # Note model class
├── test_notes_app.py    # Comprehensive test suite
├── notes_data.json      # Data storage (created automatically)
└── README_NOTES_APP.md  # This file
```

## Architecture

### Model Layer (`note.py`)
- `Note` class: Represents a single note with all its properties
- Methods for serialization, search matching, and tag management
- Automatic timestamp handling

### Business Logic Layer (`note_manager.py`)
- `NoteManager` class: Handles all CRUD operations
- File I/O with JSON format
- Search and filter functionality
- Export capabilities
- Backup system for data safety

### Presentation Layer (`notes_app.py`)
- `NotesApp` class: Tkinter GUI implementation
- Split-panel layout with notes list and editor
- Real-time search and filtering
- User-friendly dialogs and confirmations

### Entry Point (`main.py`)
- Application launcher
- Error handling for startup
- Window close confirmation

## Data Storage

Notes are stored in JSON format in `notes_data.json`:

```json
{
  "notes": [
    {
      "id": "unique-uuid",
      "title": "Note Title",
      "content": "Note content...",
      "tags": ["tag1", "tag2"],
      "created_at": "2025-11-30T10:30:00",
      "modified_at": "2025-11-30T11:45:00"
    }
  ],
  "last_saved": "2025-11-30T11:45:00"
}
```

### Backup System
- Automatic backup created before each save
- Backup file: `notes_data.json.backup`
- Automatic recovery if main file is corrupted

## Testing

Run the comprehensive test suite:

```bash
python3 test_notes_app.py
```

Tests cover:
- Note creation and updates
- Serialization/deserialization
- Search functionality
- CRUD operations
- Data persistence
- Export features
- Error handling

## Error Handling

The application includes robust error handling for:
- Missing or corrupted data files
- File permission issues
- Invalid note IDs
- Export failures
- Backup restoration

## Code Quality

- **Object-Oriented Design**: Clean separation of concerns
- **Type Hints**: Full type annotations for better code clarity
- **Documentation**: Comprehensive docstrings for all classes and methods
- **Error Handling**: Try-catch blocks for all file operations
- **Comments**: Explanatory comments for complex logic

## Future Enhancements

Potential features for future versions:
- Rich text formatting (bold, italic, lists)
- Note categories/folders
- Markdown support
- Dark mode theme
- Cloud synchronization
- Attachments support
- Note linking
- Full-text search with highlighting
- Undo/redo functionality
- Note templates

## Troubleshooting

### Application won't start
- Ensure Python 3.6+ is installed: `python3 --version`
- Check if Tkinter is available: `python3 -c "import tkinter"`

### Notes not saving
- Check file permissions in the application directory
- Ensure sufficient disk space
- Check the backup file if main file is corrupted

### GUI issues
- Update Tkinter: Usually comes with Python updates
- Try different theme: Modify `style.theme_use()` in `notes_app.py`

## License

This is a demonstration project. Feel free to use and modify as needed.

## Author

Created as a comprehensive Python note-taking application with GUI.

---

**Enjoy taking notes!** 📝

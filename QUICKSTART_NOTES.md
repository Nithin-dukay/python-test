# Quick Start Guide - Notes Application

## 🚀 Getting Started in 3 Steps

### 1. Run the Demo
See the notes application in action:
```bash
python3 demo_notes.py
```

### 2. Start the Interactive Application
Launch the full CLI interface:
```bash
python3 notes_cli.py
```

### 3. Create Your First Note
In the application menu:
1. Choose option `1` (Create new note)
2. Enter a title
3. Type your content (multiple lines supported)
4. Type `.` on a new line to finish
5. Optionally add tags

## 📋 Common Tasks

### Create a Note
```
Menu Option: 1
Title: My First Note
Content: (type your content, end with '.')
Tags: personal, ideas (optional)
```

### List All Notes
```
Menu Option: 2
```

### Search for Notes
```
Menu Option: 6
Query: python
Search in: 3 (both title and content)
```

### Export a Note
```
Menu Option: 7
Enter note number or ID
```

## 💡 Tips

- **Multi-line Content**: Press Enter for new lines, type `.` alone to finish
- **Quick Exit**: Press Ctrl+C anytime to exit
- **Note Selection**: Use note number (1, 2, 3...) or partial ID
- **Tags**: Separate multiple tags with commas
- **Search**: Search is case-insensitive and finds partial matches

## 📁 File Locations

- **Notes Data**: `notes_data/notes.json`
- **Exported Notes**: `exported_notes/`
- **Documentation**: `README_NOTES.md`

## 🔧 Programmatic Usage

Use the notes manager in your own Python scripts:

```python
from notes_manager import NotesManager

# Initialize
manager = NotesManager()

# Create a note
note = manager.create_note(
    title="My Note",
    content="Note content here",
    tags=["tag1", "tag2"]
)

# List all notes
notes = manager.get_all_notes()

# Search
results = manager.search_notes("keyword")

# Update
manager.update_note(note.id, content="New content")

# Delete
manager.delete_note(note.id)
```

## ❓ Need Help?

- Full documentation: `README_NOTES.md`
- Run demo: `python3 demo_notes.py`
- In CLI: Choose option `9` to exit

## ✨ Features at a Glance

✅ Create, edit, delete notes  
✅ Search by title, content, or tags  
✅ Export to text files  
✅ Automatic timestamps  
✅ Persistent storage  
✅ Tag-based organization  
✅ Statistics and insights  

---

**Ready to start?** Run `python3 notes_cli.py` now!

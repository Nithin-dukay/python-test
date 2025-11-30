# Quick Start Guide - Notes Application

## Installation & Setup

### 1. Check Python Installation
```bash
python3 --version
# Should show Python 3.6 or higher
```

### 2. Verify Tkinter (GUI library)
```bash
python3 -c "import tkinter; print('Tkinter is available!')"
```

### 3. Run the Application
```bash
python3 main.py
```

## First Time Setup

### Option 1: Start with Demo Notes
```bash
# Create sample notes to explore the app
python3 demo_notes.py

# Then launch the app
python3 main.py
```

### Option 2: Start Fresh
```bash
# Just launch the app - it will create an empty notes collection
python3 main.py
```

## Basic Operations

### Creating Your First Note
1. Click **"New Note"** button (left panel)
2. Type a title (e.g., "My First Note")
3. Add tags separated by commas (e.g., "personal, ideas")
4. Write your content in the large text area
5. Click **"Save"** button

### Editing a Note
1. Click on any note in the list (left panel)
2. Make your changes
3. Click **"Save"** to update

### Searching Notes
- Type in the search box at the top
- Results filter automatically as you type
- Search works on titles, content, and tags

### Deleting a Note
1. Select the note from the list
2. Click **"Delete"** button
3. Confirm when prompted

### Exporting Notes
- **Single Note**: Select note → Click "Export Note" → Choose location
- **All Notes**: Click "Export All" → Choose folder

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | Create new note |
| `Ctrl+S` | Save current note |
| `Ctrl+F` | Focus search box |

## File Locations

- **Notes Data**: `notes_data.json` (in the same directory)
- **Backup**: `notes_data.json.backup` (auto-created)
- **Exports**: You choose the location when exporting

## Testing the Application

Run the test suite to verify everything works:
```bash
python3 test_notes_app.py
```

You should see:
```
✓ ALL TESTS PASSED!
```

## Tips & Tricks

### Organizing with Tags
- Use tags like: `work`, `personal`, `ideas`, `urgent`
- Multiple tags help you find notes faster
- Tags appear in the notes list for quick identification

### Search Tips
- Search is case-insensitive
- Searches across title, content, AND tags
- Use specific keywords for better results

### Best Practices
1. **Use descriptive titles** - Makes notes easier to find
2. **Add relevant tags** - Helps with organization
3. **Save frequently** - Use Ctrl+S often
4. **Export important notes** - Create backups of critical information

## Troubleshooting

### "No module named 'tkinter'"
**Solution**: Install tkinter
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (usually pre-installed)
# Windows (usually pre-installed)
```

### Application won't start
1. Check Python version: `python3 --version`
2. Verify file permissions
3. Check if `notes_data.json` is corrupted (delete it to start fresh)

### Notes not saving
1. Check disk space
2. Verify write permissions in the directory
3. Look for error messages in the terminal

### GUI looks strange
- Try updating Python to the latest version
- Tkinter appearance varies by operating system

## Getting Help

### View Statistics
Click the **"Statistics"** button to see:
- Total number of notes
- Number of unique tags
- Total characters written
- Average note length

### Check Data File
```bash
# View your notes data
cat notes_data.json

# Check file size
ls -lh notes_data.json
```

## Next Steps

1. ✅ Create your first note
2. ✅ Try the search feature
3. ✅ Add some tags
4. ✅ Export a note
5. ✅ Explore the statistics

## Advanced Usage

### Backup Your Notes
```bash
# Manual backup
cp notes_data.json notes_backup_$(date +%Y%m%d).json
```

### Restore from Backup
```bash
# If main file is corrupted, the app auto-loads from .backup
# Or manually restore:
cp notes_data.json.backup notes_data.json
```

### Migrate Notes
Simply copy `notes_data.json` to another computer with the app installed!

---

**Happy Note-Taking!** 📝

For detailed documentation, see `README_NOTES_APP.md`

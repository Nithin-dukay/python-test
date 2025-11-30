# 📝 Notes Application

A comprehensive, feature-rich note-taking web application built with Python Flask and modern web technologies.

## ✨ Features

### Core Functionality
- ✅ **Create, Edit, Delete Notes** - Full CRUD operations for managing notes
- ✅ **Auto-Save** - Automatic saving every 3 seconds while editing
- ✅ **Search** - Real-time search across note titles and content
- ✅ **Tags & Categories** - Organize notes with custom tags and categories
- ✅ **Timestamps** - Track creation and last modified dates

### Advanced Features
- 📤 **Export Notes** - Export individual notes to TXT or Markdown format
- 📦 **Bulk Export** - Export all notes to JSON format
- 💾 **Backup System** - Create database backups with timestamps
- 📊 **Statistics** - View comprehensive statistics about your notes
- 🎨 **Markdown Preview** - Toggle between edit and preview modes
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices

### User Interface
- 🎯 Clean, modern, and intuitive interface
- 🌈 Beautiful gradient design with smooth animations
- 📋 List view with note previews
- ✏️ Full-featured editor with metadata fields
- 🔍 Advanced filtering by category and tags
- 📈 Word count and character statistics

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
# Install pip if not already installed
python3 -m ensurepip --upgrade

# Install required packages
pip install flask
```

### Step 2: Run the Application

```bash
# Navigate to the project directory
cd /vercel/sandbox

# Start the Flask server
python3 notes_app.py
```

The application will start on `http://localhost:5000`

### Step 3: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### Creating a Note
1. Click the **"+ New Note"** button in the header
2. Enter a title for your note
3. Add content in the text area
4. Optionally add a category and tags (comma-separated)
5. The note will auto-save every 3 seconds

### Editing a Note
1. Click on any note in the left sidebar to open it
2. Make your changes in the editor
3. Changes are automatically saved after 3 seconds
4. Or click the **"Save"** button to save immediately

### Searching Notes
1. Use the search box at the top of the sidebar
2. Type your search query
3. Results update in real-time as you type
4. Search works across both titles and content

### Organizing with Categories
1. Enter a category name in the "Category" field when editing a note
2. Click on any category in the sidebar to filter notes
3. Click "All Notes" to clear the filter

### Using Tags
1. Add tags in the "Tags" field (comma-separated)
2. Click on any tag in the sidebar to filter notes by that tag
3. Tags help you cross-reference notes across categories

### Exporting Notes
- **Single Note**: Click "Export" button while viewing a note, choose TXT or Markdown
- **All Notes**: Click "Export All" in the header to download all notes as JSON

### Creating Backups
1. Click the **"Backup"** button in the header
2. A timestamped backup will be created in the `backups/` directory
3. Backups are SQLite database files that can be restored if needed

### Viewing Statistics
1. Click the **"Statistics"** button in the header
2. View total notes, categories, tags, words, and characters
3. Get insights into your note-taking habits

## 🗂️ Project Structure

```
/vercel/sandbox/
├── notes_app.py           # Main Flask application
├── database.py            # SQLite database operations
├── utils.py               # Export, backup, and utility functions
├── requirements.txt       # Python dependencies
├── notes.db              # SQLite database (created on first run)
├── templates/
│   └── index.html        # Main application HTML
├── static/
│   ├── css/
│   │   └── style.css     # Application styles
│   └── js/
│       └── app.js        # Client-side JavaScript
└── backups/              # Database backups directory
```

## 🔧 Technical Details

### Backend (Python/Flask)
- **Flask** - Web framework for REST API
- **SQLite** - Lightweight database for persistent storage
- **JSON** - Data serialization for exports

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with flexbox and grid
- **Vanilla JavaScript** - No framework dependencies
- **Fetch API** - Asynchronous HTTP requests

### Database Schema
```sql
notes (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    tags TEXT (JSON array),
    category TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

## 🌐 API Endpoints

### Notes
- `GET /api/notes` - Get all notes (supports ?search, ?category, ?tag)
- `GET /api/notes/<id>` - Get single note
- `POST /api/notes` - Create new note
- `PUT /api/notes/<id>` - Update note
- `DELETE /api/notes/<id>` - Delete note

### Metadata
- `GET /api/categories` - Get all categories
- `GET /api/tags` - Get all tags
- `GET /api/statistics` - Get statistics

### Export & Backup
- `GET /api/export/note/<id>/<format>` - Export single note (txt/md)
- `GET /api/export/all/json` - Export all notes as JSON
- `POST /api/backup` - Create database backup
- `POST /api/import` - Import notes from JSON

## 🎨 Features in Detail

### Auto-Save
- Triggers 3 seconds after you stop typing
- Visual indicator shows save status
- Prevents data loss from accidental closures

### Search
- Real-time filtering as you type
- Searches both title and content
- Case-insensitive matching

### Markdown Preview
- Click the "👁️ Preview" button to toggle
- Supports basic markdown syntax:
  - `**bold**` → **bold**
  - `*italic*` → *italic*
  - `` `code` `` → `code`
  - `# Heading` → Heading

### Export Formats
- **TXT** - Plain text with metadata header
- **Markdown** - Formatted markdown with frontmatter
- **JSON** - Complete data export for backup/migration

## 🔒 Data Storage

All data is stored locally in the `notes.db` SQLite database file. Your notes are:
- ✅ Stored on your local machine
- ✅ Not sent to any external servers
- ✅ Backed up with the backup feature
- ✅ Exportable at any time

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is already in use, edit `notes_app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
to a different port number.

### Database Locked
If you get a "database is locked" error:
1. Close all instances of the application
2. Delete the `notes.db` file (backup first!)
3. Restart the application

### Import Errors
If you get module import errors:
```bash
pip install --upgrade flask
```

## 📝 Tips & Best Practices

1. **Use Categories** - Organize notes by project, topic, or context
2. **Tag Liberally** - Tags help you find related notes quickly
3. **Regular Backups** - Create backups before major changes
4. **Export Important Notes** - Keep copies of critical information
5. **Use Markdown** - Format your notes for better readability

## 🚀 Future Enhancements

Potential features for future versions:
- Rich text editor with formatting toolbar
- Note sharing and collaboration
- Attachments and file uploads
- Dark mode toggle
- Note templates
- Reminders and due dates
- Full-text search with highlighting
- Note linking and backlinks

## 📄 License

This project is open source and available for personal and educational use.

## 🤝 Contributing

Feel free to fork, modify, and enhance this application for your needs!

---

**Enjoy taking notes! 📝✨**

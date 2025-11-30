// Global state
let currentNote = null;
let allNotes = [];
let autoSaveTimer = null;
let isPreviewMode = false;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});

// Initialize application
async function initializeApp() {
    await loadNotes();
    await loadCategories();
    await loadTags();
}

// Setup event listeners
function setupEventListeners() {
    // Header buttons
    document.getElementById('newNoteBtn').addEventListener('click', createNewNote);
    document.getElementById('statsBtn').addEventListener('click', showStatistics);
    document.getElementById('backupBtn').addEventListener('click', createBackup);
    document.getElementById('exportBtn').addEventListener('click', exportAllNotes);
    
    // Search
    document.getElementById('searchInput').addEventListener('input', handleSearch);
    
    // Editor
    document.getElementById('noteTitle').addEventListener('input', handleNoteChange);
    document.getElementById('noteContent').addEventListener('input', handleNoteChange);
    document.getElementById('noteCategory').addEventListener('input', handleNoteChange);
    document.getElementById('noteTags').addEventListener('input', handleNoteChange);
    
    // Editor buttons
    document.getElementById('saveBtn').addEventListener('click', saveCurrentNote);
    document.getElementById('deleteBtn').addEventListener('click', deleteCurrentNote);
    document.getElementById('exportNoteBtn').addEventListener('click', () => openModal('exportModal'));
    
    // Toolbar
    document.querySelector('[data-action="preview"]').addEventListener('click', togglePreview);
}

// Load all notes
async function loadNotes(filter = {}) {
    try {
        let url = '/api/notes';
        const params = new URLSearchParams(filter);
        if (params.toString()) {
            url += '?' + params.toString();
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            allNotes = data.notes;
            renderNotesList(allNotes);
        }
    } catch (error) {
        console.error('Error loading notes:', error);
        showNotification('Error loading notes', 'error');
    }
}

// Render notes list
function renderNotesList(notes) {
    const notesList = document.getElementById('notesList');
    
    if (notes.length === 0) {
        notesList.innerHTML = '<div class="loading">No notes found</div>';
        return;
    }
    
    notesList.innerHTML = notes.map(note => {
        const preview = note.content.substring(0, 100).replace(/\n/g, ' ');
        const date = new Date(note.updated_at).toLocaleDateString();
        
        return `
            <div class="note-item ${currentNote && currentNote.id === note.id ? 'active' : ''}" 
                 data-note-id="${note.id}">
                <div class="note-item-title">${escapeHtml(note.title)}</div>
                <div class="note-item-preview">${escapeHtml(preview)}...</div>
                <div class="note-item-meta">
                    <span>${note.category || 'Uncategorized'}</span>
                    <span>${date}</span>
                </div>
            </div>
        `;
    }).join('');
    
    // Add click listeners
    document.querySelectorAll('.note-item').forEach(item => {
        item.addEventListener('click', () => {
            const noteId = parseInt(item.dataset.noteId);
            loadNote(noteId);
        });
    });
}

// Load single note
async function loadNote(noteId) {
    try {
        const response = await fetch(`/api/notes/${noteId}`);
        const data = await response.json();
        
        if (data.success) {
            currentNote = data.note;
            displayNote(currentNote);
        }
    } catch (error) {
        console.error('Error loading note:', error);
        showNotification('Error loading note', 'error');
    }
}

// Display note in editor
function displayNote(note) {
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('editor').style.display = 'flex';
    
    document.getElementById('noteTitle').value = note.title;
    document.getElementById('noteContent').value = note.content;
    document.getElementById('noteCategory').value = note.category || '';
    document.getElementById('noteTags').value = note.tags.join(', ');
    
    updateTimestamp(note);
    updateWordCount(note.content);
    
    // Update active state in list
    document.querySelectorAll('.note-item').forEach(item => {
        item.classList.toggle('active', parseInt(item.dataset.noteId) === note.id);
    });
    
    // Reset save button
    const saveBtn = document.getElementById('saveBtn');
    saveBtn.textContent = 'Saved';
    saveBtn.disabled = true;
    saveBtn.classList.remove('btn-primary');
    saveBtn.classList.add('btn-success');
}

// Create new note
async function createNewNote() {
    try {
        const response = await fetch('/api/notes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: 'Untitled Note',
                content: '',
                tags: [],
                category: ''
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            await loadNotes();
            loadNote(data.note.id);
            showNotification('New note created', 'success');
        }
    } catch (error) {
        console.error('Error creating note:', error);
        showNotification('Error creating note', 'error');
    }
}

// Handle note changes
function handleNoteChange() {
    if (!currentNote) return;
    
    // Update save button
    const saveBtn = document.getElementById('saveBtn');
    saveBtn.textContent = 'Save';
    saveBtn.disabled = false;
    saveBtn.classList.remove('btn-success');
    saveBtn.classList.add('btn-primary');
    
    // Update word count
    const content = document.getElementById('noteContent').value;
    updateWordCount(content);
    
    // Clear existing timer
    if (autoSaveTimer) {
        clearTimeout(autoSaveTimer);
    }
    
    // Set new auto-save timer (3 seconds)
    autoSaveTimer = setTimeout(() => {
        saveCurrentNote(true);
    }, 3000);
}

// Save current note
async function saveCurrentNote(isAutoSave = false) {
    if (!currentNote) return;
    
    const title = document.getElementById('noteTitle').value || 'Untitled Note';
    const content = document.getElementById('noteContent').value;
    const category = document.getElementById('noteCategory').value;
    const tagsInput = document.getElementById('noteTags').value;
    const tags = tagsInput ? tagsInput.split(',').map(t => t.trim()).filter(t => t) : [];
    
    try {
        const response = await fetch(`/api/notes/${currentNote.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title,
                content,
                category,
                tags
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentNote = data.note;
            updateTimestamp(currentNote);
            
            // Update save button
            const saveBtn = document.getElementById('saveBtn');
            saveBtn.textContent = 'Saved';
            saveBtn.disabled = true;
            saveBtn.classList.remove('btn-primary');
            saveBtn.classList.add('btn-success');
            
            // Reload lists
            await loadNotes();
            await loadCategories();
            await loadTags();
            
            if (!isAutoSave) {
                showNotification('Note saved successfully', 'success');
            }
        }
    } catch (error) {
        console.error('Error saving note:', error);
        showNotification('Error saving note', 'error');
    }
}

// Delete current note
async function deleteCurrentNote() {
    if (!currentNote) return;
    
    if (!confirm('Are you sure you want to delete this note?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/notes/${currentNote.id}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Note deleted successfully', 'success');
            currentNote = null;
            
            document.getElementById('editor').style.display = 'none';
            document.getElementById('emptyState').style.display = 'flex';
            
            await loadNotes();
            await loadCategories();
            await loadTags();
        }
    } catch (error) {
        console.error('Error deleting note:', error);
        showNotification('Error deleting note', 'error');
    }
}

// Handle search
function handleSearch(e) {
    const query = e.target.value.trim();
    
    if (query) {
        loadNotes({ search: query });
    } else {
        loadNotes();
    }
}

// Load categories
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();
        
        if (data.success) {
            renderCategories(data.categories);
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Render categories
function renderCategories(categories) {
    const categoriesList = document.getElementById('categoriesList');
    
    let html = '<button class="filter-item active" data-category="">All Notes</button>';
    
    categories.forEach(category => {
        html += `<button class="filter-item" data-category="${escapeHtml(category)}">${escapeHtml(category)}</button>`;
    });
    
    categoriesList.innerHTML = html;
    
    // Add click listeners
    categoriesList.querySelectorAll('.filter-item').forEach(item => {
        item.addEventListener('click', () => {
            categoriesList.querySelectorAll('.filter-item').forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            
            const category = item.dataset.category;
            if (category) {
                loadNotes({ category });
            } else {
                loadNotes();
            }
        });
    });
}

// Load tags
async function loadTags() {
    try {
        const response = await fetch('/api/tags');
        const data = await response.json();
        
        if (data.success) {
            renderTags(data.tags);
        }
    } catch (error) {
        console.error('Error loading tags:', error);
    }
}

// Render tags
function renderTags(tags) {
    const tagsList = document.getElementById('tagsList');
    
    if (tags.length === 0) {
        tagsList.innerHTML = '<span class="no-items">No tags yet</span>';
        return;
    }
    
    tagsList.innerHTML = tags.map(tag => 
        `<span class="tag-item" data-tag="${escapeHtml(tag)}">${escapeHtml(tag)}</span>`
    ).join('');
    
    // Add click listeners
    tagsList.querySelectorAll('.tag-item').forEach(item => {
        item.addEventListener('click', () => {
            const tag = item.dataset.tag;
            loadNotes({ tag });
        });
    });
}

// Show statistics
async function showStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        
        if (data.success) {
            const stats = data.statistics;
            
            const statsHtml = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">${stats.total_notes}</div>
                        <div class="stat-label">Total Notes</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.total_categories}</div>
                        <div class="stat-label">Categories</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.total_tags}</div>
                        <div class="stat-label">Tags</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.total_words.toLocaleString()}</div>
                        <div class="stat-label">Total Words</div>
                    </div>
                </div>
            `;
            
            document.getElementById('statsContent').innerHTML = statsHtml;
            openModal('statsModal');
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
        showNotification('Error loading statistics', 'error');
    }
}

// Create backup
async function createBackup() {
    try {
        const response = await fetch('/api/backup', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Backup created successfully', 'success');
        }
    } catch (error) {
        console.error('Error creating backup:', error);
        showNotification('Error creating backup', 'error');
    }
}

// Export all notes
async function exportAllNotes() {
    try {
        window.location.href = '/api/export/all/json';
        showNotification('Exporting all notes...', 'success');
    } catch (error) {
        console.error('Error exporting notes:', error);
        showNotification('Error exporting notes', 'error');
    }
}

// Export current note
function exportCurrentNote(format) {
    if (!currentNote) return;
    
    window.location.href = `/api/export/note/${currentNote.id}/${format}`;
    closeModal('exportModal');
    showNotification(`Exporting note as ${format.toUpperCase()}...`, 'success');
}

// Toggle preview mode
function togglePreview() {
    isPreviewMode = !isPreviewMode;
    
    const textarea = document.getElementById('noteContent');
    const preview = document.getElementById('notePreview');
    
    if (isPreviewMode) {
        preview.innerHTML = formatMarkdown(textarea.value);
        textarea.style.display = 'none';
        preview.style.display = 'block';
    } else {
        textarea.style.display = 'block';
        preview.style.display = 'none';
    }
}

// Format markdown (simple implementation)
function formatMarkdown(text) {
    return text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/`(.+?)`/g, '<code>$1</code>')
        .replace(/^# (.+)$/gm, '<h1>$1</h1>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^### (.+)$/gm, '<h3>$1</h3>');
}

// Update timestamp
function updateTimestamp(note) {
    const timestamp = document.getElementById('noteTimestamp');
    const created = new Date(note.created_at).toLocaleString();
    const updated = new Date(note.updated_at).toLocaleString();
    timestamp.textContent = `Created: ${created} | Updated: ${updated}`;
}

// Update word count
function updateWordCount(content) {
    const words = content.trim().split(/\s+/).filter(w => w).length;
    document.getElementById('wordCount').textContent = `${words} word${words !== 1 ? 's' : ''}`;
}

// Modal functions
function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Show notification
function showNotification(message, type = 'info') {
    const editorInfo = document.getElementById('editorInfo');
    const originalText = editorInfo.textContent;
    
    editorInfo.textContent = message;
    editorInfo.style.color = type === 'error' ? '#f56565' : type === 'success' ? '#48bb78' : '#667eea';
    
    setTimeout(() => {
        editorInfo.textContent = originalText;
        editorInfo.style.color = '#48bb78';
    }, 3000);
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Close modals on outside click
window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

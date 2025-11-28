class NotesApp {
    constructor() {
        this.notes = this.loadNotes();
        this.editingNoteId = null;

        this.noteTitleInput = document.getElementById('note-title');
        this.noteContentInput = document.getElementById('note-content');
        this.addNoteBtn = document.getElementById('add-note-btn');
        this.cancelBtn = document.getElementById('cancel-btn');
        this.searchInput = document.getElementById('search-input');
        this.notesContainer = document.getElementById('notes-container');
        this.emptyState = document.getElementById('empty-state');

        this.initEventListeners();
        this.renderNotes();
    }

    initEventListeners() {
        this.addNoteBtn.addEventListener('click', () => this.handleAddNote());
        this.cancelBtn.addEventListener('click', () => this.handleCancel());
        this.searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));

        this.noteTitleInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.noteContentInput.focus();
            }
        });
    }

    loadNotes() {
        const savedNotes = localStorage.getItem('notes');
        return savedNotes ? JSON.parse(savedNotes) : [];
    }

    saveNotes() {
        localStorage.setItem('notes', JSON.stringify(this.notes));
    }

    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    handleAddNote() {
        const title = this.noteTitleInput.value.trim();
        const content = this.noteContentInput.value.trim();

        if (!title && !content) {
            alert('Please enter a title or content for your note');
            return;
        }

        if (this.editingNoteId) {
            this.updateNote(this.editingNoteId, title, content);
        } else {
            this.addNote(title, content);
        }

        this.clearInputs();
        this.renderNotes();
    }

    addNote(title, content) {
        const note = {
            id: this.generateId(),
            title: title || 'Untitled',
            content: content,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };

        this.notes.unshift(note);
        this.saveNotes();
    }

    updateNote(id, title, content) {
        const noteIndex = this.notes.findIndex(note => note.id === id);
        if (noteIndex !== -1) {
            this.notes[noteIndex].title = title || 'Untitled';
            this.notes[noteIndex].content = content;
            this.notes[noteIndex].updatedAt = new Date().toISOString();
            this.saveNotes();
        }

        this.editingNoteId = null;
        this.addNoteBtn.textContent = 'Add Note';
        this.cancelBtn.style.display = 'none';
    }

    deleteNote(id) {
        if (confirm('Are you sure you want to delete this note?')) {
            this.notes = this.notes.filter(note => note.id !== id);
            this.saveNotes();
            this.renderNotes();
        }
    }

    editNote(id) {
        const note = this.notes.find(note => note.id === id);
        if (note) {
            this.noteTitleInput.value = note.title === 'Untitled' ? '' : note.title;
            this.noteContentInput.value = note.content;
            this.editingNoteId = id;
            this.addNoteBtn.textContent = 'Update Note';
            this.cancelBtn.style.display = 'inline-block';
            this.noteTitleInput.focus();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    handleCancel() {
        this.clearInputs();
        this.editingNoteId = null;
        this.addNoteBtn.textContent = 'Add Note';
        this.cancelBtn.style.display = 'none';
    }

    clearInputs() {
        this.noteTitleInput.value = '';
        this.noteContentInput.value = '';
    }

    handleSearch(query) {
        const filteredNotes = this.notes.filter(note => {
            const searchTerm = query.toLowerCase();
            return note.title.toLowerCase().includes(searchTerm) ||
                   note.content.toLowerCase().includes(searchTerm);
        });

        this.renderNotes(filteredNotes);
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 0) {
            const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
            if (diffHours === 0) {
                const diffMinutes = Math.floor(diffTime / (1000 * 60));
                return diffMinutes === 0 ? 'Just now' : `${diffMinutes} minute${diffMinutes > 1 ? 's' : ''} ago`;
            }
            return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        } else if (diffDays === 1) {
            return 'Yesterday';
        } else if (diffDays < 7) {
            return `${diffDays} days ago`;
        } else {
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        }
    }

    createNoteCard(note) {
        const noteCard = document.createElement('div');
        noteCard.className = 'note-card';

        const noteHeader = document.createElement('div');
        noteHeader.className = 'note-header';

        const noteTitle = document.createElement('div');
        noteTitle.className = 'note-title';
        noteTitle.textContent = note.title;

        const noteActions = document.createElement('div');
        noteActions.className = 'note-actions';

        const editBtn = document.createElement('button');
        editBtn.className = 'note-btn edit-btn';
        editBtn.innerHTML = '✏️';
        editBtn.title = 'Edit note';
        editBtn.addEventListener('click', () => this.editNote(note.id));

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'note-btn delete-btn';
        deleteBtn.innerHTML = '🗑️';
        deleteBtn.title = 'Delete note';
        deleteBtn.addEventListener('click', () => this.deleteNote(note.id));

        noteActions.appendChild(editBtn);
        noteActions.appendChild(deleteBtn);

        noteHeader.appendChild(noteTitle);
        noteHeader.appendChild(noteActions);

        const noteContent = document.createElement('div');
        noteContent.className = 'note-content';
        noteContent.textContent = note.content;

        const noteDate = document.createElement('div');
        noteDate.className = 'note-date';
        noteDate.textContent = this.formatDate(note.updatedAt);

        noteCard.appendChild(noteHeader);
        noteCard.appendChild(noteContent);
        noteCard.appendChild(noteDate);

        return noteCard;
    }

    renderNotes(notesToRender = this.notes) {
        this.notesContainer.innerHTML = '';

        if (notesToRender.length === 0) {
            this.emptyState.classList.remove('hidden');
            this.notesContainer.classList.add('hidden');
        } else {
            this.emptyState.classList.add('hidden');
            this.notesContainer.classList.remove('hidden');

            notesToRender.forEach(note => {
                const noteCard = this.createNoteCard(note);
                this.notesContainer.appendChild(noteCard);
            });
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new NotesApp();
});

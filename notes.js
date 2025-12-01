class NotesApp {
    constructor() {
        this.notes = this.loadNotes();
        this.currentNoteId = null;
        this.initializeElements();
        this.attachEventListeners();
        this.renderNotes();
    }

    initializeElements() {
        this.addNoteBtn = document.getElementById('addNoteBtn');
        this.modal = document.getElementById('noteModal');
        this.closeModal = document.getElementById('closeModal');
        this.saveNoteBtn = document.getElementById('saveNoteBtn');
        this.deleteNoteBtn = document.getElementById('deleteNoteBtn');
        this.noteTitle = document.getElementById('noteTitle');
        this.noteContent = document.getElementById('noteContent');
        this.notesContainer = document.getElementById('notesContainer');
        this.emptyState = document.getElementById('emptyState');
        this.searchInput = document.getElementById('searchInput');
        this.modalTitle = document.getElementById('modalTitle');
    }

    attachEventListeners() {
        this.addNoteBtn.addEventListener('click', () => this.openModal());
        this.closeModal.addEventListener('click', () => this.closeModalHandler());
        this.saveNoteBtn.addEventListener('click', () => this.saveNote());
        this.deleteNoteBtn.addEventListener('click', () => this.deleteNote());
        this.searchInput.addEventListener('input', (e) => this.searchNotes(e.target.value));

        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModalHandler();
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.classList.contains('active')) {
                this.closeModalHandler();
            }
        });
    }

    loadNotes() {
        const notes = localStorage.getItem('notes');
        return notes ? JSON.parse(notes) : [];
    }

    saveNotesToStorage() {
        localStorage.setItem('notes', JSON.stringify(this.notes));
    }

    openModal(noteId = null) {
        this.currentNoteId = noteId;

        if (noteId) {
            const note = this.notes.find(n => n.id === noteId);
            if (note) {
                this.noteTitle.value = note.title;
                this.noteContent.value = note.content;
                this.modalTitle.textContent = 'Edit Note';
                this.deleteNoteBtn.style.display = 'block';
            }
        } else {
            this.noteTitle.value = '';
            this.noteContent.value = '';
            this.modalTitle.textContent = 'New Note';
            this.deleteNoteBtn.style.display = 'none';
        }

        this.modal.classList.add('active');
        this.noteTitle.focus();
    }

    closeModalHandler() {
        this.modal.classList.remove('active');
        this.currentNoteId = null;
    }

    saveNote() {
        const title = this.noteTitle.value.trim();
        const content = this.noteContent.value.trim();

        if (!title && !content) {
            alert('Please enter a title or content for your note.');
            return;
        }

        const now = new Date().toISOString();

        if (this.currentNoteId) {
            const noteIndex = this.notes.findIndex(n => n.id === this.currentNoteId);
            if (noteIndex !== -1) {
                this.notes[noteIndex] = {
                    ...this.notes[noteIndex],
                    title: title || 'Untitled',
                    content,
                    updatedAt: now
                };
            }
        } else {
            const newNote = {
                id: Date.now().toString(),
                title: title || 'Untitled',
                content,
                createdAt: now,
                updatedAt: now
            };
            this.notes.unshift(newNote);
        }

        this.saveNotesToStorage();
        this.renderNotes();
        this.closeModalHandler();
    }

    deleteNote() {
        if (!this.currentNoteId) return;

        if (confirm('Are you sure you want to delete this note?')) {
            this.notes = this.notes.filter(n => n.id !== this.currentNoteId);
            this.saveNotesToStorage();
            this.renderNotes();
            this.closeModalHandler();
        }
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
                return diffMinutes === 0 ? 'Just now' : `${diffMinutes}m ago`;
            }
            return `${diffHours}h ago`;
        } else if (diffDays === 1) {
            return 'Yesterday';
        } else if (diffDays < 7) {
            return `${diffDays} days ago`;
        } else {
            return date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
            });
        }
    }

    searchNotes(query) {
        const searchQuery = query.toLowerCase().trim();

        if (!searchQuery) {
            this.renderNotes();
            return;
        }

        const filteredNotes = this.notes.filter(note =>
            note.title.toLowerCase().includes(searchQuery) ||
            note.content.toLowerCase().includes(searchQuery)
        );

        this.renderNotes(filteredNotes);
    }

    renderNotes(notesToRender = this.notes) {
        this.notesContainer.innerHTML = '';

        if (notesToRender.length === 0) {
            this.emptyState.style.display = 'block';
            this.notesContainer.style.display = 'none';
        } else {
            this.emptyState.style.display = 'none';
            this.notesContainer.style.display = 'grid';

            notesToRender.forEach(note => {
                const noteCard = document.createElement('div');
                noteCard.className = 'note-card';
                noteCard.addEventListener('click', () => this.openModal(note.id));

                const noteTitle = note.title || 'Untitled';
                const notePreview = note.content.substring(0, 150) + (note.content.length > 150 ? '...' : '');
                const formattedDate = this.formatDate(note.updatedAt);

                noteCard.innerHTML = `
                    <h3>${this.escapeHtml(noteTitle)}</h3>
                    <p>${this.escapeHtml(notePreview)}</p>
                    <span class="note-date">${formattedDate}</span>
                `;

                this.notesContainer.appendChild(noteCard);
            });
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new NotesApp();
});

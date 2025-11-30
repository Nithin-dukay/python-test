"""
Notes Application GUI
Tkinter-based graphical user interface for the note-taking application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from typing import Optional
from datetime import datetime
from note_manager import NoteManager
from note import Note


class NotesApp:
    """
    Main application window for the note-taking app.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the application.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("Notes Application")
        self.root.geometry("1000x700")
        
        # Initialize note manager
        self.note_manager = NoteManager()
        self.current_note: Optional[Note] = None
        
        # Configure style
        self.setup_styles()
        
        # Create UI components
        self.create_widgets()
        
        # Load initial notes
        self.refresh_notes_list()
        
        # Bind keyboard shortcuts
        self.setup_shortcuts()
    
    def setup_styles(self):
        """Configure ttk styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
    
    def create_widgets(self):
        """Create and layout all UI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left panel - Notes list
        self.create_left_panel(main_frame)
        
        # Right panel - Note editor
        self.create_right_panel(main_frame)
        
        # Status bar
        self.create_status_bar()
    
    def create_left_panel(self, parent):
        """Create the left panel with notes list and search."""
        left_frame = ttk.Frame(parent, padding="5")
        left_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(2, weight=1)
        
        # Search section
        search_label = ttk.Label(left_frame, text="Search Notes:", font=('Arial', 10, 'bold'))
        search_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.on_search())
        search_entry = ttk.Entry(left_frame, textvariable=self.search_var, width=30)
        search_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Notes list
        list_label = ttk.Label(left_frame, text="All Notes:", font=('Arial', 10, 'bold'))
        list_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        # Listbox with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.notes_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                        font=('Arial', 10), width=35, height=25)
        self.notes_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.notes_listbox.yview)
        
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        new_btn = ttk.Button(button_frame, text="New Note", command=self.new_note,
                            style='Accent.TButton')
        new_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_btn = ttk.Button(button_frame, text="Delete", command=self.delete_note)
        delete_btn.pack(side=tk.LEFT)
    
    def create_right_panel(self, parent):
        """Create the right panel with note editor."""
        right_frame = ttk.Frame(parent, padding="5")
        right_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(4, weight=1)
        
        # Toolbar
        toolbar = ttk.Frame(right_frame)
        toolbar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        save_btn = ttk.Button(toolbar, text="Save", command=self.save_note,
                             style='Accent.TButton')
        save_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        export_btn = ttk.Button(toolbar, text="Export Note", command=self.export_current_note)
        export_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        export_all_btn = ttk.Button(toolbar, text="Export All", command=self.export_all_notes)
        export_all_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        stats_btn = ttk.Button(toolbar, text="Statistics", command=self.show_statistics)
        stats_btn.pack(side=tk.LEFT)
        
        # Title
        title_label = ttk.Label(right_frame, text="Title:", font=('Arial', 10, 'bold'))
        title_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.title_entry = ttk.Entry(right_frame, font=('Arial', 12))
        self.title_entry.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Tags
        tags_label = ttk.Label(right_frame, text="Tags (comma-separated):", 
                              font=('Arial', 10, 'bold'))
        tags_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        self.tags_entry = ttk.Entry(right_frame, font=('Arial', 10))
        self.tags_entry.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Content
        content_label = ttk.Label(right_frame, text="Content:", font=('Arial', 10, 'bold'))
        content_label.grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        
        self.content_text = scrolledtext.ScrolledText(right_frame, font=('Arial', 11),
                                                      wrap=tk.WORD, width=60, height=25)
        self.content_text.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Metadata
        self.metadata_label = ttk.Label(right_frame, text="", font=('Arial', 9),
                                       foreground='#666')
        self.metadata_label.grid(row=7, column=0, sticky=tk.W, pady=(10, 0))
    
    def create_status_bar(self):
        """Create the status bar at the bottom."""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = ttk.Label(self.root, textvariable=self.status_var,
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        self.root.bind('<Control-n>', lambda e: self.new_note())
        self.root.bind('<Control-s>', lambda e: self.save_note())
        self.root.bind('<Control-f>', lambda e: self.search_var.get())
    
    def refresh_notes_list(self, search_query: str = ""):
        """
        Refresh the notes list display.
        
        Args:
            search_query: Optional search query to filter notes
        """
        self.notes_listbox.delete(0, tk.END)
        
        if search_query:
            notes = self.note_manager.search_notes(search_query)
        else:
            notes = self.note_manager.get_all_notes()
        
        for note in notes:
            display_text = note.title if note.title else "Untitled"
            if note.tags:
                display_text += f" [{', '.join(note.tags[:2])}]"
            self.notes_listbox.insert(tk.END, display_text)
            # Store note ID as a reference
            self.notes_listbox.itemconfig(tk.END, {'fg': 'black'})
        
        # Store notes for reference
        self.displayed_notes = notes
        
        self.update_status(f"Showing {len(notes)} note(s)")
    
    def on_search(self):
        """Handle search input changes."""
        query = self.search_var.get()
        self.refresh_notes_list(query)
    
    def on_note_select(self, event):
        """Handle note selection from the list."""
        selection = self.notes_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index < len(self.displayed_notes):
            self.load_note(self.displayed_notes[index])
    
    def load_note(self, note: Note):
        """
        Load a note into the editor.
        
        Args:
            note: The Note instance to load
        """
        self.current_note = note
        
        # Clear and populate fields
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note.title)
        
        self.tags_entry.delete(0, tk.END)
        self.tags_entry.insert(0, ', '.join(note.tags))
        
        self.content_text.delete('1.0', tk.END)
        self.content_text.insert('1.0', note.content)
        
        # Update metadata
        created = datetime.fromisoformat(note.created_at).strftime('%Y-%m-%d %H:%M')
        modified = datetime.fromisoformat(note.modified_at).strftime('%Y-%m-%d %H:%M')
        self.metadata_label.config(text=f"Created: {created} | Modified: {modified}")
        
        self.update_status(f"Loaded: {note.title}")
    
    def new_note(self):
        """Create a new note."""
        note = self.note_manager.create_note(title="Untitled", content="")
        self.refresh_notes_list()
        self.load_note(note)
        self.title_entry.focus()
        self.update_status("New note created")
    
    def save_note(self):
        """Save the current note."""
        if not self.current_note:
            messagebox.showwarning("No Note", "Please select or create a note first.")
            return
        
        title = self.title_entry.get().strip()
        content = self.content_text.get('1.0', tk.END).strip()
        tags_text = self.tags_entry.get().strip()
        tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
        
        if not title:
            title = "Untitled"
        
        success = self.note_manager.update_note(
            self.current_note.id,
            title=title,
            content=content,
            tags=tags
        )
        
        if success:
            self.refresh_notes_list(self.search_var.get())
            self.load_note(self.current_note)  # Refresh metadata
            self.update_status("Note saved successfully")
        else:
            messagebox.showerror("Error", "Failed to save note")
    
    def delete_note(self):
        """Delete the selected note."""
        selection = self.notes_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a note to delete.")
            return
        
        index = selection[0]
        note = self.displayed_notes[index]
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{note.title}'?"
        )
        
        if confirm:
            success = self.note_manager.delete_note(note.id)
            if success:
                self.refresh_notes_list(self.search_var.get())
                self.clear_editor()
                self.update_status("Note deleted")
            else:
                messagebox.showerror("Error", "Failed to delete note")
    
    def clear_editor(self):
        """Clear the note editor."""
        self.current_note = None
        self.title_entry.delete(0, tk.END)
        self.tags_entry.delete(0, tk.END)
        self.content_text.delete('1.0', tk.END)
        self.metadata_label.config(text="")
    
    def export_current_note(self):
        """Export the current note to a text file."""
        if not self.current_note:
            messagebox.showwarning("No Note", "Please select a note to export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"{self.current_note.title}.txt"
        )
        
        if file_path:
            success = self.note_manager.export_note(self.current_note.id, file_path)
            if success:
                messagebox.showinfo("Success", f"Note exported to {file_path}")
                self.update_status("Note exported")
            else:
                messagebox.showerror("Error", "Failed to export note")
    
    def export_all_notes(self):
        """Export all notes to a directory."""
        directory = filedialog.askdirectory(title="Select Export Directory")
        
        if directory:
            count = self.note_manager.export_all_notes(directory)
            messagebox.showinfo("Success", f"Exported {count} note(s) to {directory}")
            self.update_status(f"Exported {count} note(s)")
    
    def show_statistics(self):
        """Display statistics about the notes collection."""
        stats = self.note_manager.get_statistics()
        
        message = f"""Notes Statistics:
        
Total Notes: {stats['total_notes']}
Total Tags: {stats['total_tags']}
Total Characters: {stats['total_characters']:,}
Average Note Length: {stats['average_length']:,} characters
        """
        
        messagebox.showinfo("Statistics", message)
    
    def update_status(self, message: str):
        """
        Update the status bar message.
        
        Args:
            message: Status message to display
        """
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = NotesApp(root)
    app.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Notes CLI - Interactive Command Line Interface for Note Taking
Provides a user-friendly menu-driven interface for managing notes.
"""

import sys
import os
from typing import Optional
from datetime import datetime
from notes_manager import NotesManager, Note


class NotesCLI:
    """
    Command-line interface for the notes application.
    """
    
    def __init__(self):
        """Initialize the CLI with a NotesManager instance."""
        try:
            self.manager = NotesManager()
            self.running = True
        except Exception as e:
            print(f"❌ Error initializing notes manager: {e}")
            sys.exit(1)
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self, title: str):
        """
        Print a formatted header.
        
        Args:
            title: Header title text
        """
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)
    
    def print_separator(self):
        """Print a separator line."""
        print("-" * 70)
    
    def format_datetime(self, iso_string: str) -> str:
        """
        Format ISO datetime string to readable format.
        
        Args:
            iso_string: ISO format datetime string
            
        Returns:
            Formatted datetime string
        """
        try:
            dt = datetime.fromisoformat(iso_string)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return iso_string
    
    def get_input(self, prompt: str, allow_empty: bool = False) -> Optional[str]:
        """
        Get user input with validation.
        
        Args:
            prompt: Input prompt text
            allow_empty: Whether to allow empty input
            
        Returns:
            User input string or None if empty and not allowed
        """
        while True:
            user_input = input(prompt).strip()
            if user_input or allow_empty:
                return user_input if user_input else None
            print("⚠️  Input cannot be empty. Please try again.")
    
    def get_multiline_input(self, prompt: str) -> str:
        """
        Get multi-line input from user.
        
        Args:
            prompt: Input prompt text
            
        Returns:
            Multi-line input as a single string
        """
        print(prompt)
        print("(Enter a line with just '.' to finish, or Ctrl+D)")
        lines = []
        
        try:
            while True:
                line = input()
                if line == '.':
                    break
                lines.append(line)
        except EOFError:
            pass
        
        return '\n'.join(lines)
    
    def confirm_action(self, prompt: str) -> bool:
        """
        Ask user for confirmation.
        
        Args:
            prompt: Confirmation prompt text
            
        Returns:
            True if user confirms, False otherwise
        """
        response = input(f"{prompt} (y/n): ").strip().lower()
        return response in ('y', 'yes')
    
    def display_note_summary(self, note: Note, index: Optional[int] = None):
        """
        Display a summary of a note.
        
        Args:
            note: Note instance to display
            index: Optional index number for listing
        """
        prefix = f"{index}. " if index is not None else ""
        created = self.format_datetime(note.created_at)
        
        # Truncate title if too long
        title = note.title if len(note.title) <= 50 else note.title[:47] + "..."
        
        # Show tags if present
        tags_str = f" [{', '.join(note.tags)}]" if note.tags else ""
        
        print(f"{prefix}📝 {title}{tags_str}")
        print(f"   ID: {note.id[:8]}... | Created: {created}")
    
    def display_note_details(self, note: Note):
        """
        Display full details of a note.
        
        Args:
            note: Note instance to display
        """
        self.print_header(f"📝 {note.title}")
        print(f"ID: {note.id}")
        print(f"Created: {self.format_datetime(note.created_at)}")
        print(f"Updated: {self.format_datetime(note.updated_at)}")
        
        if note.tags:
            print(f"Tags: {', '.join(note.tags)}")
        
        self.print_separator()
        print(note.content)
        self.print_separator()
    
    def create_note(self):
        """Create a new note interactively."""
        self.print_header("📝 Create New Note")
        
        title = self.get_input("Enter note title: ")
        if not title:
            print("❌ Note creation cancelled.")
            return
        
        print("\nEnter note content:")
        content = self.get_multiline_input("")
        
        if not content or not content.strip():
            print("❌ Note content cannot be empty. Note creation cancelled.")
            return
        
        # Optional tags
        tags_input = self.get_input("Enter tags (comma-separated, optional): ", allow_empty=True)
        tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
        
        try:
            note = self.manager.create_note(title, content, tags)
            print(f"\n✅ Note created successfully!")
            print(f"   ID: {note.id[:8]}...")
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Failed to create note: {e}")
    
    def list_notes(self):
        """List all notes."""
        self.print_header("📚 All Notes")
        
        notes = self.manager.get_all_notes()
        
        if not notes:
            print("No notes found. Create your first note!")
            return
        
        print(f"\nTotal notes: {len(notes)}\n")
        
        for idx, note in enumerate(notes, 1):
            self.display_note_summary(note, idx)
            print()
    
    def view_note(self):
        """View a specific note by ID."""
        self.print_header("👁️  View Note")
        
        notes = self.manager.get_all_notes()
        if not notes:
            print("No notes available.")
            return
        
        # Show list for reference
        print("\nAvailable notes:")
        for idx, note in enumerate(notes, 1):
            print(f"{idx}. {note.title} (ID: {note.id[:8]}...)")
        
        print()
        note_input = self.get_input("Enter note number or ID: ")
        
        # Try to parse as number first
        note = None
        try:
            note_num = int(note_input)
            if 1 <= note_num <= len(notes):
                note = notes[note_num - 1]
        except ValueError:
            # Try as ID
            note = self.manager.get_note(note_input)
            if not note:
                # Try partial ID match
                for n in notes:
                    if n.id.startswith(note_input):
                        note = n
                        break
        
        if note:
            print()
            self.display_note_details(note)
        else:
            print("❌ Note not found.")
    
    def edit_note(self):
        """Edit an existing note."""
        self.print_header("✏️  Edit Note")
        
        notes = self.manager.get_all_notes()
        if not notes:
            print("No notes available.")
            return
        
        # Show list for reference
        print("\nAvailable notes:")
        for idx, note in enumerate(notes, 1):
            print(f"{idx}. {note.title} (ID: {note.id[:8]}...)")
        
        print()
        note_input = self.get_input("Enter note number or ID to edit: ")
        
        # Find note
        note = None
        try:
            note_num = int(note_input)
            if 1 <= note_num <= len(notes):
                note = notes[note_num - 1]
        except ValueError:
            note = self.manager.get_note(note_input)
            if not note:
                for n in notes:
                    if n.id.startswith(note_input):
                        note = n
                        break
        
        if not note:
            print("❌ Note not found.")
            return
        
        # Show current note
        print("\nCurrent note:")
        self.display_note_details(note)
        
        print("\n(Press Enter to keep current value)")
        
        # Get new values
        new_title = self.get_input(f"New title [{note.title}]: ", allow_empty=True)
        
        print("\nNew content (current content will be replaced):")
        print("Press Enter twice to keep current content, or start typing:")
        new_content = self.get_multiline_input("")
        
        new_tags_input = self.get_input(
            f"New tags [{', '.join(note.tags) if note.tags else 'none'}]: ",
            allow_empty=True
        )
        new_tags = [tag.strip() for tag in new_tags_input.split(',')] if new_tags_input else None
        
        # Update note
        try:
            updated = self.manager.update_note(
                note.id,
                title=new_title if new_title else None,
                content=new_content if new_content.strip() else None,
                tags=new_tags
            )
            
            if updated:
                print("\n✅ Note updated successfully!")
            else:
                print("❌ Failed to update note.")
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Failed to update note: {e}")
    
    def delete_note(self):
        """Delete a note."""
        self.print_header("🗑️  Delete Note")
        
        notes = self.manager.get_all_notes()
        if not notes:
            print("No notes available.")
            return
        
        # Show list for reference
        print("\nAvailable notes:")
        for idx, note in enumerate(notes, 1):
            print(f"{idx}. {note.title} (ID: {note.id[:8]}...)")
        
        print()
        note_input = self.get_input("Enter note number or ID to delete: ")
        
        # Find note
        note = None
        try:
            note_num = int(note_input)
            if 1 <= note_num <= len(notes):
                note = notes[note_num - 1]
        except ValueError:
            note = self.manager.get_note(note_input)
            if not note:
                for n in notes:
                    if n.id.startswith(note_input):
                        note = n
                        break
        
        if not note:
            print("❌ Note not found.")
            return
        
        # Show note and confirm
        print("\nNote to delete:")
        self.display_note_summary(note)
        print()
        
        if self.confirm_action("⚠️  Are you sure you want to delete this note?"):
            if self.manager.delete_note(note.id):
                print("✅ Note deleted successfully!")
            else:
                print("❌ Failed to delete note.")
        else:
            print("Deletion cancelled.")
    
    def search_notes(self):
        """Search for notes."""
        self.print_header("🔍 Search Notes")
        
        query = self.get_input("Enter search query: ")
        if not query:
            print("Search cancelled.")
            return
        
        print("\nSearch in:")
        print("1. Title only")
        print("2. Content only")
        print("3. Both title and content")
        print("4. Tags")
        
        choice = self.get_input("Choose option (1-4) [3]: ", allow_empty=True) or "3"
        
        search_map = {
            '1': 'title',
            '2': 'content',
            '3': 'both',
            '4': 'tags'
        }
        
        search_in = search_map.get(choice, 'both')
        results = self.manager.search_notes(query, search_in)
        
        print(f"\n🔍 Found {len(results)} note(s):\n")
        
        if results:
            for idx, note in enumerate(results, 1):
                self.display_note_summary(note, idx)
                print()
        else:
            print("No notes found matching your query.")
    
    def export_note(self):
        """Export a note to a text file."""
        self.print_header("💾 Export Note")
        
        notes = self.manager.get_all_notes()
        if not notes:
            print("No notes available.")
            return
        
        # Show list for reference
        print("\nAvailable notes:")
        for idx, note in enumerate(notes, 1):
            print(f"{idx}. {note.title} (ID: {note.id[:8]}...)")
        
        print()
        note_input = self.get_input("Enter note number or ID to export: ")
        
        # Find note
        note = None
        try:
            note_num = int(note_input)
            if 1 <= note_num <= len(notes):
                note = notes[note_num - 1]
        except ValueError:
            note = self.manager.get_note(note_input)
            if not note:
                for n in notes:
                    if n.id.startswith(note_input):
                        note = n
                        break
        
        if not note:
            print("❌ Note not found.")
            return
        
        try:
            filepath = self.manager.export_note(note.id)
            if filepath:
                print(f"✅ Note exported successfully to: {filepath}")
            else:
                print("❌ Failed to export note.")
        except Exception as e:
            print(f"❌ Error exporting note: {e}")
    
    def show_statistics(self):
        """Display statistics about notes."""
        self.print_header("📊 Notes Statistics")
        
        stats = self.manager.get_statistics()
        
        print(f"\n📝 Total Notes: {stats['total_notes']}")
        print(f"🏷️  Total Tags: {stats['total_tags']}")
        print(f"📏 Total Characters: {stats['total_characters']:,}")
        print(f"📐 Average Note Length: {stats['average_note_length']:,} characters")
        
        if stats['unique_tags']:
            print(f"\n🏷️  Tags: {', '.join(stats['unique_tags'])}")
    
    def display_menu(self):
        """Display the main menu."""
        self.print_header("📓 Notes Application")
        print("\n1.  📝 Create new note")
        print("2.  📚 List all notes")
        print("3.  👁️  View note")
        print("4.  ✏️  Edit note")
        print("5.  🗑️  Delete note")
        print("6.  🔍 Search notes")
        print("7.  💾 Export note")
        print("8.  📊 Show statistics")
        print("9.  ❌ Exit")
        print()
    
    def run(self):
        """Run the main CLI loop."""
        print("\n🎉 Welcome to Notes Application!")
        
        while self.running:
            self.display_menu()
            choice = self.get_input("Choose an option (1-9): ", allow_empty=True)
            
            print()
            
            if choice == '1':
                self.create_note()
            elif choice == '2':
                self.list_notes()
            elif choice == '3':
                self.view_note()
            elif choice == '4':
                self.edit_note()
            elif choice == '5':
                self.delete_note()
            elif choice == '6':
                self.search_notes()
            elif choice == '7':
                self.export_note()
            elif choice == '8':
                self.show_statistics()
            elif choice == '9':
                print("👋 Thank you for using Notes Application!")
                self.running = False
            else:
                print("⚠️  Invalid option. Please choose 1-9.")
            
            if self.running:
                input("\nPress Enter to continue...")


def main():
    """Main entry point for the CLI application."""
    try:
        cli = NotesCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

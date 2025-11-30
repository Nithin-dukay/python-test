#!/usr/bin/env python3
"""
Demo script for the Notes Application
Demonstrates the key features of the notes manager.
"""

from notes_manager import NotesManager


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def main():
    """Run the demo."""
    print("\n🎉 Welcome to the Notes Application Demo!")
    
    # Initialize manager
    print_header("1. Initializing Notes Manager")
    manager = NotesManager()
    print("✅ Notes manager initialized")
    print(f"   Data directory: {manager.data_dir}")
    print(f"   Data file: {manager.filepath}")
    
    # Show existing notes
    print_header("2. Listing Existing Notes")
    notes = manager.get_all_notes()
    print(f"📚 Found {len(notes)} existing note(s):\n")
    for idx, note in enumerate(notes, 1):
        print(f"{idx}. {note.title}")
        print(f"   Tags: {', '.join(note.tags) if note.tags else 'none'}")
        print(f"   Created: {note.created_at}")
        print()
    
    # Search demonstration
    print_header("3. Search Demonstration")
    query = "python"
    print(f"🔍 Searching for '{query}'...")
    results = manager.search_notes(query)
    print(f"✅ Found {len(results)} note(s) matching '{query}'")
    for note in results:
        print(f"   - {note.title}")
    
    # Filter by tags
    print_header("4. Filter by Tags")
    tag = "programming"
    print(f"🏷️  Filtering notes with tag '{tag}'...")
    results = manager.filter_by_tags([tag])
    print(f"✅ Found {len(results)} note(s) with tag '{tag}'")
    for note in results:
        print(f"   - {note.title}")
    
    # Statistics
    print_header("5. Notes Statistics")
    stats = manager.get_statistics()
    print(f"📊 Collection Statistics:")
    print(f"   Total Notes: {stats['total_notes']}")
    print(f"   Unique Tags: {stats['total_tags']}")
    print(f"   Total Characters: {stats['total_characters']:,}")
    print(f"   Average Note Length: {stats['average_note_length']:,} characters")
    if stats['unique_tags']:
        print(f"\n   Available Tags:")
        for tag in stats['unique_tags']:
            print(f"      - {tag}")
    
    # Export demonstration
    if notes:
        print_header("6. Export Demonstration")
        note = notes[0]
        print(f"💾 Exporting note: '{note.title}'...")
        filepath = manager.export_note(note.id)
        print(f"✅ Note exported to: {filepath}")
    
    # Summary
    print_header("Demo Complete!")
    print("\n📝 To use the interactive CLI application, run:")
    print("   python3 notes_cli.py")
    print("\n📖 For more information, see README_NOTES.md")
    print("\n✨ Key Features:")
    print("   • Create, read, update, delete notes")
    print("   • Search by title, content, or tags")
    print("   • Export notes to text files")
    print("   • Persistent JSON storage")
    print("   • Comprehensive error handling")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

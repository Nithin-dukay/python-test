#!/usr/bin/env python3
"""
Test script for the Notes Application
Tests all core functionality without GUI.
"""

import os
import json
from note import Note
from note_manager import NoteManager


def test_note_creation():
    """Test creating notes."""
    print("Testing Note Creation...")
    note = Note(title="Test Note", content="This is a test note", tags=["test", "demo"])
    assert note.title == "Test Note"
    assert note.content == "This is a test note"
    assert "test" in note.tags
    assert note.id is not None
    print("✓ Note creation successful")


def test_note_update():
    """Test updating notes."""
    print("\nTesting Note Update...")
    note = Note(title="Original", content="Original content")
    original_modified = note.modified_at
    
    import time
    time.sleep(0.1)  # Small delay to ensure timestamp changes
    
    note.update(title="Updated", content="Updated content")
    assert note.title == "Updated"
    assert note.content == "Updated content"
    assert note.modified_at != original_modified
    print("✓ Note update successful")


def test_note_serialization():
    """Test note serialization and deserialization."""
    print("\nTesting Note Serialization...")
    note = Note(title="Serialize Test", content="Content", tags=["tag1", "tag2"])
    
    # Convert to dict
    note_dict = note.to_dict()
    assert note_dict['title'] == "Serialize Test"
    assert note_dict['tags'] == ["tag1", "tag2"]
    
    # Convert back to Note
    restored_note = Note.from_dict(note_dict)
    assert restored_note.title == note.title
    assert restored_note.content == note.content
    assert restored_note.tags == note.tags
    print("✓ Note serialization successful")


def test_note_search():
    """Test note search functionality."""
    print("\nTesting Note Search...")
    note = Note(title="Python Tutorial", content="Learn Python programming", tags=["python", "tutorial"])
    
    assert note.matches_search("python")
    assert note.matches_search("Tutorial")
    assert note.matches_search("programming")
    assert note.matches_search("tutorial")
    assert not note.matches_search("javascript")
    print("✓ Note search successful")


def test_note_manager():
    """Test NoteManager functionality."""
    print("\nTesting NoteManager...")
    
    # Use a test data file
    test_file = "test_notes_data.json"
    if os.path.exists(test_file):
        os.remove(test_file)
    
    manager = NoteManager(data_file=test_file)
    
    # Test creating notes
    note1 = manager.create_note(title="First Note", content="First content", tags=["tag1"])
    note2 = manager.create_note(title="Second Note", content="Second content", tags=["tag2"])
    note3 = manager.create_note(title="Python Guide", content="Python is great", tags=["python"])
    
    assert len(manager.get_all_notes()) == 3
    print("✓ Created 3 notes")
    
    # Test retrieving notes
    retrieved = manager.get_note(note1.id)
    assert retrieved.title == "First Note"
    print("✓ Retrieved note by ID")
    
    # Test updating notes
    success = manager.update_note(note1.id, title="Updated First Note")
    assert success
    updated = manager.get_note(note1.id)
    assert updated.title == "Updated First Note"
    print("✓ Updated note")
    
    # Test searching
    results = manager.search_notes("python")
    assert len(results) == 1
    assert results[0].title == "Python Guide"
    print("✓ Search functionality works")
    
    # Test filtering by tag
    results = manager.filter_by_tag("tag1")
    assert len(results) == 1
    print("✓ Tag filtering works")
    
    # Test getting all tags
    all_tags = manager.get_all_tags()
    assert "python" in all_tags
    assert "tag1" in all_tags
    print("✓ Get all tags works")
    
    # Test statistics
    stats = manager.get_statistics()
    assert stats['total_notes'] == 3
    assert stats['total_tags'] == 3
    print("✓ Statistics work")
    
    # Test export
    export_file = "test_export.txt"
    success = manager.export_note(note1.id, export_file)
    assert success
    assert os.path.exists(export_file)
    print("✓ Export single note works")
    
    # Test export all
    export_dir = "test_exports"
    count = manager.export_all_notes(export_dir)
    assert count == 3
    assert os.path.exists(export_dir)
    print("✓ Export all notes works")
    
    # Test deleting notes
    success = manager.delete_note(note2.id)
    assert success
    assert len(manager.get_all_notes()) == 2
    print("✓ Delete note works")
    
    # Test persistence
    manager2 = NoteManager(data_file=test_file)
    assert len(manager2.get_all_notes()) == 2
    print("✓ Data persistence works")
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(test_file + ".backup"):
        os.remove(test_file + ".backup")
    if os.path.exists(export_file):
        os.remove(export_file)
    if os.path.exists(export_dir):
        import shutil
        shutil.rmtree(export_dir)
    
    print("✓ All NoteManager tests passed")


def test_data_persistence():
    """Test that data persists across manager instances."""
    print("\nTesting Data Persistence...")
    
    test_file = "test_persistence.json"
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create notes with first manager
    manager1 = NoteManager(data_file=test_file)
    note1 = manager1.create_note(title="Persistent Note", content="This should persist")
    note_id = note1.id
    
    # Create second manager and verify data loaded
    manager2 = NoteManager(data_file=test_file)
    loaded_note = manager2.get_note(note_id)
    
    assert loaded_note is not None
    assert loaded_note.title == "Persistent Note"
    assert loaded_note.content == "This should persist"
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("✓ Data persistence test passed")


def test_error_handling():
    """Test error handling for edge cases."""
    print("\nTesting Error Handling...")
    
    manager = NoteManager(data_file="test_error_handling.json")
    
    # Test updating non-existent note
    success = manager.update_note("non-existent-id", title="Test")
    assert not success
    print("✓ Handles non-existent note update")
    
    # Test deleting non-existent note
    success = manager.delete_note("non-existent-id")
    assert not success
    print("✓ Handles non-existent note deletion")
    
    # Test getting non-existent note
    note = manager.get_note("non-existent-id")
    assert note is None
    print("✓ Handles non-existent note retrieval")
    
    # Cleanup
    if os.path.exists("test_error_handling.json"):
        os.remove("test_error_handling.json")
    
    print("✓ Error handling tests passed")


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("Running Notes Application Tests")
    print("="*60)
    
    try:
        test_note_creation()
        test_note_update()
        test_note_serialization()
        test_note_search()
        test_note_manager()
        test_data_persistence()
        test_error_handling()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        return True
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

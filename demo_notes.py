#!/usr/bin/env python3
"""
Demo script to create sample notes for the Notes Application.
Run this to populate the app with example notes.
"""

from note_manager import NoteManager


def create_demo_notes():
    """Create sample notes to demonstrate the application."""
    print("Creating demo notes...")
    
    manager = NoteManager()
    
    # Sample notes with various content
    notes_data = [
        {
            "title": "Welcome to Notes App",
            "content": """Welcome to your new note-taking application!

This app helps you organize your thoughts, ideas, and information efficiently.

Key Features:
- Create and edit notes easily
- Search across all your notes
- Organize with tags
- Export notes to text files
- Automatic timestamps

Get started by creating your first note!""",
            "tags": ["welcome", "tutorial"]
        },
        {
            "title": "Python Tips",
            "content": """Useful Python Tips:

1. Use list comprehensions for cleaner code
2. F-strings are the best way to format strings
3. Use 'with' statements for file operations
4. Virtual environments keep dependencies isolated
5. Type hints improve code readability

Remember: "Readability counts" - The Zen of Python""",
            "tags": ["python", "programming", "tips"]
        },
        {
            "title": "Project Ideas",
            "content": """Ideas for future projects:

1. Web scraper for news articles
2. Personal finance tracker
3. Habit tracking app
4. Recipe organizer
5. Workout planner
6. Book reading list manager

Pick one and start building!""",
            "tags": ["ideas", "projects", "todo"]
        },
        {
            "title": "Meeting Notes - Nov 30",
            "content": """Team Meeting Notes:

Attendees: Alice, Bob, Charlie

Discussion Points:
- Q4 goals review
- New feature proposals
- Timeline for next release
- Resource allocation

Action Items:
- Alice: Prepare design mockups
- Bob: Review technical requirements
- Charlie: Update project timeline

Next meeting: Dec 7""",
            "tags": ["meeting", "work", "notes"]
        },
        {
            "title": "Book Recommendations",
            "content": """Books to Read:

Fiction:
- "The Midnight Library" by Matt Haig
- "Project Hail Mary" by Andy Weir
- "Klara and the Sun" by Kazuo Ishiguro

Non-Fiction:
- "Atomic Habits" by James Clear
- "Thinking, Fast and Slow" by Daniel Kahneman
- "The Pragmatic Programmer" by Hunt & Thomas

Technical:
- "Clean Code" by Robert Martin
- "Design Patterns" by Gang of Four""",
            "tags": ["books", "reading", "recommendations"]
        },
        {
            "title": "Recipe: Chocolate Chip Cookies",
            "content": """Ingredients:
- 2 1/4 cups all-purpose flour
- 1 tsp baking soda
- 1 tsp salt
- 1 cup butter, softened
- 3/4 cup granulated sugar
- 3/4 cup packed brown sugar
- 2 large eggs
- 2 tsp vanilla extract
- 2 cups chocolate chips

Instructions:
1. Preheat oven to 375°F
2. Mix flour, baking soda, and salt
3. Beat butter and sugars until creamy
4. Add eggs and vanilla
5. Gradually blend in flour mixture
6. Stir in chocolate chips
7. Drop rounded tablespoons onto baking sheets
8. Bake 9-11 minutes

Enjoy!""",
            "tags": ["recipe", "cooking", "dessert"]
        },
        {
            "title": "Workout Routine",
            "content": """Weekly Workout Plan:

Monday: Upper Body
- Push-ups: 3 sets of 15
- Dumbbell rows: 3 sets of 12
- Shoulder press: 3 sets of 10

Wednesday: Lower Body
- Squats: 3 sets of 15
- Lunges: 3 sets of 12 each leg
- Calf raises: 3 sets of 20

Friday: Full Body
- Burpees: 3 sets of 10
- Plank: 3 sets of 60 seconds
- Mountain climbers: 3 sets of 20

Remember to stretch and stay hydrated!""",
            "tags": ["fitness", "workout", "health"]
        },
        {
            "title": "Travel Bucket List",
            "content": """Places to Visit:

Europe:
- Paris, France - Eiffel Tower, Louvre
- Rome, Italy - Colosseum, Vatican
- Barcelona, Spain - Sagrada Familia

Asia:
- Tokyo, Japan - Cherry blossoms, temples
- Bali, Indonesia - Beaches, culture
- Bangkok, Thailand - Street food, temples

Americas:
- New York, USA - Times Square, Central Park
- Rio de Janeiro, Brazil - Christ the Redeemer
- Machu Picchu, Peru - Ancient ruins

Start planning your next adventure!""",
            "tags": ["travel", "bucket-list", "adventure"]
        }
    ]
    
    # Create the notes
    created_count = 0
    for note_data in notes_data:
        manager.create_note(
            title=note_data["title"],
            content=note_data["content"],
            tags=note_data["tags"]
        )
        created_count += 1
        print(f"✓ Created: {note_data['title']}")
    
    print(f"\n✓ Successfully created {created_count} demo notes!")
    print("\nRun 'python3 main.py' to view them in the application.")
    
    # Show statistics
    stats = manager.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total Notes: {stats['total_notes']}")
    print(f"  Total Tags: {stats['total_tags']}")
    print(f"  Total Characters: {stats['total_characters']:,}")


if __name__ == "__main__":
    create_demo_notes()

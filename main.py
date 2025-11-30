#!/usr/bin/env python3
"""
Main Entry Point for Notes Application
Launches the note-taking application with GUI.
"""

import sys
import tkinter as tk
from notes_app import NotesApp


def main():
    """
    Main function to launch the notes application.
    """
    try:
        # Create root window
        root = tk.Tk()
        
        # Set window icon (optional - will use default if not available)
        try:
            # You can add a custom icon here if available
            # root.iconbitmap('icon.ico')
            pass
        except:
            pass
        
        # Create and run the application
        app = NotesApp(root)
        
        # Handle window close event
        def on_closing():
            """Handle application closing."""
            if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start the application
        app.run()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

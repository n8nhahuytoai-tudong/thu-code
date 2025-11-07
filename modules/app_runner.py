"""
Main application runner with browser automation
"""
import sys
from .gui_browser import create_app, create_main_window


def run():
    """
    Main entry point for the application

    Returns:
        int: Exit code
    """
    try:
        # Create Qt application with async support
        app, loop = create_app()

        # Create and show main window
        window = create_main_window()

        # Run async event loop
        with loop:
            loop.run_forever()

        return 0

    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run())

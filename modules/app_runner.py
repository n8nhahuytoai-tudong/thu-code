"""
Main application runner
"""
import sys
from .gui_simple import create_app, create_main_window


def run():
    """
    Main entry point for the application

    Returns:
        int: Exit code
    """
    try:
        # Create Qt application
        app = create_app()

        # Create and show main window
        window = create_main_window()

        # Run event loop
        return app.exec_()

    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run())

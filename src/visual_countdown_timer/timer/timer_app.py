from .display_utils import UserDisplay
from .system_utils import SystemUtils, TerminalUtils
from .timer_utils import TimerLoop, UserInput

"""
Main application coordinator for the Visual Countdown Timer.

This module provides the main TimerApp class that orchestrates all other
components to create the complete countdown timer application.
"""

class TimerApp:
    """Main application coordinator."""
    
    def __init__(self):
        """Initialize the timer application."""
        exit_handler = TerminalUtils.initialize_exit_handler()
        # Change to exit_handler_initialized = TerminalUtils...() where the function returns either True or False

    def run(self):
        """Run the main timer application."""
        TerminalUtils.clear_terminal()
        
        # Get user preferences
        SystemUtils.wrap_text(
            func_name = print,
            text_unformatted=f"{UserDisplay.TITLE_BLOCK}\n{UserDisplay.TIMER_INTRO_TEXT}"
        )
        countdown_minutes = UserInput.get_countdown_time()
        hour_format = UserInput.get_hour_format()
        
        # Start timer loop
        TimerLoop.run(countdown_minutes, hour_format)

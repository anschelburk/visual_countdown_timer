from timer_display_prompts import DisplayWelcomeMessage
from timer_utils import TerminalUtils

"""
# Add docstring to this module.
"""

class TimerApp:

    """
    Main timer application class that coordinates all components.
    """

    def __init__(self):
        TerminalUtils.initialize_exit_handler()

    def run(self):
        DisplayWelcomeMessage()
        # Ask user for timer info.
        # Run timer loop.
        pass

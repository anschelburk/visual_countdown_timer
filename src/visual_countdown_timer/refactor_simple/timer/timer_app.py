from .timer_display_prompts import DisplayForUser
from .timer_utils import TerminalUtils

"""
# Add docstring to this module.
"""

class TimerApp:

    """
    Main timer application class that coordinates all components.
    """

    def __init__(self):
        pass

    def run(self):
        TerminalUtils.clear_terminal_screen()
        DisplayForUser.timer_app_welcome()    # Finish defining this.
        # Ask user for timer info.
        # Run timer loop.

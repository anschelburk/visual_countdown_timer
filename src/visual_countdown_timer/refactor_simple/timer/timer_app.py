from .timer_prompts import TimerPrompts
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
        TimerPrompts.display_timer_introduction()    # Finish defining this.
        # Ask user for timer info.
        # Run timer loop.

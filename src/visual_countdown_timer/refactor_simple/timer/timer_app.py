from timer_display_prompts import UserMessages
from timer_utils import TerminalUtils
# from timer_utils import CoreUtils

"""
Core logic for Visual Countdown Timer app.
"""

class TimerApp:

    """
    Main timer application class that coordinates all components.
    """

    def __init__(self):
        TerminalUtils.initialize_exit_handler()

    def run(self):
        TerminalUtils.clear_terminal_screen()
        UserMessages.timer_app_welcome()
        # UserMessages.get_countdown_times()
        # UserMessages.get_hour_display_format()
        # CoreUtils.timer_countdown_continuous()

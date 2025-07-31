from timer_display_prompts import UserMessages
from timer_utils import TerminalUtils

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
        # TimerActions.get_countdown_times_from_user()
        # TimerActions.get_hour_format_from_user()
        # TimerActions.run_timer_loop()

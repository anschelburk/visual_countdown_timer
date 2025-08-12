from .settings import DisplaySettings
from .system_utils import SystemUtils
import math

"""
Display and output handling for the Visual Countdown Timer.

This module provides classes for formatting and displaying information
to the user, including the timer interface and status messages.
"""

class ProgressBar:
    """Handles creation of visual elements like progress bars."""
    
    @staticmethod
    def create_progress_bar(remaining_time_in_seconds:int) -> str:
        """
        Generates a visual progress bar representing remaining time.
        
        Args:
            remaining_time_in_seconds (int): Remaining time in seconds
            
        Returns:
            progress_bar_text (str): Visual progress bar with '#' and '.' characters
        """
        
        remaining_minutes = remaining_time_in_seconds / 60
        minutes_rounded_up = math.ceil(remaining_minutes)
        
        progress_bar_width_full = round(minutes_rounded_up / 2)
        progress_bar_width_empty = DisplaySettings.PROGRESS_BAR_WIDTH - progress_bar_width_full
        
        progress_bar_full = '#' * progress_bar_width_full
        progress_bar_empty = '.' * progress_bar_width_empty
        
        progress_bar_text = f'[{progress_bar_full}{progress_bar_empty}]'
        return progress_bar_text

class UserDisplay:
    """Handles displaying information to the user."""
    
    # Display formatting constants
    INDENT = ' ' * DisplaySettings.INDENT_LENGTH
    THICK_HORIZONTAL_LINE = "=" * DisplaySettings.LINE_THICKNESS
    THIN_HORIZONTAL_LINE = "-" * DisplaySettings.LINE_THICKNESS
    INDENTED_HORIZONTAL_LINE = {INDENT} + '-' * (DisplaySettings.LINE_THICKNESS - DisplaySettings.INDENT_LENGTH)
    """Handles displaying information to the user."""

    TIMER_INTRO_TEXT = (
        'Welcome to Visual Countdown Timer!\n' +
        'This timer counts down to a set number of minutes past each hour.\n' +
        'For example, if you enter \"25\", it will count down to 1:25, 2:25, etc.\n'
    )

    TITLE_BLOCK = (
        THICK_HORIZONTAL_LINE + '\n' +
        'Visual Countdown Timer\n' +
        'Press Ctrl + C to exit.\n' +
        THICK_HORIZONTAL_LINE
    )
    
    @staticmethod
    def format_time_display(remaining_minutes:int, remaining_seconds:int) -> str:
        """
        Formats the remaining minutes and seconds for display in-app.

        Args:
            remaining_minutes (int): The unformatted number of remaining minutes.
            remaining_seconds (int): The unformatted number of remaining seconds.

        Returns:
            remaining_time_formatted (str): The formatted number of remaining minutes and seconds.
        """

        minutes_label = SystemUtils.pluralize("minute", remaining_minutes)
        seconds_label = SystemUtils.pluralize("second", remaining_seconds)

        remaining_minutes_formatted = f'{UserDisplay.INDENT}{remaining_minutes:02} {minutes_label}'
        remaining_seconds_formatted = f'{UserDisplay.INDENT}{remaining_seconds:02} {seconds_label}'

        remaining_time_formatted = (
            remaining_minutes_formatted + '\n' +
            remaining_seconds_formatted
        )

        return remaining_time_formatted

    @classmethod
    def show_timer_display(cls, current_date, current_time, target_time, remaining_minutes, 
                          remaining_seconds, progress_bar_text):
        """Displays the main timer interface."""

        print(UserDisplay.TITLE_BLOCK)   
        print(current_date)
        print(current_time)
        print(UserDisplay.INDENTED_HORIZONTAL_LINE)
        print(f'Countdown until {target_time}:')
        print(UserDisplay.INDENTED_HORIZONTAL_LINE)
        print(cls.format_time_display(remaining_minutes, remaining_seconds))
        print(progress_bar_text)

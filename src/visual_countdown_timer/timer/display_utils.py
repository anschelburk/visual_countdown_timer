from .settings import DisplaySettings
import math

"""
Display and output handling for the Visual Countdown Timer.

This module provides classes for formatting and displaying information
to the user, including the timer interface and status messages.
"""

class ProgressBar: # Previously 'VisualElements'. Add to all other modules.
    """Handles creation of visual elements like progress bars."""
    
    @staticmethod
    def create_progress_bar(remaining_time_in_seconds):
        """
        Generates a visual progress bar representing remaining time.
        
        Args:
            remaining_time_in_seconds (int): Remaining time in seconds
            
        Returns:
            str: Visual progress bar with '#' and '.' characters
        """
        remaining_minutes_rounded = math.ceil(remaining_time_in_seconds / 60)
        progress_bar_full = '#' * round(remaining_minutes_rounded / 2)
        progress_bar_empty = '.' * (DisplaySettings.PROGRESS_BAR_WIDTH - round(remaining_minutes_rounded / 2))
        return f'[{progress_bar_full}{progress_bar_empty}]'

class UserDisplay:
    """Handles displaying information to the user."""
    
    # Display formatting constants
    INDENT = ' ' * DisplaySettings.INDENT_LENGTH
    THICK_HORIZONTAL_LINE = "=" * DisplaySettings.LINE_THICKNESS
    THIN_HORIZONTAL_LINE = "-" * DisplaySettings.LINE_THICKNESS
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
        THICK_HORIZONTAL_LINE + '\n\n'
    )

    @staticmethod
    def remaining_minutes_formatted(remaining_minutes):
        minutes_label = "minute" if remaining_minutes == 1 else "minutes"
        remaining_minutes_formatted = f'{UserDisplay.INDENT}{remaining_minutes:02} {minutes_label}'
        return remaining_minutes_formatted

    @staticmethod
    def remaining_seconds_formatted(remaining_seconds):
        seconds_label = "second" if remaining_seconds == 1 else "seconds"
        remaining_seconds_formatted = f'{UserDisplay.INDENT}{remaining_seconds:02} {seconds_label}'
        return remaining_seconds_formatted
    
    @staticmethod
    def remaining_time_formatted(unit_of_time:str, remaining_time_unformatted:int) -> str:
        """
        Formats the remaining minutes or seconds for display in-app.

        Args:
            unit_of_time (str): Either "minute" or "second"
            remaining_time_unformatted (int): The number of remaining minutes or seconds

        Returns:
            remaining_time_formatted (str): The formatted number of remaining minutes or seconds.
        """
        if remaining_time_unformatted == 1:
            time_label = unit_of_time[:-1]
        else:
           time_label = unit_of_time
        remaining_time_formatted = f'{UserDisplay.INDENT}{remaining_time_unformatted:02} {time_label}'
        return remaining_time_formatted

    @classmethod
    def show_timer_display(cls, current_date, current_time, target_time, remaining_minutes, 
                          remaining_seconds, progress_bar_text):
        """Displays the main timer interface."""

        print(UserDisplay.TITLE_BLOCK)   
        print(current_date)
        print(f'Current Time: {current_time}\n')
        print(UserDisplay.THIN_HORIZONTAL_LINE)
        print(f'Countdown until {target_time}:')
        print(UserDisplay.THIN_HORIZONTAL_LINE)
        print(cls.remaining_time_formatted("minutes", remaining_minutes))
        print(cls.remaining_time_formatted("seconds", remaining_seconds))
        print(progress_bar_text)

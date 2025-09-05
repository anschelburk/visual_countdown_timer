from .settings import DisplaySettings
import math

"""
Display and output handling for the Visual Countdown Timer.

This module provides classes for formatting and displaying information
to the user, including the timer interface and status messages.
"""

class ProgressBar:
    """Handles creation of visual progress bar in-app."""   
    
    @classmethod
    def render(cls, remaining_time_in_seconds:int) -> str:
        """
        Generates a visual progress bar representing remaining time.
        
        Args:
            remaining_time_in_seconds(int): The total remaining time in seconds to count down.
            
        Returns:
            text_complete (str): Visual progress bar with '#' and '.' characters
        """

        text_remaining, text_elapsed = cls._generate_text(remaining_time_in_seconds)
        text_complete = f'[{text_remaining}{text_elapsed}]'
        return text_complete

    @staticmethod
    def _minutes_rounded_up(remaining_time_in_seconds:int) -> int:
        """
        Calculates remaining minutes (rounded up) from total remaining seconds.

        Args:
            remaining_time_in_seconds(int): The total remaining time in seconds to count down.
        Returns:
            minutes_rounded_up (int): The total number of minutes, rounded up.
        """
        remaining_minutes = remaining_time_in_seconds / 60
        minutes_rounded_up = math.ceil(remaining_minutes)
        return minutes_rounded_up

    @classmethod
    def _text_width(cls, remaining_time_in_seconds:int) -> int:
        """
        Calculates the full and empty portions of the progress bar. These represent:
            Remaining portion: The amount of time that has yet to count down.
            Elapsed portion: The amount of time that has already counted down.

        Args:
            remaining_time_in_seconds(int): The total remaining time in seconds to count down.
        Returns:
            width_remaining (int): The width of the full portion of the progress bar.
            width_elapsed (int): The width of the empty portion of the progress bar.
        """

        minutes_rounded_up = cls._minutes_rounded_up(remaining_time_in_seconds)
        width_remaining = round(minutes_rounded_up / 2)
        width_elapsed = DisplaySettings.PROGRESS_BAR_WIDTH_TOTAL - width_remaining
        return width_remaining, width_elapsed
    
    @classmethod
    def _generate_text(cls, remaining_time_in_seconds: int) -> str:
        """
        Generates the full and empty text of the progress bar.
            Text (remaining time): Represents the amount of time that has yet to count down.
            Text (elapsed time): Represents the amount of time that has already counted down.

        Args:
            remaining_time_in_seconds(int): The total remaining time in seconds to count down.
        Returns:
            text_remaining (str): The portion of the progress bar representing the remaining time to count down.
            text_elapsed (str): The portion of the progress bar representing the elapsed time that has already counted down.
        """
        width_remaining, width_elapsed = cls._text_width(remaining_time_in_seconds)
        text_remaining = '#' * width_remaining
        text_elapsed = '.' * width_elapsed
        return text_remaining, text_elapsed

class UserDisplay:
    """Handles displaying information to the user."""
    
    # Display formatting constants
    INDENT = ' ' * DisplaySettings.INDENT_LENGTH
    INDENTED_HORIZONTAL_LINE = INDENT + '-' * (DisplaySettings.LINE_THICKNESS - DisplaySettings.INDENT_LENGTH)
    THICK_HORIZONTAL_LINE = "=" * DisplaySettings.LINE_THICKNESS
    THIN_HORIZONTAL_LINE = "-" * DisplaySettings.LINE_THICKNESS
    """Handles displaying information to the user."""

    TIMER_INTRO_TEXT = (
        'Welcome to Visual Countdown Timer!\n' +
        'This timer counts down to a set number of minutes past each hour. ' +
        'For example, if you enter \"25\", it will count down to 1:25, 2:25, etc.\n'
    )

    TITLE_BLOCK = (
        THICK_HORIZONTAL_LINE + '\n' +
        'Visual Countdown Timer\n' +
        'Press Ctrl + C to exit.\n' +
        THICK_HORIZONTAL_LINE
    )

    @staticmethod
    def show_timer_display(current_date, current_time, target_time, remaining_time, 
                          progress_bar_text):
        """Displays the main timer interface."""

        timer_display_text = (
            f"{UserDisplay.TITLE_BLOCK}\n" +
            f"{current_date}\n" +
            f"{current_time}\n" +
            f"{UserDisplay.INDENTED_HORIZONTAL_LINE}\n" +
            f"{UserDisplay.INDENT}Countdown until {target_time}:\n" +
            f"{UserDisplay.INDENTED_HORIZONTAL_LINE}\n" +
            f"{remaining_time}\n" +
            f"{UserDisplay.INDENT}{progress_bar_text}"
        )

        return timer_display_text

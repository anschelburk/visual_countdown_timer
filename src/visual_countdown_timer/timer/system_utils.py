from .settings import DisplaySettings, TimerConfig
from datetime import datetime
import os
import signal
import sys
import textwrap
import time

"""
System-level utilities for the Visual Countdown Timer.

This module provides classes for handling system operations like terminal
clearing, timing controls, and text processing utilities.
"""

class SystemUtils:
    """Handles system-level operations like terminal clearing and timing."""
    
    @staticmethod
    def clean_text(unformatted_text: str) -> str:
        """
        Removes leading and trailing spaces and common punctuation from a string.

        Args:
            unformatted_text (str): The string to be cleaned.

        Returns:
            clean_text (str): The cleaned string with specified characters removed from both ends.
        """
        CHARACTERS_TO_REMOVE = " .,\"'"
        unformatted_text_str = str(unformatted_text)
        clean_text = unformatted_text_str.strip(CHARACTERS_TO_REMOVE)
        return clean_text

    @staticmethod
    def pluralize(singular_text: str, count: int) -> str:
        """
        Return singular or plural form of text based on count.
        
        Args:
            singular_text (str): The singular form of the text to pluralize.
            count (int): The number to determine pluralization. Will be converted to int.
        
        Returns:
            str: The singular text if count is 1, otherwise singular text with 's' appended.
            
        Raises:
            ValueError: If count cannot be converted to an integer.
        """
        try:
            count = int(count)
        except ValueError:
            raise ValueError(f"Count must be an integer. Right now, count = {count} of type {type(count)}")

        return singular_text if count == 1 else singular_text + "s"
    
    @staticmethod
    def _format_wrapped_text(text_unformatted: str) -> str:
        """
        Wraps the input text to fit within the current terminal window width.

        Args:
            text_unformatted (str): The text to be wrapped.

        Returns:
            text_wrapped (str): The wrapped text.

        """
        text_wrapped = '\n'.join([textwrap.fill(line, width=DisplaySettings.TERMINAL_WINDOW_WIDTH) for line in text_unformatted.splitlines()])
        return text_wrapped
    
    @classmethod
    def wrap_text(cls, func_name, text_unformatted: str):
        """
        Prints the input text wrapped to fit within the current terminal window width.

        Args:
            text_unformatted (str): The text to be wrapped and printed.

        """
        return func_name(cls._format_wrapped_text(text_unformatted))
    
    @staticmethod
    def sleep_until_next_second(current_time: datetime):
        """
        Pauses execution to align next loop with the next full second.
        
        Calculates fractional time remaining in current second and sleeps
        for that duration to ensure loops run on second boundaries.
        """
        remaining_time_until_next_loop = 1 - (current_time.microsecond / 1_000_000)
        return time.sleep(remaining_time_until_next_loop)
    
class TerminalUtils:

    @staticmethod
    def clear_terminal():
        """Clears the terminal screen."""
        # Use 'clear' if running in a Unix-like shell on Windows
        if 'bash' in os.environ.get('SHELL', '') or os.environ.get('TERM') == 'xterm':
            os.system('clear')
        # Use 'cls' if running in a native Windows terminal
        elif os.name == 'nt':
            os.system('cls')
        # Use 'clear' on macOS, Linux, or other Unix-based environments
        else:
            os.system('clear')

    @staticmethod
    def initialize_exit_handler():
        """Setup graceful shutdown handler for interrupt signals (typically Ctrl+C)."""

        def signal_handler(sig, frame):
            SystemUtils.wrap_text(
                func_name='print',
                text_unformatted="\n\nTimer stopped. Thank you for using Visual Countdown Timer!\n\n"
            )
            sys.exit(TimerConfig.EXIT_SUCCESS)
        signal.signal(signal.SIGINT, signal_handler)

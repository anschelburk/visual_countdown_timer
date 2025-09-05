from .settings import DisplaySettings, TimerConfig
from datetime import datetime
from typing import Any, Callable
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
    def _format_wrapped_text(add_linebreaks: bool, text_unformatted: str) -> str:
        """
        Wraps the input text to fit within the current terminal window width.

        If add_linebreaks is True and the output contains multiple lines, an extra
            blank line is inserted after each line for improved readability.

        Args:
            add_linebreaks (bool): If True, add an extra blank line after each wrapped output line, but
                only if the output is multiline.
            text_unformatted (str): The text to be wrapped.

        Returns:
            wrapped_text (str): The wrapped text.

        """
        lines = [
            textwrap.fill(line, width=DisplaySettings.TERMINAL_WINDOW_WIDTH)
            for line in text_unformatted.splitlines()
        ]
        separator = '\n\n' if add_linebreaks and len(lines) > 1 else '\n'
        wrapped_text = separator.join(lines)
        return wrapped_text
    
    @classmethod
    def wrap_text(cls, func_name: Callable[[str], Any], add_extra_lines: bool, text_unformatted: str) -> Any:
        """
        Wraps and outputs the provided text to fit within the terminal window width,
            using the supplied function (such as `print` or `input`) for display or interaction.

        If add_linebreaks is True and the output contains multiple lines, an extra
            blank line is inserted after each line for improved readability.

        Args:
            func_name (Callable[[str], Any]): A callable that consumes the wrapped string.
                Typically the built-in `print` or `input` function.

            add_linebreaks (bool): If True, add an extra blank line after each wrapped output line, but
                only if the output is multiline.
                
            text_unformatted (str): The text that will be wrapped and then passed to `func_name`.

        Returns:
            Any: The return value from the provided `func_name`.
        """
        text_wrapped = cls._format_wrapped_text(add_extra_lines, text_unformatted)
        if func_name is input and text_unformatted.rstrip('\n').endswith(' '):
            text_wrapped += ' '
        return func_name(text_wrapped)
    
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
                func_name=print,
                text_unformatted="\n\nTimer stopped. Thank you for using Visual Countdown Timer!\n\n"
            )
            sys.exit(TimerConfig.EXIT_SUCCESS)
        signal.signal(signal.SIGINT, signal_handler)

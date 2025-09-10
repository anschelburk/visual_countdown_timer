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
    
    # @staticmethod
    # def _format_wrapped_text(text_unformatted: str, add_linebreaks: bool) -> str:
    #     """
    #     Supporting function for `wrap_text()`.

    #     Wraps each non-empty line of input text to fit the terminal window width. 
        
    #     If `add_extra_lines` is True and any original line exceeds the terminal width, 
    #     an extra blank line is inserted after each wrapped line.

    #     Any leading newlines in `text_unformatted` produce empty strings, which are filtered out before joining,
    #     preventing extra blank lines at the beginning of the output.

    #     Parameters
    #     ----------
    #     add_extra_lines : bool
    #         If True, adds an extra blank line after each output line, but only if any input line's length exceeds the terminal window width.
    #     text_unformatted : str
    #         The input text to be wrapped.

    #     Returns
    #     -------
    #     str
    #         The formatted, wrapped text. Output will not start with an extra blank line due to filtering of empty strings.
    #     """
    #     lines = text_unformatted.splitlines()
    #     should_add_extra = add_linebreaks and any(
    #         len(line) > DisplaySettings.TERMINAL_WINDOW_WIDTH for line in lines
    #     )
    #     wrapped_lines = [
    #         textwrap.fill(line, width=DisplaySettings.TERMINAL_WINDOW_WIDTH)
    #         for line in lines if line.strip() != ''
    #     ]
    #     separator = '\n\n' if should_add_extra else '\n'
    #     return separator.join(wrapped_lines)
    
    # @classmethod
    # # def wrap_text(cls, func_name: Callable[[str], Any], text_unformatted: str, add_linebreaks: bool = True) -> Any:
    # def wrap_text(cls, unformatted_text: str, add_linebreaks: bool = True):
    #     """
    #     Wraps and outputs the provided text to fit within the terminal window width, 
    #     using the supplied function (such as `print` or `input`) for display or interaction.

    #     By default, if any line in the unformatted input exceeds the terminal window width, 
    #     an extra blank line is inserted after each wrapped output line.  This only applies to non-empty lines;
    #     leading blank lines do not generate additional empty output lines.

    #     Parameters
    #     ----------
    #     # func_name : Callable[[str], Any]
    #         # A callable that consumes the wrapped string, typically the built-in `print` or `input` function.
    #     unformatted_text : str
    #         The text that will be wrapped and then passed to `func_name`.
    #     add_extra_lines : bool, optional
    #         If True (default), adds an extra blank line after each wrapped output line, but only if at least one 
    #         line in the input exceeds the terminal window width and requires wrapping. Leading empty lines are filtered.

    #     Returns
    #     -------
    #     wrapped_text : str
    #         The wrapped text
    #     """

    #     wrapped_text = cls._format_wrapped_text(unformatted_text, add_linebreaks)
    #     # if func_name is input and text_unformatted.rstrip('\n').endswith(' '):
    #     if unformatted_text.rstrip('\n').endswith(' '):
    #         wrapped_text += ' '
    #     # return func_name(text_wrapped)
    #     return wrapped_text
    
    @staticmethod
    def wrap_text(unformatted_text: str, add_linebreaks: bool = True) -> str:
        """
        Wraps each non-empty line of input text to fit the terminal window width.

        If `add_linebreaks` is True and any original line exceeds terminal width, an extra blank line
        is inserted after each wrapped line. Leading blank lines do not generate additional output lines.

        Parameters
        ----------
        unformatted_text : str
            The text that will be wrapped and formatted.
        add_linebreaks : bool, optional
            If True (default), adds an extra blank line after each wrapped output line, but only if at least one 
            input line exceeds the terminal window width.

        Returns
        -------
        str
            The wrapped and formatted text. Output will not start with an extra blank line due to filtering empty input rows.
        """

        wrapped_lines = []
        needs_extra_linebreak = False

        for line in unformatted_text.splitlines():
            if line.strip() != '':
                if not needs_extra_linebreak:
                    if len(line) > DisplaySettings.TERMINAL_WINDOW_WIDTH:
                        needs_extra_linebreak = True
                wrapped_lines.append(textwrap.fill(line, width=DisplaySettings.TERMINAL_WINDOW_WIDTH))

        separator = '\n\n' if (add_linebreaks and needs_extra_linebreak) else '\n'
        wrapped_text = separator.join(wrapped_lines)
        if unformatted_text.rstrip('\n').endswith(' '):
            wrapped_text += ' '
        return wrapped_text

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
                func_name = print,
                text_unformatted = "\n\nTimer stopped. Thank you for using Visual Countdown Timer!\n\n"
            )
            sys.exit(TimerConfig.EXIT_SUCCESS)
        signal.signal(signal.SIGINT, signal_handler)

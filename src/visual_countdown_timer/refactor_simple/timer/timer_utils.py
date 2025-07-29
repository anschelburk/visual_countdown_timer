import os
import signal
import sys

"""
# Add docstring for module.
"""

class TerminalUtils:
    """
    # Add docstring for class.
    """

    def __init__(self):
        pass

    @staticmethod
    def  clear_terminal_screen():
        """
        Clears the terminal screen.
        Args: None.
        Returns: None.
        """

        # Use 'clear' if running in a Unix-like shell on Windows (e.g., Git Bash or WSL)
        if 'bash' in os.environ.get('SHELL', '') or os.environ.get('TERM') == 'xterm':
            os.system('clear')

        # Use 'cls' if running in a native Windows terminal (e.g., Command Prompt or PowerShell)
        elif os.name == 'nt':
            os.system('cls')

        # Use 'clear' on macOS, Linux, or another Unix-based environment
        else:
            os.system('clear')

    @staticmethod
    def initialize_exit_handler():
        """Setup graceful shutdown handler for interrupt signals (typically Ctrl+C)."""
        print("initialize_exit_handler() function is running.")
        def signal_handler(sig, frame):
            print("\n\nTimer stopped. Thank you for using Visual Countdown Timer!")
            sys.exit(TimerConfig.EXIT_SUCCESS)
        signal.signal(signal.SIGINT, signal_handler)

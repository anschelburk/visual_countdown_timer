from timer_utils import TerminalUtils

"""
# Add docstring for module.
"""

class TextElements:

    """
    Simple text elements derived from configuration settings.

    All blocks in this class are derived from the base measurements
    defined in DisplaySettings, providing consistent formatting throughout
    the timer application.
    """

    INDENT = DisplaySettings.INDENT_LENGTH * ' '
    THICK_HORIZONTAL_LINE = DisplaySettings.LINE_LENGTH * '='
    THIN_HORIZONTAL_LINE = DisplaySettings.LINE_LENGTH * '-'

class PrintTextBlock:
    """
    Pre-built text blocks built from simpler elements in _TextElements class.

    Contains display strings and formatting blocks that are calculated
    from base configuration values. These are ready-to-use
    blocks of text for building the timer interface, including indentation
    strings and horizontal divider lines.
    """

    @staticmethod
    def timer_title_text():
        print(TextElements.THICK_HORIZONTAL_LINE)
        print('Visual Countdown Timer')
        print('Press Ctrl + C to exit.')
        print(TextElements.THICK_HORIZONTAL_LINE)

    @staticmethod
    def timer_app_introduction():
        print('\nWelcome to Visual Countdown Timer!')
        print('This timer counts down to a set number of minutes past each hour.')
        print('For example, if you enter \"25\", it will count down to 1:25, 2:25, etc.\n')


class DisplayForUser:
    """
    # Add docstring for class.
    """

    def __init__(self):
        pass

    @staticmethod
    def timer_app_welcome():
        """
        Prints the introductory text for the Visual Countdown Timer interface.
        Args: None.
        Returns: None.
        """
        TerminalUtils.clear_terminal_screen()
        TextBlock.timer_title_text()

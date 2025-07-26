from .timer_logic import TimerLogic
from .timer_settings import DisplaySettings
from datetime import datetime

class TextBlocks:                                           # [x] Confirmed
    """
    Pre-built text blocks derived from configuration settings.
    
    Contains display strings and formatting blocks that are calculated
    from base configuration values. These are ready-to-use
    blocks of text for building the timer interface, including indentation
    strings and horizontal divider lines.
    
    All blocks in this class are derived from the base measurements
    defined in DisplaySettings, providing consistent formatting throughout
    the timer application.
    """

    INDENT = ' ' * DisplaySettings.INDENT_LENGTH                 # [x] Confirmed
    THICK_HORIZONTAL_LINE = "=" * DisplaySettings.LINE_LENGTH    # [x] Confirmed
    THIN_HORIZONTAL_LINE = "-" * DisplaySettings.LINE_LENGTH     # [x] Confirmed

class DisplayLogic:
    # Edit the `TimerLogic` portion of this docstring.
    # Edit the first line: "formatting and"
    """
    Handles the logic for formatting and displaying time-related information.

    This class is responsible for taking raw time data and presenting it in a
    user-friendly format, including current time, countdown information, and
    progress bars. It relies on `TimerLogic` for calculations.
    """

class PrintText:
    # Edit this docstring
    """
    Contains static text content and multi-line print statements for the timer display.
    
    This class serves as a centralized repository for all display text,
    including titles, headers, formatted output blocks, and multi-line
    content used throughout the timer application. It separates the
    actual text content from the display logic.
    
    Contains methods that output formatted text blocks, title sections,
    and other pre-defined display elements. This separation allows for
    easy modification of display content without changing the underlying
    display logic.
    """

    @staticmethod                                   # Later on: can I make 'CTRL + C' text dynamic to show user's preference?
    def title_block():                              # [x] Confirmed
        """Prints the title block for the Visual Countdown Timer interface."""
        print(TextBlocks.THICK_HORIZONTAL_LINE)
        print('Visual Countdown Timer')
        print('Press Ctrl + C to exit.')
        print(f'{TextBlocks.THICK_HORIZONTAL_LINE}\n')

class TimerDisplay:
    """Handles all display formatting and output."""
    
    def __init__(self):
        self.timer_logic = TimerLogic()
    
    def format_time(self, datetime_unformatted: datetime, hour_format: int) -> str:
        """
        Format datetime object into 12/24 hour string with timezone.
        
        Args:
            datetime_unformatted (datetime): The raw datetime to format.
            hour_format (int): Either "12" for 12-hour format, or "24" for 24-hour format.
            
        Returns:
            datetime_formatted (datetime): The formatted datetime string
        """

        timezone = datetime_unformatted.astimezone().strftime('%Z')

        try:
            hour_format = int(hour_format)
            if hour_format in DisplaySettings.POSSIBLE_HOUR_DISPLAY_FORMATS:
                if hour_format == 12:
                    hour = datetime_unformatted.strftime('%I:%M').lstrip('0')
                    ampm = datetime_unformatted.strftime('%p').lower()
                    datetime_formatted = f'{hour}{ampm} {timezone}'
                elif hour_format == 24:
                    hour = datetime_unformatted.strftime('%H:%M')
                    datetime_formatted = f'{hour} {timezone}'
                return datetime_formatted
            else:
                raise ValueError
            
        except ValueError:
            print('\nError: Hour format must be either \"12\" or \"24\", written as a whole number.')
            print(f'Right now, hour_format input = {hour_format}')
    
    def show_current_info(self, current_datetime: datetime, hour_format: int):
        """
        Display current date and time information.
        
        Args:
            current_datetime (datetime): The current datetime.
            hour_format (int):  Either "12" for 12-hour format, or "24" for 24-hour format.

        Returns:
            None
        """

        current_date = current_datetime.strftime('%B %d, %Y')
        formatted_time = self.format_time(current_datetime, hour_format)
        
        print(current_date)
        print(f'Current Time: {formatted_time}\n')
    
    @staticmethod                                                      # Come back to this function once I find where it's referenced.
    def show_countdown_info(target_time: datetime, remaining_seconds: int, hour_format: int):
        """Display countdown information including progress bar."""
        formatted_target = self.format_time(target_time, hour_format)
        progress_bar = self.timer_logic.get_progress_bar(remaining_seconds)
        
        remaining_minutes, seconds = divmod(remaining_seconds, 60)
        
        # Proper pluralization
        min_label = "minute" if remaining_minutes == 1 else "minutes"
        sec_label = "second" if seconds == 1 else "seconds"
        
        print(TextBlocks.THIN_HORIZONTAL_LINE)
        print(f'Countdown until {formatted_target}:')
        print(TextBlocks.THIN_HORIZONTAL_LINE)
        print(f'{TextBlocks.INDENT}{remaining_minutes:02} {min_label}')
        print(f'{TextBlocks.INDENT}{seconds:02} {sec_label}')
        print(progress_bar)
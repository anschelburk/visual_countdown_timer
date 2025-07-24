from .constants import INDENT, THIN_HORIZONTAL_LINE, POSSIBLE_HOUR_DISPLAY_FORMATS
from .timer_logic import TimerLogic
from datetime import datetime


class DisplayFormatter:
    """Handles all display formatting and output."""
    
    def __init__(self):
        self.timer_logic = TimerLogic()
    
    def format_time(self, datetime_unformatted: datetime, hour_format: int) -> str:
        """
        Format datetime object into 12/24 hour string with timezone.
        
        Args:
            datetime_unformatted: Datetime to format
            hour_format: 12 or 24 hour format
            
        Returns:
            Formatted time string
        """

        timezone = datetime_unformatted.astimezone().strftime('%Z')

        try:
            hour_format = int(hour_format)
            if hour_format in POSSIBLE_HOUR_DISPLAY_FORMATS:
                if hour_format == 12:
                    hour = datetime_unformatted.strftime('%I:%M').lstrip('0')
                    ampm = datetime_unformatted.strftime('%p').lower()
                    return f'{hour}{ampm} {timezone}'
                elif hour_format == 24:
                    hour = datetime_unformatted.strftime('%H:%M')
                    return f'{hour} {timezone}'
            else:
                raise ValueError
            
        except ValueError:
            print('\nError: Hour format must be either \"12\" or \"24\", written as a whole number.')
            print(f'Right now, hour_format input = {hour_format}')
    
    def show_current_info(self, current_time: datetime, hour_format: int):
        """Display current date and time information."""
        current_date = current_time.strftime('%B %d, %Y')
        formatted_time = self.format_time(current_time, hour_format)
        
        print(current_date)
        print(f'Current Time: {formatted_time}')
        print()
    
    def show_countdown_info(self, target_time: datetime, remaining_seconds: int, hour_format: int):
        """Display countdown information including progress bar."""
        formatted_target = self.format_time(target_time, hour_format)
        progress_bar = self.timer_logic.get_progress_bar(remaining_seconds)
        
        remaining_minutes, seconds = divmod(remaining_seconds, 60)
        
        # Proper pluralization
        min_label = "minute" if remaining_minutes == 1 else "minutes"
        sec_label = "second" if seconds == 1 else "seconds"
        
        print(THIN_HORIZONTAL_LINE)
        print(f'Countdown until {formatted_target}:')
        print(THIN_HORIZONTAL_LINE)
        print(f'{INDENT}{remaining_minutes:02} {min_label}')
        print(f'{INDENT}{seconds:02} {sec_label}')
        print(progress_bar)
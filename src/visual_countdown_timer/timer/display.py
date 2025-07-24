from .constants import INDENT, THIN_HORIZONTAL_LINE
from .timer_logic import TimerLogic
from datetime import datetime


class DisplayFormatter:
    """Handles all display formatting and output."""
    
    def __init__(self):
        self.timer_logic = TimerLogic()
    
    def format_time(self, time_obj: datetime, hour_format: int) -> str:
        """
        Format datetime object into 12/24 hour string with timezone.
        
        Args:
            time_obj: Datetime to format
            hour_format: 12 or 24 hour format
            
        Returns:
            Formatted time string
        """
        if hour_format not in (12, 24):
            raise ValueError('Hour format must be 12 or 24')
        
        timezone = time_obj.astimezone().strftime('%Z')
        
        if hour_format == 12:
            time_str = time_obj.strftime('%I:%M').lstrip('0')
            ampm = time_obj.strftime('%p').lower()
            return f'{time_str}{ampm} {timezone}'
        else:
            time_str = time_obj.strftime('%H:%M')
            return f'{time_str} {timezone}'
    
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
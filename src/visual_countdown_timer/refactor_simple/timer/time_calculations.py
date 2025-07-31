from datetime import datetime, timedelta
from .constants import TimerConfig

from datetime import datetime, timedelta

class TimeCalculations:
    """Handles all time-related calculations and formatting."""
    
    @staticmethod
    def get_next_occurrence(target_minute, current_datetime):
        """
        Returns the next datetime where the minute equals target_minute.
        
        Args:
            target_minute (int): The target minute after the hour
            current_datetime (datetime): The current date and time
            
        Returns:
            next_occurrence (datetime): The next datetime where minute equals target_minute
        """
        if current_datetime.minute < target_minute:
            next_occurrence = current_datetime.replace(minute=target_minute, second=0, microsecond=0)
        else:
            next_hour = current_datetime + timedelta(hours=1)
            next_occurrence = next_hour.replace(minute=target_minute, second=0, microsecond=0)
        
        return next_occurrence
    
    @staticmethod
    def get_remaining_seconds(end_time, current_datetime):
        """
        Calculates total remaining seconds until end_time.
        
        Args:
            end_time (datetime): Target end time
            current_datetime (datetime): Current time
            
        Returns:
            int: Total remaining seconds
        """
        remaining_time = end_time - current_datetime
        return int(remaining_time.total_seconds())
    
    @staticmethod
    def format_time(unformatted_time, hour_display_format):
        """
        Formats a datetime object into a 12-hour or 24-hour time string.
        
        Args:
            unformatted_time (datetime): The datetime object to format
            hour_display_format (int): 12 or 24 hour format
            
        Returns:
            str: Formatted time string
        """
        try:
            hour_display_format = int(hour_display_format)
            if hour_display_format not in TimerConfig.POSSIBLE_HOUR_FORMATS:
                raise ValueError
                
            timezone = unformatted_time.astimezone().strftime('%Z')
            
            if hour_display_format == 12:
                formatted_hours = unformatted_time.strftime('%I:%M')
                formatted_ampm = unformatted_time.strftime('%p').lower()
                return f'{formatted_hours}{formatted_ampm} {timezone}'
            elif hour_display_format == 24:
                formatted_hours = unformatted_time.strftime('%H:%M')
                return f'{formatted_hours} {timezone}'
                
        except ValueError:
            raise ValueError('Hours format must be either 12 or 24.')

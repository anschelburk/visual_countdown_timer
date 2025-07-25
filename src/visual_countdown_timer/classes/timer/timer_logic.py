from datetime import datetime, timedelta
import math

class TimerLogic:
    """Handles all timer-related calculations and logic."""
    
    @staticmethod
    def get_next_occurrence(target_minute: int, current_time: datetime) -> datetime:
        """
        Calculate the next datetime when the minute equals target_minute.
        
        Args:
            target_minute: Target minute past the hour (0-59)
            current_time: Current datetime
            
        Returns:
            Next occurrence of target_minute
        """
        if current_time.minute < target_minute:
            # Target hasn't occurred this hour yet
            return current_time.replace(minute=target_minute, second=0, microsecond=0)
        else:
            # Target has passed, move to next hour
            next_hour = current_time + timedelta(hours=1)
            return next_hour.replace(minute=target_minute, second=0, microsecond=0)
    
    @staticmethod
    def get_remaining_seconds(target_time: datetime, current_time: datetime) -> int:
        """
        Calculate remaining seconds until target time.
        
        Args:
            target_time: Target datetime
            current_time: Current datetime
            
        Returns:
            Remaining seconds as integer
        """
        remaining = target_time - current_time
        return int(remaining.total_seconds())
    
    @staticmethod
    def get_progress_bar(remaining_seconds: int, bar_width: int = 30) -> str:
        """
        Generate a visual progress bar.
        
        Args:
            remaining_seconds: Seconds remaining
            bar_width: Width of progress bar (default 30)
            
        Returns:
            Formatted progress bar string
        """
        remaining_minutes = math.ceil(remaining_seconds / 60)
        filled_chars = min(round(remaining_minutes / 2), bar_width)
        empty_chars = bar_width - filled_chars
        
        return f"[{'#' * filled_chars}{'.' * empty_chars}]"
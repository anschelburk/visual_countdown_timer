import math

class VisualElements:
    """Handles creation of visual elements like progress bars."""
    
    @staticmethod
    def create_progress_bar(remaining_time_in_seconds):
        """
        Generates a visual progress bar representing remaining time.
        
        Args:
            remaining_time_in_seconds (int): Remaining time in seconds
            
        Returns:
            str: Visual progress bar with '#' and '.' characters
        """
        remaining_minutes_rounded = math.ceil(remaining_time_in_seconds / 60)
        progress_bar_full = '#' * round(remaining_minutes_rounded / 2)
        progress_bar_empty = '.' * (DisplaySettings.PROGRESS_BAR_WIDTH - round(remaining_minutes_rounded / 2))
        return f'[{progress_bar_full}{progress_bar_empty}]'

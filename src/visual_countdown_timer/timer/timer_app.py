from datetime import datetime
from .display_utils import ProgressBar, UserDisplay
from .system_utils import SystemUtils, TerminalUtils
from .timer_utils import TimeCalculations, UserInput

"""
Main application coordinator for the Visual Countdown Timer.

This module provides the main TimerApp class that orchestrates all other
components to create the complete countdown timer application.
"""

class TimerApp:
    """Main application coordinator."""
    
    def __init__(self):
        """Initialize the timer application."""
        TerminalUtils.initialize_exit_handler()
    
    def run(self):
        """Run the main timer application."""
        TerminalUtils.clear_terminal()
        
        # Get user preferences
        countdown_minutes = UserInput.get_countdown_time('initial')
        hour_format = UserInput.get_hour_format()
        
        # Start timer loop
        self._timer_loop(countdown_minutes, hour_format)
    
    def _timer_loop(self, countdown_minutes, hour_format):
        """Main timer loop that updates the display continuously."""
        while True:
            TerminalUtils.clear_terminal()
            
            # Get current time information
            datetime_now = datetime.now().astimezone()
            current_date = datetime_now.strftime('%B %d, %Y')
            current_time = TimeCalculations.format_time(datetime_now, hour_format)
            
            # Calculate next target time
            end_of_current_loop = TimeCalculations.get_next_occurrence(countdown_minutes, datetime_now)
            target_time = TimeCalculations.format_time(end_of_current_loop, hour_format)
            
            # Calculate remaining time
            total_remaining = TimeCalculations.get_remaining_seconds(end_of_current_loop, datetime_now)
            remaining_minutes, remaining_seconds = divmod(total_remaining, 60)
            
            # Create visual elements
            progress_bar_text = ProgressBar.create_progress_bar(total_remaining)
            
            # Display everything
            UserDisplay.show_timer_display(
                current_date, current_time, target_time,
                remaining_minutes, remaining_seconds, progress_bar_text
            )
            
            SystemUtils.sleep_until_next_second(datetime_now)

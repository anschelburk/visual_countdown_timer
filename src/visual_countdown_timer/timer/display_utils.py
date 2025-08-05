from .settings import DisplaySettings
import math

"""
Display and output handling for the Visual Countdown Timer.

This module provides classes for formatting and displaying information
to the user, including the timer interface and status messages.
"""

class ProgressBar: # Previously 'VisualElements'. Add to all other modules.
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

class UserDisplay:
    """Handles displaying information to the user."""
    
    # Display formatting constants
    INDENT = ' ' * DisplaySettings.INDENT_LENGTH
    THICK_HORIZONTAL_LINE = "=" * DisplaySettings.LINE_THICKNESS
    THIN_HORIZONTAL_LINE = "-" * DisplaySettings.LINE_THICKNESS
    """Handles displaying information to the user."""

    TIMER_INTRO_TEXT = (
        'Welcome to Visual Countdown Timer!\n' +
        'This timer counts down to a set number of minutes past each hour.\n' +
        'For example, if you enter \"25\", it will count down to 1:25, 2:25, etc.\n'
    )
#    @staticmethod
#    def show_intro_text(runtime_status):
#        """Displays introductory text based on runtime status."""
#        if runtime_status == 'initial':
#            print('Welcome to Visual Countdown Timer!')
#            print('This timer counts down to a set number of minutes past each hour.')
#            print('For example, if you enter "25", it will count down to 1:25, 2:25, etc.\n')
#        elif runtime_status == 'update':
#            print('\nWould you like to update the countdown time?')

    TITLE_BLOCK = (
        THICK_HORIZONTAL_LINE + '\n' +
        'Visual Countdown Timer\n' +
        'Press Ctrl + C to exit.\n' +
        THICK_HORIZONTAL_LINE + '\n\n'
    )
    
    @staticmethod
    def show_timer_display(current_date, current_time, target_time, remaining_minutes, 
                          remaining_seconds, progress_bar_text):
        """Displays the main timer interface."""
        minutes_label = "minute" if remaining_minutes == 1 else "minutes"
        seconds_label = "second" if remaining_seconds == 1 else "seconds"

        print(UserDisplay.TITLE_BLOCK)
        
        print(current_date)
        print(f'Current Time: {current_time}')
        
        print('')
        print(UserDisplay.THIN_HORIZONTAL_LINE)
        print(f'Countdown until {target_time}:')
        print(UserDisplay.THIN_HORIZONTAL_LINE)
        print(f'{UserDisplay.INDENT}{remaining_minutes:02} {minutes_label}')
        print(f'{UserDisplay.INDENT}{remaining_seconds:02} {seconds_label}')
        print(progress_bar_text)

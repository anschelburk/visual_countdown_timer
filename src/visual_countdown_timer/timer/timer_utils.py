from datetime import datetime, timedelta
from .display_utils import ProgressBar, UserDisplay
from .settings import TimerConfig
from .system_utils import SystemUtils

"""
Time calculation and formatting utilities for the Visual Countdown Timer.

This module provides classes for handling datetime operations, including
calculating next occurrences, remaining time, and formatting time displays.
"""

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
            else:
                raise ValueError
                
        except ValueError:
            raise ValueError('Hours format must be either 12 or 24.')

class UserInput:
    """Handles all user input collection and validation."""
    
    @staticmethod
    def get_countdown_time(runtime_status):
        """
        Prompts the user to enter a countdown time and returns it if valid.
        
        Args:
            runtime_status (str): 'initial' or 'update'
        
        Returns:
            countdown_minutes (int): A valid countdown minute (0–59)
        """
        print(UserDisplay.TIMER_INTRO_TEXT)

        while True:
            try:
                countdown_minutes = UserInput._get_minutes_input()
                if UserInput._confirm_minutes(countdown_minutes):
                    return countdown_minutes
                else:
                    print('')  # restart loop
            except ValueError as error_message:
                print(f"\nError: {error_message}\n")
    
    @staticmethod
    def get_hour_format():
        """
        Prompts the user to choose between 12-hour and 24-hour time display.
        
        Returns:
            user_hours (int): The user's preferred time format (12 or 24).
        """
        print("\nWould you like the time to display as 12 hours or 24 hours?")
        print(f'{UserDisplay.INDENT}{UserDisplay.THIN_HORIZONTAL_LINE}')
        print(f"{UserDisplay.INDENT}12 hours looks like this: 3:52pm")
        print(f"{UserDisplay.INDENT}24 hours looks like this: 15:52")
        print(f'{UserDisplay.INDENT}{UserDisplay.THIN_HORIZONTAL_LINE}')

        user_hours = input('Type "12" for 12-hour format, or "24" for 24-hour format: ')
        user_hours_validated = ValidateInput.hour_format(user_hours)
        return user_hours_validated
    
    @staticmethod
    def _get_minutes_input():
        """Prompts for and validates minute input."""
        user_input = SystemUtils.clean_text(input("Please enter the number of minutes you'd like to count down to: "))
        
        try:
            minute = int(user_input)
            if not (0 <= minute < 60):
                raise ValueError
        except ValueError:
            raise ValueError("The number of minutes must be a whole number between 0 and 59 (e.g., 0, 3, 25, 59).")

        return minute
    
    @staticmethod
    def _confirm_minutes(minutes:int) -> bool:
        """Displays preview and gets user confirmation."""

        print(f'\nYou entered {minutes} minutes. The timer will count down to:')

        EXAMPLE_HOURS_START = 1
        EXAMPLE_HOURS_END = 3
        print(' | '.join(f'{hour:02}:{minutes:02}' for hour in range(EXAMPLE_HOURS_START, EXAMPLE_HOURS_END + 1)) + ' | etc.\n')

        user_confirmation = input("Is this correct? Please enter \"y\" for yes, or \"n\" for no: ")
        user_confirmation_bool = SystemUtils.confirm_y_or_n(user_confirmation)
        return user_confirmation_bool

class ValidateInput:

    """
    Input validation utilities for user interactions.
    """

    @staticmethod
    def hour_format(user_input: int) -> int:
        """
        Checks to make sure the user entered a valid input for the hour display format.
        If they have, this function returns the user input.
        If not, it prompts them to re-enter the input.

        Args:
            user_input (int): The user's input for the hours display format they would like the app to use.
        """
        while True:
            try:
                user_input = SystemUtils.clean_text(user_input)
                user_input = int(user_input)
                if user_input in TimerConfig.POSSIBLE_HOUR_FORMATS:
                    return user_input
                else:
                    raise ValueError
            except ValueError:
                print(f"\nError: please enter either 12 or 24. You typed: '{user_input}'\n")
                user_input = input("Please type \"12\" for 12-hour format, or \"24\" for 24-hour format: ")

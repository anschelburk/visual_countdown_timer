from datetime import datetime, timedelta
from .display_utils import ProgressBar, UserDisplay
from .settings import TimerConfig
from .system_utils import SystemUtils, TerminalUtils

"""
Time calculation and formatting utilities for the Visual Countdown Timer.

This module provides classes for handling datetime operations, including
calculating next occurrences, remaining time, and formatting time displays.
"""

class Format:
    """
    Formats time and date entries for user display.
    """

    @staticmethod
    def date(datetime_unformatted: datetime) -> datetime:
        """
        Formats a date for the user display.

        Args:
            datetime_unformatted (datetime): The datetime object to format
        Returns:
            date_formatted (datetime): The formatted date.
        """
        date_formatted = datetime_unformatted.strftime('%B %d, %Y')
        return date_formatted

    @classmethod
    def time(cls, datetime_unformatted: datetime, hour_display_format: int) -> str:
        """
        Formats a datetime object into a 12-hour or 24-hour time string.
        
        Args:
            datetime_unformatted (datetime): The datetime object to format
            hour_display_format (int): 12 or 24 hour format
            
        Returns:
            time_formatted (str): Formatted time string
        """
        try:
            hour_display_format = int(hour_display_format)
            if hour_display_format not in TimerConfig.POSSIBLE_HOUR_FORMATS:
                raise ValueError
                
            if hour_display_format == 12:
                time_formatted_notimezone = cls._time_12h(datetime_unformatted)
            elif hour_display_format == 24:
                time_formatted_notimezone = cls._time_24h(datetime_unformatted)
            else:
                raise ValueError

            time_formatted = cls._add_timezone(datetime_unformatted, time_formatted_notimezone)
            return time_formatted
                
        except ValueError:
            raise ValueError('Hours format must be either 12 or 24.')

    @staticmethod
    def _add_timezone(datetime_unformatted: datetime, time_without_timezone: str) -> str:
        """
        Appends timezone information to a formatted time string.
        Args:
            datetime_unformatted (datetime): The unformatted datetime object (used to determine timezone).
            time_without_timezone (str): A formatted time string without timezone (e.g., "15:30", "3:30pm").
        Returns:
            time_with_timezone (str): The time string with timezone appended            
        """
        timezone = datetime_unformatted.strftime('%Z')
        time_with_timezone = time_without_timezone + ' ' + timezone
        return time_with_timezone

    @staticmethod
    def _time_12h(datetime_unformatted: datetime) -> str:
        """
        Formats the time using 12-hour display format for user display.

        Args:
            datetime_unformatted (datetime): The datetime object to format
        Returns:
            time_formatted (str): The time formatted for 12-hour display.
        """
        formatted_hours = datetime_unformatted.strftime('%-I:%M')
        formatted_ampm = datetime_unformatted.strftime('%p').lower()       
        time_formatted = f'{formatted_hours}{formatted_ampm}'
        return time_formatted

    @staticmethod
    def _time_24h(datetime_unformatted: datetime) -> str:
        """
        Formats the time using 12-hour display format for user display.

        Args:
            datetime_unformatted (datetime): The datetime object to format
        Returns:
            time_formatted (str): The time formatted for 24-hour display.
        """
        time_formatted = datetime_unformatted.strftime('%H:%M')
        return time_formatted

    @staticmethod
    def remaining_time(remaining_minutes:int, remaining_seconds:int) -> str:
        """
        Formats the remaining minutes and seconds for display in-app.

        Args:
            remaining_minutes (int): The unformatted number of remaining minutes.
            remaining_seconds (int): The unformatted number of remaining seconds.

        Returns:
            remaining_time_formatted (str): The formatted number of remaining minutes and seconds.
        """

        minutes_label = SystemUtils.pluralize("minute", remaining_minutes)
        seconds_label = SystemUtils.pluralize("second", remaining_seconds)

        remaining_minutes_formatted = f'{UserDisplay.INDENT}{remaining_minutes:02} {minutes_label}'
        remaining_seconds_formatted = f'{UserDisplay.INDENT}{remaining_seconds:02} {seconds_label}'

        remaining_time_formatted = (
            remaining_minutes_formatted + '\n' +
            remaining_seconds_formatted
        )

        return remaining_time_formatted

class Calculate:
    """Handles all time-related calculations."""
    
    @staticmethod
    def next_countdown_occurrence(target_minute: int, current_datetime: datetime) -> datetime:
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
    def remaining_seconds(end_time: datetime, current_datetime: datetime) -> int:
        """
        Calculates total remaining seconds until end_time input.
        
        Args:
            end_time (datetime): Target end time
            current_datetime (datetime): Current time
            
        Returns:
            remaining_seconds (int): Total remaining seconds
        """
        remaining_time = end_time - current_datetime
        remaining_seconds = int(remaining_time.total_seconds())
        return remaining_seconds
    
class TimerLoop:
    """
    Manages the continuous countdown timer execution and display updates.
    
    This class encapsulates the main timer loop functionality, coordinating
    time calculations, visual display updates, and system operations to
    provide a real-time countdown experience. It continuously updates the
    terminal display with current time, target time, remaining duration,
    and a visual progress bar until the user exits.
    
    The timer loop operates on one-second intervals, recalculating and
    refreshing the display each second to show accurate countdown progress
    toward the next occurrence of the specified target minute.
    
    Attributes:
        countdown_minutes (int): Target minute past each hour (0-59)
        hour_format (int): Time display format (12 or 24 hour)
    
    Example:
        >>> timer_loop = TimerLoop(25, 12)
        >>> timer_loop.run()  # Starts continuous countdown to X:25
    """
    
    @staticmethod
    def run(countdown_minutes, hour_format):
        """Main timer loop that updates the display continuously."""
        while True:
            TerminalUtils.clear_terminal()
            
            # Get current time information
            datetime_now = datetime.now().astimezone()
            current_date = Format.date(datetime_now)
            current_time = Format.time(datetime_now, hour_format)
            
            # Calculate next target time
            end_of_current_loop = Calculate.next_countdown_occurrence(countdown_minutes, datetime_now)
            target_time = Format.time(end_of_current_loop, hour_format)
            
            # Calculate remaining time
            total_seconds = Calculate.remaining_seconds(end_of_current_loop, datetime_now)
            remaining_minutes, remaining_seconds = divmod(total_seconds, 60)
            remaining_time = Format.remaining_time(remaining_minutes, remaining_seconds)
            
            # Create visual elements
            progress_bar_text = ProgressBar.render(total_seconds)
            
            # Display everything
            print(
                UserDisplay.show_timer_display(
                    current_date, current_time, target_time,
                    remaining_time, progress_bar_text
                )
            )
            
            SystemUtils.sleep_until_next_second(datetime_now)


class UserInput:
    """Handles all user input collection and validation."""

    # @staticmethod
    # def countdown_minutes():
        # print(UserDisplay.TIMER_INTRO_TEXT)
        # while True:
            # user_minutes_raw = input("Please enter the number of minutes you'd like to count down to: ")
            # user_minutes_clean = SystemUtils.clean_text(user_minutes_raw)
            # if _can_be_cast_as_int(user_minutes_clean):
                # 
    
    # def _can_be_cast_as_int(countdown_minutes_from_user: str) -> bool:
        # try:
            # countdown_minutes_int = int(countdown_minutes_from_user)
            # return True
        # except ValueError:
            # return False

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
    
    @classmethod
    def get_hour_format(cls) -> int:
        """
        Prompts the user to choose between 12-hour and 24-hour time display.

        Args:
            None
            
        Returns:
            user_hours_validated (int): The user's preferred time format (12 or 24).
        """
        print(cls._HOUR_FORMAT_USER_PROMPT)
        user_hours = input('Type \"12\" for 12-hour format, or \"24\" for 24-hour format: ')
        user_hours_validated = ValidateInput.hour_format(user_hours)
        return user_hours_validated

    _HOUR_FORMAT_USER_PROMPT = (
        "\nWould you like the time to display as 12 or 24 hours?" +
        "\n" + UserDisplay.INDENTED_HORIZONTAL_LINE +
        f"\n{UserDisplay.INDENT}12 hours looks like this: 3:52pm" +
        f"\n{UserDisplay.INDENT}24 hours looks like this: 15:52" +
        "\n" + UserDisplay.INDENTED_HORIZONTAL_LINE
    )
    
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

        user_confirmation = ValidateInput.confirm_user_choice()
        return user_confirmation

class ConfirmInput:
    """
    Confirmation prompts for user interactions.
    """

#     @staticmethod
#     def user_minutes(user_input: int):
#         """
#         Confirms countdown minutes from user.
#         """
# 
#         print(f'\nYou entered {user_input} minutes. The timer will count down to:')
# 
#         EXAMPLE_HOURS_START = 1
#         EXAMPLE_HOURS_END = 3
#         print(' | '.join(f'{hour:02}:{minutes:02}' for hour in range(EXAMPLE_HOURS_START, EXAMPLE_HOURS_END + 1)) + ' | etc.\n')
# 
#         user_confirmation = ValidateInput.confirm_user_choice()
#         return user_confirmation

class ValidateInput:
# Rename Valid
    # Valid.integer()
    # Valid.minutes_range()
    # Valid.hour_display_format()
    # Valid.user_input (to check multiple)

    """
    Input validation utilities for user interactions.
    """

    @staticmethod
    def integer(user_input) -> bool:
        try:
            int(user_input)
            return True
        except ValueError:
            return False
        
    def minutes_range(user_input: int) -> bool:
        return (0 <= user_input < 60)

    @staticmethod
    def confirm_user_choice() -> bool:
        """
        Prompts the user for yes/no confirmation and returns their choice.
        
        Continuously prompts until the user enters a valid response ('y' or 'n').
        Input is automatically cleaned of whitespace and converted to lowercase.

        Args:
            None
        Returns:
            bool: True if user confirms with 'y', False if user declines with 'n'
        """
        user_confirmation = input("Is this correct? Please enter \"y\" for yes, or \"n\" for no: ")
        while True:
            user_confirmation = SystemUtils.clean_text(user_confirmation).lower()
            if user_confirmation == 'y':
                return True
            elif user_confirmation == 'n':
                return False
            else:
                user_confirmation = input('Error: Please type either \"y\" to for yes, or \"n\" for no: ')

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

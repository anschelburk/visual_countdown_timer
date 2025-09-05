from datetime import datetime, timedelta
from .display_utils import ProgressBar, UserDisplay
from .settings import TimerConfig
from .system_utils import SystemUtils, TerminalUtils
from .validation import InputIsValid

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
        This function assumes that the `hour_display_format` input has been checked, and is:
            1) An integer.
            2) A valid hour display format, as defined in settings.TimerConfig.POSSIBLE_HOUR_FORMATS.
        
        Args:
            datetime_unformatted (datetime): The datetime object to format
            hour_display_format (int): 12 or 24 hour format
            
        Returns:
            time_formatted (str): Formatted time string
        """

        if hour_display_format == 12:
            time_formatted_notimezone = cls._time_12h(datetime_unformatted)
        elif hour_display_format == 24:
            time_formatted_notimezone = cls._time_24h(datetime_unformatted)
        time_formatted = cls._add_timezone(datetime_unformatted, time_formatted_notimezone)
        return time_formatted

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
            SystemUtils.wrap_text(
                func_name = print,
                text_unformatted = UserDisplay.show_timer_display(
                    current_date, current_time, target_time,
                    remaining_time, progress_bar_text
                )
            )
            
            SystemUtils.sleep_until_next_second(datetime_now)


class UserInput:
    """Handles all user input collection and validation."""

    @staticmethod
    def get_countdown_time():
        """
        Prompts the user to enter a countdown time and returns it if valid.
        
        Args:
            None        
        Returns:
            countdown_minutes (int): A valid countdown minute (0–59)
        """
        while True:
            countdown_minutes = SystemUtils.wrap_text(
                func_name = input,
                text_unformatted = "\nPlease enter the number of minutes you'd like to count down to: ",
                add_linebreaks=False
            )
            countdown_minutes = SystemUtils.clean_text(countdown_minutes)
            if InputIsValid.integer(countdown_minutes):
                countdown_minutes = int(countdown_minutes)
                if InputIsValid.minutes_range(countdown_minutes):
                    if UserConfirms.countdown_time(countdown_minutes):
                        return countdown_minutes
    
    @classmethod
    def get_hour_format(cls) -> int:
        """
        Prompts the user to choose between 12-hour and 24-hour time display.

        Args:
            None
            
        Returns:
            user_hours_validated (int): The user's preferred time format (12 or 24).
        """
        while True:

            SystemUtils.wrap_text(
                func_name = print,
                text_unformatted=(
                    "\nWould you like the time to display as 12 or 24 hours?" +
                    f"\n{UserDisplay.INDENTED_HORIZONTAL_LINE}" +
                    f"\n{UserDisplay.INDENT}12 hours looks like this: 3:52pm" +
                    f"\n{UserDisplay.INDENT}24 hours looks like this: 15:52" +
                    f"\n{UserDisplay.INDENTED_HORIZONTAL_LINE}"
                )
            )
            user_hours = SystemUtils.wrap_text(
                func_name= input,
                text_unformatted='Type \"12\" for 12-hour format, or \"24\" for 24-hour format: '
            )
            # Add this to print_wrapped - maybe change to text_wrapped(func_name, input_text)
            # Where func_name (str) = 'input' or 'print' and the output is `return func_name(...)`` instead of `return print(...)`
            if InputIsValid.integer(user_hours):
                user_hours = int(user_hours)
                if InputIsValid.hour_display_format(user_hours):
                    if UserConfirms.hour_display_format(user_hours):
                        return user_hours

class UserConfirms:
    """
    Confirmation prompts for user interactions.
    """

    @classmethod
    def countdown_time(cls, minutes:int) -> bool:
        """Displays preview and gets user confirmation."""

        SystemUtils.wrap_text(
            func_name = print,
            text_unformatted=f'\nYou entered {minutes} minutes. The timer will count down to:'
        )

        EXAMPLE_HOURS_START = 1
        EXAMPLE_HOURS_END = 3
        EXAMPLE_HOURS_DISPLAY = ' | '.join(f'{hour:02}:{minutes:02}' for hour in range(EXAMPLE_HOURS_START, EXAMPLE_HOURS_END + 1)) + ' | etc.\n'
        
        SystemUtils.wrap_text(
            func_name= print,
            text_unformatted=EXAMPLE_HOURS_DISPLAY
        )

        if cls._confirm_user_input():
            return True
        else:
            SystemUtils.wrap_text(
                func_name= print,
                text_unformatted="\nNo problem! Let's try again:"
            )
            return False

    @classmethod
    def hour_display_format(cls, user_hours: int) -> bool:
        """
        Prompts the user to confirm their choice for hour display format (either 12 or 24).
        *Please note:* This function assumes that the input has been confirmed valid under the following criteria:
            1. The input is an integer, as defined in: validation.InputIsValid.integer()
            2. The input is a valid hour display format, as defined in: validation.InputIsValid.hour_display_format()
        
        Args:
            user_hours (int): The hour display format the user has entered, to confirm.
        Returns:
            bool: True if the user confirms yes, False for all other responses.
        """
    
        SystemUtils.wrap_text(
            func_name= print,
            text_unformatted=f"\n{user_hours}-hour display format selected."
        )
        if cls._confirm_user_input():
            return True
        else:
            SystemUtils.wrap_text(
                func_name= print,
                text_unformatted="\nNo problem! Let's try again:"
            )
            return False

    @staticmethod
    def _confirm_user_input() -> bool:
        # Break this up by adding a new method:
        # InputIsValid.user_confirmation()
        """
        Prompts the user for yes/no confirmation and returns their choice.
        
        Continuously prompts until the user enters a valid response ('y' or 'n').
        Input is automatically cleaned of whitespace and converted to lowercase.

        Args:
            None
        Returns:
            bool: True if user confirms with 'y', False if user declines with 'n'
        """
        user_confirmation = SystemUtils.wrap_text(
            func_name = input,
            text_unformatted = "Is this correct? Please enter \"y\" for yes, or \"n\" for no: "
        )
        while True:
            user_confirmation = SystemUtils.clean_text(user_confirmation).lower()
            if user_confirmation == 'y':
                return True
            elif user_confirmation == 'n':
                return False
            else:
                user_confirmation = SystemUtils.wrap_text(
                    func_name = input,
                    text_unformatted = 'Error: Please type either \"y\" to for yes, or \"n\" for no: '
                )

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
    def user_input(user_input, *validity_checks) -> bool:
        """
        Validates user input against multiple validation functions.
    
        Takes a user input value and applies a series of validation functions
        to determine if the input meets all specified criteria. All validation
        functions must return True for the input to be considered valid.
        
        Args:
            user_input: The user input value to validate. Can be any type
                depending on the validation functions being used.
            *validity_checks: Variable number of callable validation functions.
                Each function should take user_input as its single argument
                and return True if valid, False if invalid.
        
        Returns:
            bool: True if user_input passes all validation checks,
                  False if any validation check fails.
        """
        for valid in validity_checks:
            if not valid(user_input):
                return False
        return True

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
                SystemUtils.wrap_text(
                    func_name = print,
                    text_unformatted=f"\nError: please enter either 12 or 24. You typed: \"{user_input}\"\n"
                )
                SystemUtils.wrap_text(
                    func_name= input,
                    text_unformatted="Please type \"12\" for 12-hour format, or \"24\" for 24-hour format: "
                )

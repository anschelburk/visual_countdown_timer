from .support import clean_text
from .constants import INDENT, THIN_HORIZONTAL_LINE, POSSIBLE_HOUR_DISPLAY_FORMATS


class UserInput:
    """Handles all user input and validation."""
    
    def get_hour_format(self) -> int:
        """
        Get user's preferred hour format (12 or 24).
        
        Returns:
            12 or 24 based on user preference
        """
        print("\nWould you like the time to display as 12 hours or 24 hours?")
        print(f'{INDENT}{THIN_HORIZONTAL_LINE}')
        print(f"{INDENT}12 hours looks like this: 3:52pm")
        print(f"{INDENT}24 hours looks like this: 15:52")
        print(f'{INDENT}{THIN_HORIZONTAL_LINE}')
        
        while True:

            user_input = clean_text(input('Type "12" for 12-hour format, or "24" for 24-hour format: '))
            
            try:
                user_input = int(user_input)
                if user_input in POSSIBLE_HOUR_DISPLAY_FORMATS:
                    return user_input
                else:
                    raise ValueError

            except ValueError:
                print(f"\nError: please enter either 12 or 24. You typed: '{user_input}'\n")
    
    def get_countdown_time(self, status: str = 'initial') -> int:
        """
        Get countdown time in minutes from user.
        
        Args:
            status: 'initial' for first run, 'update' for changes
            
        Returns:
            Valid countdown minute (0-59)
        """
        self._show_intro_text(status)
        
        while True:
            try:
                minutes = self._get_minutes_input()
                if self._confirm_minutes(minutes):
                    return minutes
                print()  # Add spacing before retry
            except ValueError as e:
                print(f"\nError: {e}\n")
    
    def _show_intro_text(self, status: str):
        """Show appropriate intro text based on status."""
        if status == 'initial':
            print('Welcome to Visual Countdown Timer!')
            print('This timer counts down to a set number of minutes past each hour.')
            print('For example, if you enter "25", it will count down to 1:25, 2:25, etc.\n')
        elif status == 'update':
            print('\nWould you like to update the countdown time?')
    
    def _get_minutes_input(self) -> int:
        """Get and validate minutes input from user."""
        
        user_input = clean_text(input("Please enter the number of minutes you'd like to count down to: "))
        
        try:
            minute = int(user_input)
            if 0 <= minute < 60:
                return minute
            else:
                raise ValueError
        
        except ValueError:
            raise ValueError("The number of minutes must be a whole number between 0 and 59.")
    
    def _confirm_minutes(self, minutes: int) -> bool:
        """
        Get user confirmation for selected minutes.
        
        Args:
            minutes: Selected minute value
            
        Returns:
            True if confirmed, False if rejected
        """
        # Show preview of countdown times
        examples = [f'{h:02}:{minutes:02}' for h in range(1, 4)]
        print(f'\nYou entered {minutes} minutes. The timer will count down to:')
        print(' | '.join(examples) + ' | etc.\n')
        
        while True:
            response = clean_text(input("Is this correct? Please enter 'y' or 'n': ")).lower()
            if response == 'y':
                return True
            elif response == 'n':
                return False
            print("\nInvalid answer: Please enter 'y' for yes, or 'n' for no.")
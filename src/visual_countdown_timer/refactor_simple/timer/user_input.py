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
        UserDisplay.show_intro_text(runtime_status)

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

        while True:
            user_input = SystemUtils.clean_text(input('Type "12" for 12-hour format, or "24" for 24-hour format: '))
            try:
                user_hours = int(user_input)
                if user_hours in TimerConfig.POSSIBLE_HOUR_FORMATS:
                    return user_hours
                else:
                    raise ValueError
            except ValueError:
                print(f"\nError: please enter either 12 or 24. You typed: '{user_input}'\n")
    
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
    def _confirm_minutes(minutes):
        """Displays preview and gets user confirmation."""
        print(f'\nYou entered {minutes} minutes. The timer will count down to:')
        print(' | '.join(f'{hour:02}:{minutes:02}' for hour in range(TimerConfig.FIRST_HOUR_IN_RANGE, TimerConfig.LAST_HOUR_IN_RANGE + 1)) + ' | etc.\n')

        while True:
            user_confirmation = SystemUtils.clean_text(input("Is this correct? Please enter 'y' or 'n': ")).lower()
            if user_confirmation == 'y':
                return True
            elif user_confirmation == 'n':
                return False
            else:
                print("\nInvalid answer: Please enter 'y' for yes, or 'n' for no.")

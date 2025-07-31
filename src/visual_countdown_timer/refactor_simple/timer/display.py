class UserDisplay:
    """Handles displaying information to the user."""
    
    # Display formatting constants
    INDENT = ' ' * DisplaySettings.INDENT_LENGTH
    THICK_HORIZONTAL_LINE = "=" * DisplaySettings.LINE_THICKNESS
    THIN_HORIZONTAL_LINE = "-" * DisplaySettings.LINE_THICKNESS
    """Handles displaying information to the user."""
    
    @staticmethod
    def show_intro_text(runtime_status):
        """Displays introductory text based on runtime status."""
        if runtime_status == 'initial':
            print('Welcome to Visual Countdown Timer!')
            print('This timer counts down to a set number of minutes past each hour.')
            print('For example, if you enter "25", it will count down to 1:25, 2:25, etc.\n')
        elif runtime_status == 'update':
            print('\nWould you like to update the countdown time?')
    
    @staticmethod
    def show_title_block():
        """Prints the title block for the Visual Countdown Timer interface."""
        print(UserDisplay.THICK_HORIZONTAL_LINE)
        print('Visual Countdown Timer')
        print('Press Ctrl + C to exit.')
        print(f'{UserDisplay.THICK_HORIZONTAL_LINE}\n')
    
    @staticmethod
    def show_timer_display(current_date, current_time, target_time, remaining_minutes, 
                          remaining_seconds, progress_bar_text):
        """Displays the main timer interface."""
        minutes_label = "minute" if remaining_minutes == 1 else "minutes"
        seconds_label = "second" if remaining_seconds == 1 else "seconds"

        UserDisplay.show_title_block()
        
        print(current_date)
        print(f'Current Time: {current_time}')
        
        print('')
        print(UserDisplay.THIN_HORIZONTAL_LINE)
        print(f'Countdown until {target_time}:')
        print(UserDisplay.THIN_HORIZONTAL_LINE)
        print(f'{UserDisplay.INDENT}{remaining_minutes:02} {minutes_label}')
        print(f'{UserDisplay.INDENT}{remaining_seconds:02} {seconds_label}')
        print(progress_bar_text)

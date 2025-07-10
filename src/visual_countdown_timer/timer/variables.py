from datetime import datetime

def current_date():
    """
    Calculates the current date, formatted as follows: [Month] [Day], [Year].
    Args:
        None.
    Returns:
        current_date (datetime): a datetime object, formatted as described above.
    """
    current_date = datetime.now().strftime('%B %d, %Y')
    return current_date

def current_time():
    """
    Calculates the current time, formatted as follows: [Hour]:[Minute] [Timezone]
    Args:
        None.
    Returns:
        current_time (datetime): a datetime object, formatted as described above.
    """
    current_time = datetime.now().astimezone().strftime('%H:%M %Z')
    return current_time
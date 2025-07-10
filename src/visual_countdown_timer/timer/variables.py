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
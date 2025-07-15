import os

def clean_text(unformatted_text):
    """
    Removes leading and trailing spaces and common punctuation from a string.

    Args:
        unformatted_text (str): The string to be cleaned.

    Returns:
        clean_text (str): The cleaned string with specified characters removed from both ends.
    """
    characters_to_remove = " .,\"\'"
    clean_text = unformatted_text.strip(characters_to_remove)
    return clean_text

def  clear_terminal():
    """
    Clears the terminal screen.
    Args: None.
    Returns: None.    
    """
    # Clear terminal on Windows:
    if os.name == 'nt':
        os.system('cls')
    
    # Clear terminal on MacOS or Linux:
    else:
        os.system('clear')
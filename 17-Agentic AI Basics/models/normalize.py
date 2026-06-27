def normalize(text):
    """Normalizes an input string by converting it to lowercase and removing leading/trailing whitespace.

    Args:
        text (str): The raw input string text to normalize.

    Returns:
        str: The sanitized, lowercased, and stripped string.
    """
    return text.lower().strip()
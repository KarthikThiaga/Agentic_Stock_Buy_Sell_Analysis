from rapidfuzz import process 
from config.logger import logger

def fuzzy_match(word, choices):
    """Performs a fuzzy string matching lookup on a target word against a list of choices.

    Uses an approximation extraction utility to find the single closest match for the 
    specified token. If the calculated similarity score meets or exceeds a baseline 
    threshold of 80, the match is accepted and returned along with its classification metadata.

    Args:
        word (str): The target token or string slice to resolve (e.g., a company name fragment).
        choices (Iterable[str]): A collection or database of valid target strings to match against.

    Returns:
        Tuple[str | None, str | None, int | float]: A structured tuple containing:
            - match (str or None): The closest string match if the confidence score >= 80; 
              otherwise, None.
            - logic (str or None): The matching classification strategy applied ('fuzzy') if 
              successful; otherwise, None.
            - score (int or float): The raw similarity score assigned to the closest match, 
              or 0 if it fails the threshold test.
    """
    match, score, _ = process.extractOne(word,choices)
    logger.info (f'event=fuzzy_match token={word} match={match}, score={score}')
    if score >= 80:
        logic = 'fuzzy'
        return match, logic, score
    
    return None,None,0

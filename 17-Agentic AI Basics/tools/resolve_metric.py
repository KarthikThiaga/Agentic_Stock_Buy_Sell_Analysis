
from models.normalize import normalize

BLACKLIST = ["other", "misc", "non-current"]


EXACT_MATCH = {
    "assets": ["total assets"],
    "liabilities": ["total liabilities"],
    "cash": ["cash and cash equivalents"]
}

FUZZY_MATCH = {
    "assets": [
        "assets, current",
        "assets total"
    ],
    "liabilities": [
        "liabilities, current",
        "total liabilities",
        "liabilities"
    ],
    "cash": [
        "cash equivalents",
    ]
}


def resolve_metric(input):
    """Resolves raw accounting report labels into standardized target metrics with confidence scores.

    Normalizes the input label string and systematically matches it against matching rule maps. 
    The matching process follows a strict hierarchy of valuation stages:
    1. Check against a blacklist of generic keywords to avoid noisy matches.
    2. Check for exact equality against a predefined list of high-confidence synonyms (Confidence Score 3).
    3. Check for partial or fuzzy substring containment within secondary synonyms (Confidence Score 2).

    Args:
        input (str): The raw text label extracted from the source financial report document row.

    Returns:
        Tuple[str | None, int]: A tuple containing the resolution result metadata:
            - The canonical internal system key name ('assets', 'liabilities', 'cash') or None if unmapped.
            - An integer confidence score matching the quality tier (3 for Exact, 2 for Fuzzy, 0 for Unresolved/Blacklisted).
    """
    label = normalize(input)

    if any(b in label for b in BLACKLIST):  
        return None, 0
    

    for key,phrases in EXACT_MATCH.items():

        if any(p == label for p in phrases):
            return key,3
    
    for key,phrases in FUZZY_MATCH.items():

        if any(p in label for p in phrases):
            return key,2
        

    return None,0

FALL_BACK_EXACT_MATCH = {
    "assets": ["totalAssets"],
    "liabilities": ["totalLiabilities"],
    "cash": ["cashAndCashEquivalentsAtCarryingValue"]
}

def resolve_financial_term(term):
    """Maps vendor-specific financial accounting terminology to standardized keys.

    Iterates through a pre-defined registry of exact match synonyms (`FALL_BACK_EXACT_MATCH`) 
    to resolve vendor-specific reporting attributes (e.g., 'totalAssets') back into internal 
    canonical system keys ('assets', 'liabilities', or 'cash').

    Args:
        term (str): The raw accounting key string extracted from the external vendor response payload.

    Returns:
        str | None: The matching canonical internal key name (e.g., 'assets') if a mapping 
        synonym is identified; otherwise, returns None.
    """
    for key, synonyms in FALL_BACK_EXACT_MATCH.items():
        if term in synonyms:
            return key
    return None

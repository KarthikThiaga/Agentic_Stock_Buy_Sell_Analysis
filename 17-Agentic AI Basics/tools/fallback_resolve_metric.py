FALL_BACK_EXACT_MATCH = {
    "assets": ["totalAssets"],
    "liabilities": ["totalLiabilities"],
    "cash": ["cashAndCashEquivalentsAtCarryingValue"]
}

def resolve_financial_term(term):
    for key, synonyms in FALL_BACK_EXACT_MATCH.items():
        if term in synonyms:
            return key
    return None

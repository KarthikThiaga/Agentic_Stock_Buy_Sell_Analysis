
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

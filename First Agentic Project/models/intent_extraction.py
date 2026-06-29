import re
from app.emit_event import emit_event

COMPARISON_KEYWORDS = ['compare', 'comparison', 'difference', 'best', 'better']

PRICE_KEYWORDS = ['price', 'trading', 'value', 'quote']
NEWS_KEYWORDS = ['news','update', 'happening', 'recent']
BUY_KEYWORDS = ['buy', 'invest','good', 'worth','analyse']


def parsing_intent(query):
    """Parses individual space-separated tokens from a query to extract metric topics.

    Iterates through each space-separated token in the query string to check for exact 
    matches against sets of predefined financial data category keywords (price, news, 
    and analysis metrics). Confirmed matches are aggregated into a unique list of 
    intent strings.

    Args:
        query (str): The preprocessed, lowercase query string to examine.

    Returns:
        List[str]: A list of identified intent topics matching the detected 
        keywords (e.g., `['price', 'news']`).
    """
    intents = []
    for token in query.split():
        for word in PRICE_KEYWORDS:
            if word == token:
                if not 'price' in intents:
                    intents.append('price')
        for word in NEWS_KEYWORDS:
            if word == token:
                if not 'news' in intents:
                    intents.append('news')
        for word in BUY_KEYWORDS:
            if word == token:
                if not 'analysis' in intents:
                    intents.append('analysis')

    # for word in PRICE_KEYWORDS: 
    #     for token in query.split():
    #         if word == token:
    #             intents.append('price')
    #             break
    # for word in NEWS_KEYWORDS: 
    #     for token in query.split():
    #         if word == token:
    #             intents.append('news')
    #             break
    # for word in BUY_KEYWORDS: 
    #     for token in query.split():
    #         if word == token:
    #             intents.append('analysis')
    #             break
    # if any (word in query for word in NEWS_KEYWORDS):
    #     intents.append('news')
    # if any(word in query for word in BUY_KEYWORDS):
    #     intents.append('analysis')
    
    return intents

def get_intent(query):
    """Extracts operational intent classifications and objective categories from a query.

    Cleans the incoming user query by removing specialized characters and converting 
    the casing to lowercase. It evaluates whether any comparison keywords are present 
    among the isolated tokens to set a comparison boolean flag, and then determines 
    the active metric tracking topics by delegating to `parsing_intent`.

    Args:
        query (str): The natural language query string submitted by the user.

    Returns:
        Dict[str, Any]: A structured intent dictionary containing:
            - 'compare' (bool): True if comparison indicators are discovered in 
              the query; otherwise, False.
            - 'basis' (List[str]): A list of extracted core financial topics 
              (such as 'price', 'news', or 'analysis') required to service the query.

    Events Emitted:
        Emits an initial "info" level event tracking status via `emit_event` 
        indicating that intent parsing has initiated.
    """
    emit_event({'type': 'info', 'text': 'Parsing intent from query'})
    q = query.lower()
    cleaned_query = re.sub(r"[!@#$%^&?*]", "", q)
    compare = False
    for word in COMPARISON_KEYWORDS:
        for token in cleaned_query.split():
            if word == token:
                #emit_event({'type': 'info', 'text': f'Comparison keyword detected: {word}'})
                compare = True
                break
    
    intent = {
        'compare': compare,
        'basis': parsing_intent(cleaned_query),
    }


    # intent = {
    #     'compare': any(word in q for word in COMPARISON_KEYWORDS),
    #     'basis': parsing_intent(q),
    # }

    return intent

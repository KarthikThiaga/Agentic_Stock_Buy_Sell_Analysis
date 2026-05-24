from app.emit_event import emit_event

COMPARISON_KEYWORDS = ['compare', 'comparison', 'difference', 'good', 'best', 'better']

PRICE_KEYWORDS = ['price', 'trading', 'value', 'quote']
NEWS_KEYWORDS = ['news','update', 'happening', 'recent']
BUY_KEYWORDS = ['buy', 'invest','good', 'worth','analyse']


def parsing_intent(query):
    intents = []
    if any (word in query for word in PRICE_KEYWORDS):
        intents.append('price')
    if any (word in query for word in NEWS_KEYWORDS):
        intents.append('news')
    if any(word in query for word in BUY_KEYWORDS):
        intents.append('analysis')
    
    return intents

def get_intent(query):
    emit_event({'type': 'info', 'text': 'Parsing intent from query'})
    q = query.lower()

    intent = {
        'compare': any(word in q for word in COMPARISON_KEYWORDS),
        'basis': parsing_intent(q),
    }

    return intent

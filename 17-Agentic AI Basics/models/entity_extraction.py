import re
from app.emit_event import emit_event
from models.fuzzy_match import fuzzy_match
from storage.alias_read import load_alias_map
from storage.user_token_log import user_token_log
from config.logger import logging

COMPANY_DB = {
    'apple': 'AAPL',
    'nvidia': 'NVDA',
    'jpmorgan': 'JPM', 
    'google': 'GOOG',
    'microsoft': 'MSFT',
    'amazon': 'AMZN'
}

STOP_WORDS = ['compare', 'or', 'and', 'of', 'are', 'vs' ,'what']


alias_map = load_alias_map()
 
def entity_extraction(query):
    """Extracts unique financial entity objects from a text query using fuzzy matching.

    Tokenizes the incoming query by pulling out words, filtering against a collection 
    of stop words, and validating lengths. For each qualified token, it performs a 
    two-tiered fuzzy match lookup against the primary company database and an alias 
    map to resolve the corresponding corporate stock ticker symbol. Successfully 
    resolved tickers are compiled into a deduplicated list of initial placeholder objects.

    Args:
        query (str): The natural language input query string from the user.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing extracted entities. 
        Each dictionary contains placeholder slots for data metrics:
            {
                'ticker': str (the resolved ticker symbol),
                'price': None,
                'news': None,
                'financials': None
            }
    """


    # emit_event({'type': 'info', 'text': 'Extracting entities from query'})
    seen = set()
    words = re.findall(r'\b\w+\b', query.lower())
    tokens = [word for word in words if word not in STOP_WORDS]
    entities = []


    for token in tokens:

        if len(token) > 3:
            try:
                company_name,logic,score = fuzzy_match(token,COMPANY_DB.keys())
            except Exception as ex_fuzzy:
                logging.exception(f'event=entity_extraction tool=fuzzy_match map=company_DB token={token} msg={ex_fuzzy}')
                print(f'ERROR: Fuzzy matching failed for token {token} - {ex_fuzzy}')
                company_name = None

            if not company_name:
                try:
                    company_name,logic,score = fuzzy_match(token,alias_map.keys())
                except Exception as ex_fuzzy_alias:
                    logging.exception(f'event=entity_extraction tool=fuzzy_match map=alias_map token={token} msg={ex_fuzzy_alias}')
                    print(f'ERROR: Fuzzy matching failed for token {token} in alias map - {ex_fuzzy_alias}')
                    company_name = None

            if  company_name:
                if company_name in alias_map:
                    ticker = alias_map[company_name]
                elif company_name in COMPANY_DB:
                    ticker = COMPANY_DB[company_name]

                user_token_log(token,score,ticker,logic)

                if ticker not in seen:

                    entity = {
                        'ticker': ticker,
                        'price': None,
                        'news': None,
                        'financials': None
                    }
                    seen.add(ticker)
                    entities.append(entity)
            

    return entities
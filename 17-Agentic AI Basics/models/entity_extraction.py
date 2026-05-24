import re
from app.emit_event import emit_event
from models.fuzzy_match import fuzzy_match
from storage.alias_read import load_alias_map
from storage.user_token_log import user_token_log

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
    emit_event({'type': 'info', 'text': 'Extracting entities from query'})
    seen = set()
    words = re.findall(r'\b\w+\b', query.lower())
    tokens = [word for word in words if word not in STOP_WORDS]
    entities = []


    for token in tokens:

        if len(token) > 3:
            try:
                company_name,logic,score = fuzzy_match(token,COMPANY_DB.keys())
            except Exception as ex_fuzzy:
                print(f'ERROR: Fuzzy matching failed for token {token} - {ex_fuzzy}')
                company_name = None

            if not company_name:
                try:
                    company_name,logic,score = fuzzy_match(token,alias_map.keys())
                except Exception as ex_fuzzy_alias:
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
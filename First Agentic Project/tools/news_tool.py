
from tools.api_call import api_call
from app.emit_event import emit_event
from datetime import datetime
from storage.read_memory import read_memory
from tools.get_from_memory import get_from_memory
from tools.update_memory import update_memory
from config.logger import logger
import json

def get_news(ticker,config):
    """Retrieves, caches, and compiles the most recent news headlines for a given ticker.

    Coordinates historical or ongoing news stream extraction by first checking local caching 
    tables (memory) against the current calendar day to minimize redundant outbound network 
    requests. If a cache miss occurs, the function dispatches an query to the designated external 
    news repository using the company ticker symbol scoped strictly to headline titles. It attempts 
    to parse and isolate the first six articles from the payload response, commits the collected 
    headlines array back to persistent memory, and handles collection or validation anomalies.

    Args:
        ticker (str): The unique financial asset abbreviation identifier (e.g., 'AAPL').
        config (Dict[str, Any]): A configuration dictionary containing access keys and endpoint parameters:
            - "url" (str): The primary api dataset routing destination address for news queries.
            - "key" (str): The api authorization token.

    Returns:
        List[str]: A list containing up to six recent news article headline strings. Returns 
        an empty list if parsing or indexing constraints fail.

    Raises:
        Exception: If the provided `ticker` argument evaluates to an empty or falsy value.
    """

    if not ticker:
        logger.exception(f'event=get_news msg=Ticker missing for news fetch')
        raise Exception('Ticker missing for news fetch')
    
    current_date = datetime.date(datetime.now())
    memory = read_memory()

    news = get_from_memory(memory,ticker, current_date, 'news')

    if news:
        return news
    

    recent_news = []

    api_url = config.get("url")
    api_key = config.get("key")


    params = {
        "q":ticker,
        "searchIn": "title",
        "apiKey": api_key
    }


    response = api_call(ticker,api_url,params,'news')
    try:    
        res = response
        i=0
        while i < 6:
            news = (res['articles'][i]['title'])
            recent_news.append(news)
            i += 1

        details = {
            'news': recent_news
        }
        update_memory(memory,ticker,current_date,details)
        
    except Exception as ex2:
        logger.exception(f'event=get_news operation=parsing ticker={ticker} exception={ex2}')
        # print(f"get_news function exception: {ex2}")
        emit_event({'type': 'error', 'text': f'Failed to fetch news for {ticker}'}) 
    

    return recent_news
 

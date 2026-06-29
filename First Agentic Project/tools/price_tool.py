from tools.api_call import api_call
from datetime import datetime
from tools.get_from_memory import get_from_memory
from tools.update_memory import update_memory
from storage.read_memory import read_memory
from config.logger import logger



def get_price(ticker,config):

    """Retrieves, caches, and returns the current stock price for a specified ticker.

    Coordinates stock price extraction by first inspecting local caching tables (memory)
    against the current calendar execution date to minimize redundant outbound network
    requests. If a cache miss occurs, the function dispatches a request to the designated
    external asset pricing repository. Upon receiving a valid response, it extracts the
    latest closing or current price market marker, commits that value back to persistent
    session state memory, and handles payload mapping anomalies by falling back to a zero value.

    Args:
        ticker (str): The unique financial asset abbreviation identifier (e.g., 'AAPL').
        config (Dict[str, Any]): A configuration dictionary containing access keys and endpoint parameters:
            - "url" (str): The primary api dataset routing destination address for pricing data.
            - "key" (str): The api authorization token.

    Returns:
        float | int: The active asset transaction price matching the target asset if found; 
        otherwise, returns 0 if parsing or indexing constraints fail.
    """

    current_date = datetime.date(datetime.now())

    memory = read_memory()

    
    cache_price = get_from_memory(memory,ticker,current_date,'price')


    if cache_price:
        return cache_price
    
    api_url = config.get("url")
    api_key = config.get("key")

    params = { 
        "symbol": ticker,
        "token": api_key
    }

    response = api_call(ticker,api_url,params,'price')


    try:
        if response:
            price = response['c']
            details = {
                "price": price
            }

            update_memory(memory,ticker,current_date,details)

    
    except Exception as ex2:
        logger.exception(f'event=get_price operation=parsing ticker={ticker} exception={ex2}')
        # print(f"get_price function exception: {ex2}")
        price = 0

    
    
    return price

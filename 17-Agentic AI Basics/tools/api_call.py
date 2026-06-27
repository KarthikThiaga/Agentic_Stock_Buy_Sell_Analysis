import requests
from requests.exceptions import HTTPError, RequestException
from app.emit_event import emit_event
from config.logger import logger


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0'
}

def api_call(ticker,url,params,field):
    """Executes an HTTP GET request to fetch target financial metrics for a specific ticker.

    Sends an authenticated or parameterized network request to a designated external api 
    endpoint utilizing browser-impersonating request headers. On verification of a successful 
    HTTP transaction status, it deserializes the transmission packet. If execution anomalies 
    occur—such as an empty ticker parameter validation trigger, specific HTTP validation failures, 
    or underlying connection drops—the function records standard traceback logs, notifies downstream 
    channels via frontend events, and falls back to a string literal representation.

    Args:
        ticker (str): The unique financial asset abbreviation identifier (e.g., 'AAPL').
        url (str): The target REST api base endpoint routing address.
        params (Dict[str, Any]): A collection of query string parameters containing access keys, 
            tokens, filtering conditions, or format specifications.
        field (str): The logical financial dataset attribute category being pulled (such as 
            'price', 'news', or 'financials').

    Returns:
        Dict[str, Any] | str: The deserialized JSON payload structure if the server transaction 
        succeeds; otherwise, returns the string literal 'none' if an HTTP error or generic 
        request connection failure is handled.

    Raises:
        Exception: If the provided `ticker` argument evaluates to an empty or falsy value.
    """
    
    if not ticker:
        logger.exception(
            f'event=api_call'
            f'ticker: Empty' 
            f'status=failure' 
            f'exception=Ticker missing for {field} fetch'
            )
        raise Exception(f'Ticker missing for {field} fetch')
        

    api_url = url

    try:
        response = requests.get(api_url,params=params, headers=HEADERS)

        response.raise_for_status()
        
        resp = response.json()

        logger.info(
            f'event=api_call'
            f'ticker={ticker}'
            f'field={field}'
            f'status=success')
        
        return(resp)
    
    except HTTPError as ex1:
        logger.exception(
            f'event=api_call'
            f'ticker={ticker}'
            f'field={field}'
            f'status=HTTPError'
            f'status_code= {ex1.response.status_code}' 
            f'exception={ex1}')
        emit_event({'type': 'error', 'text': f'Failed to fetch {field} for {ticker} status_code {ex1.response.status_code}'})
        response = 'none'
        return response

    except RequestException as ex2:

        logger.exception(
            f'event=api_call'
            f'ticker={ticker}'
            f'field={field}'
            f'status=RequestException'
            f'status_code= {ex2.response.status_code}' 
            f'exception={ex2}')
        emit_event({'type': 'error', 'text': f'Failed to fetch {field} for {ticker} status_code {ex2.response.status_code}'})
        response = 'none'
        return response

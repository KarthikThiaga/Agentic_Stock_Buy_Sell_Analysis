from tools.api_call import api_call
from tools.resolve_metric import resolve_metric
from tools.compute_metric import compute_metric
from datetime import datetime
from storage.read_memory import read_memory
from tools.get_from_memory import get_from_memory
from tools.update_memory import update_memory
from config.logger import logger


def get_financial_reports(ticker,config):

    """Retrieves, caches, and processes corporate financial statements for a specified ticker.

    Coordinates historical balance sheet evaluation by first checking local caching tables 
    (memory) against the current calendar execution date to minimize redundant network I/O. 
    If a cache miss occurs, it targets a structured REST API endpoint to pull multiple years 
    of data. It then isolates the most recent reporting cycle, parses row labels through a metric 
    resolution engine using a heuristic scoring metric to find optimal matches, extracts relevant values, 
    and passes them to a computation utility. Finally, it records the newly evaluated data structure 
    back into persistent storage before delivery.

    Args:
        ticker (str): The unique financial asset abbreviation identifier (e.g., 'AAPL').
        config (Dict[str, Any]): A configuration dictionary containing access keys and endpoint parameters:
            - "url" (str): The primary api dataset routing destination address.
            - "key" (str): The api authorization token.

    Returns:
        Dict[str, int | float]: A dictionary containing calculated accounting metrics and 
        financial health indicators for the latest fiscal period. Returns an empty dictionary 
        if the API service returns a validation failure string or if structural data parsing errors occur.
    """
    
    current_date = datetime.date(datetime.now())
    memory = read_memory()
    
    cached_fin = get_from_memory(memory,ticker,current_date,'financials')

    if cached_fin:
        return cached_fin
                
    annual_data = {}
    api_url = config.get("url")
    api_key = config.get("key")

    params = { 
        "symbol": ticker,
        "token": api_key
    }
    
    response = api_call(ticker,url=api_url, params=params, field='financials')

    try:
        if response == 'none':
            return annual_data
        else:
            data = response['data']
            current_data = max(data, key=lambda x: x['year'])
            curr_year = current_data['year']
            annual_data[curr_year] = {}
            reports = current_data['report']['bs']

            metric_store = {}
            for details in reports:
                key, score = resolve_metric(details['label'])
                if key:
                    current = metric_store.get(key)
                    if current:
                        current_score = current.get('score', 0)
                    else:
                        current_score = 0
                    if not current or score > current_score:
                        metric_store[key] = {
                            "value": details['value'],
                            "score": score,
                            "label": details["label"]
                        }
                    

            annual_data[curr_year] = {
                k: v['value'] for k, v in metric_store.items()
            }



    except Exception as ex3:
        logger.exception(f'event=get_financial_reports operation=parsing status=failure exception={ex3}')
        print(f"get_financial_report function exception: {ex3}")
        return {}

    financial_data = compute_metric(annual_data,curr_year)
    details = {
        'financials': financial_data
    }
    memory = read_memory()
    update_memory(memory,ticker,current_date,details)
    
    return financial_data

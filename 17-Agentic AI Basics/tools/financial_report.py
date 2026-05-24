from tools.api_call import api_call
from tools.resolve_metric import resolve_metric
from tools.compute_metric import compute_metric
from datetime import datetime
from storage.read_memory import read_memory
from tools.get_from_memory import get_from_memory
from tools.update_memory import update_memory


def get_financial_reports(ticker,url):
    
    current_date = datetime.date(datetime.now())
    memory = read_memory()
    
    cached_fin = get_from_memory(memory,ticker,current_date,'financials')

    if cached_fin:
        return cached_fin
                
    annual_data = {}
    api_url = url
    params = { 
        "symbol": ticker,
        "token": 'd6v6jk9r01qig546muf0d6v6jk9r01qig546mufg'
    }
    
    response = api_call(ticker,api_url, params, 'financials')
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
        print(f"get_financial_report function exception: {ex3}")
        return {}

    financial_data = compute_metric(annual_data,curr_year)
    details = {
        'financials': financial_data
    }
    memory = read_memory()
    update_memory(memory,ticker,current_date,details)
    
    return financial_data

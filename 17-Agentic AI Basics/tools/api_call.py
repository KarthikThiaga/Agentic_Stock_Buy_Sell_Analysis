import requests
from app.emit_event import emit_event

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0'
}

def api_call(ticker,url,params,field):
    
    if not ticker:
        raise Exception(f'Ticker missing for {field} fetch')

    api_url = url

    try:
        response = requests.get(api_url,params=params, headers=HEADERS).json()
        return(response)
    except Exception as ex1:
        print(f"api call failed exception: {ex1}")
        emit_event({'type': 'error', 'text': f'Failed to fetch {field} for {ticker}'})
        response = 'none'
        return response


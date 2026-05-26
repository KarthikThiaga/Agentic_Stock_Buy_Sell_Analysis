
from tools.api_call import api_call
from app.emit_event import emit_event
from datetime import datetime
from storage.read_memory import read_memory
from tools.get_from_memory import get_from_memory
from tools.update_memory import update_memory
import json

def get_news(ticker,config):
    if not ticker:
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
        print(f"get_news function exception: {ex2}")
        emit_event({'type': 'error', 'text': f'Failed to fetch news for {ticker}'}) 
    

    return recent_news
 

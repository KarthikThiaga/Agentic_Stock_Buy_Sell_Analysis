from tools.api_call import api_call
from datetime import datetime
from tools.get_from_memory import get_from_memory
from tools.update_memory import update_memory
from storage.read_memory import read_memory



def get_price(ticker,config):

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
        print(f"get_price function exception: {ex2}")
        price = 0

    
    
    return price

from tools.api_call import api_call
from datetime import datetime
from tools.get_from_memory import get_from_memory
from tools.update_memory import update_memory
from storage.read_memory import read_memory



def get_price(ticker,url):

    print('into get_price')

    current_date = datetime.date(datetime.now())

    memory = read_memory()

    
    cache_price = get_from_memory(memory,ticker,current_date,'price')


    if cache_price:
        return cache_price
    
    api_url = url

    params = { 
        "symbol": ticker,
        "token": 'd6v6jk9r01qig546muf0d6v6jk9r01qig546mufg'
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

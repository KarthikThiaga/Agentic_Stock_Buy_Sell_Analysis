from tools.api_call import api_call
FALL_API_KEY = 'D5UBRFGP3EKH7ROG'

def fall_back_price(ticker,url):
    print(f"Falling back to secondary method for price for {ticker}")
    function = 'TIME_SERIES_DAILY'
    params = {
        'function': function,
        'symbol': ticker,
        'apikey': FALL_API_KEY
    }
    
    response = api_call(ticker,url,params=params,field='fallback_price')
    try:
        data = response
        time_series = data.get('Time Series (Daily)', {})
        if time_series:
            latest_date = sorted(time_series.keys())[-1]
            fallback_price = time_series[latest_date]['4. close']
            fallback_price = float(fallback_price)
        else:
            print(f"No time series data found for {ticker} in fallback API.")
    except Exception as e:
        print(f"Error parsing fallback API response for {ticker}: {e}")

    return fallback_price

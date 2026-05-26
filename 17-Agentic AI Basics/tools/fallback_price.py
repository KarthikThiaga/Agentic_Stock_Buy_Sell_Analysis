from tools.api_call import api_call


def fall_back_price(ticker,config):
    print(f"Falling back to secondary method for price for {ticker}")

    api_url = config.get("url")
    api_key = config.get("key")

    function = 'TIME_SERIES_DAILY'
    params = {
        'function': function,
        'symbol': ticker,
        'apikey': api_key
    }
    
    response = api_call(ticker,api_url,params=params,field='fallback_price')
    try:
        data = response
        time_series = data.get('Time Series (Daily)', {})
        if time_series:
            latest_date = sorted(time_series.keys())[-1]
            fallback_price = time_series[latest_date]['4. close']
            fallback_price = float(fallback_price)
        else:
            print(f"No time series data found for {ticker} in fallback API.")
            fallback_price = 0
    except Exception as e:
        print(f"Error parsing fallback API response for {ticker}: {e}")
        fallback_price = 0

    return fallback_price

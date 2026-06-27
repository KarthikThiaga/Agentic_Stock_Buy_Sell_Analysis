from tools.api_call import api_call
from config.logger import logger

def fall_back_price(ticker,config):
    """Retrieves and processes the latest daily closing price for a ticker via a secondary api channel.

    Acts as a failover routine when primary pricing data pathways are exhausted. The function 
    queries an external daily time-series repository, extracts the historical daily records mapping 
    to the target asset, sorts the date-string keys chronologically to identify the most recent market 
    date, and captures its closing price. If the tracking dataset is unavailable or an error occurs 
    during numeric type conversion, the pipeline defaults to a zero value and logs the exception details.

    Args:
        ticker (str): The unique financial asset abbreviation identifier (e.g., 'AAPL').
        config (Dict[str, Any]): A configuration dictionary containing access keys and endpoint parameters:
            - "url" (str): The fallback endpoint routing URL.
            - "key" (str): The api authorization token.

    Returns:
        float: The most recent daily closing asset price extracted from the vendor time series payload, 
        or 0.0 if data is missing or parsing task constraints fail.
    """
    logger.info(f'event=fall_back_finance msg=Falling back to secondary method for price for {ticker}')

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
        logger.exception(f'event=fall_back_price operation=parsing status=failure exception={e}')
        # print(f"Error parsing fallback API response for {ticker}: {e}")
        fallback_price = 0

    return fallback_price

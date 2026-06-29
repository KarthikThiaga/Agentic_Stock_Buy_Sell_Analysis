from tools.api_call import api_call
from datetime import datetime
from config.logger import logger



def fall_back_news(ticker,config):
    """Retrieves and processes recent news headlines for a ticker via a secondary api channel.

    Acts as a failover routine when primary news data streams are unavailable. The function 
    queries an external sentiment and news repository, extracts article feeds mapping to the target 
    asset, sorts them chronologically using the payload's publication timestamp format, and isolates 
    the top six most recent headlines.

    Args:
        ticker (str): The unique financial asset abbreviation identifier (e.g., 'AAPL').
        config (Dict[str, Any]): A configuration dictionary containing access keys and endpoint parameters:
            - "url" (str): The fallback endpoint routing URL.
            - "key" (str): The api authorization token.

    Returns:
        List[str]: A list of string headlines containing the titles of the six most recent news items. 
        Returns an empty list if an API connection failure occurs or if an error is handled during 
        response collection parsing.
    """
    logger.info(f'event=fall_back_finance msg=Falling back to secondary method for news for {ticker}')
    # print(f"Falling back to secondary method for news for {ticker}")
    api_url = config.get("url")
    api_key = config.get("key")
    
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "apikey": api_key
    }

    try:
        res = api_call(ticker, api_url, params=params, field='fallback_news')
        recent_news = []
        feed = res.get('feed', [])

        top_news = sorted(feed, key=lambda x: datetime.strptime(x['time_published'], '%Y%m%dT%H%M%S'), reverse=True)[:6]
        for items in top_news:
            recent_news.append(items['title'])

        return recent_news
    except Exception as e:
        logger.exception(f'event=fall_back_news operation=parsing status=failure exception={e}')
        # print(f"Error fetching news from fallback API for {ticker}: {e}")
        return []

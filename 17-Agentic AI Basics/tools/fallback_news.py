from tools.api_call import api_call
from datetime import datetime
FALL_API_KEY = 'D5UBRFGP3EKH7ROG'

def fall_back_news(ticker,url):
    print(f"Falling back to secondary method for news for {ticker}")
    url = url
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "apikey": FALL_API_KEY
    }

    try:
        res = api_call(ticker, url, params=params, field='fallback_news')
        recent_news = []
        feed = res.get('feed', [])

        top_news = sorted(feed, key=lambda x: datetime.strptime(x['time_published'], '%Y%m%dT%H%M%S'), reverse=True)[:6]
        for items in top_news:
            recent_news.append(items['title'])

        return recent_news
    except Exception as e:
        print(f"Error fetching news from fallback API for {ticker}: {e}")
        return None

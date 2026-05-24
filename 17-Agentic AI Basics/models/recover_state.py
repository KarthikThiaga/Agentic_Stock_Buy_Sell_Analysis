from tools.price_tool import get_price
from tools.news_tool import get_news
from tools.financial_report import get_financial_reports

PRICE_API_URL = "https://finnhub.io/api/v1/quote"
NEWS_API_URL = "https://newsapi.org/v2/everything"
FINANCIAL_REPORT_URL = "https://finnhub.io/api/v1/stock/financials-reported"


capabilities = {
    "price": get_price,
    "news": get_news,
    "financials": get_financial_reports
}

url_dict = {
    "price": PRICE_API_URL,
    "news": NEWS_API_URL,
    "financials": FINANCIAL_REPORT_URL
}

def recover_state(result, errors):
    retry_count = {}

    for err in errors:
        ticker = err['ticker']
        field = err['field']

        key = f"{ticker}_{field}"
        retry_count[key] = retry_count.get(key,0) + 1

        if retry_count[key] > 1:
            continue

        tool = capabilities.get(field)
        url = url_dict.get(field)

        if tool:
            try:
                result[ticker][field] = tool(ticker,url)
            except:
                continue
        
    return result

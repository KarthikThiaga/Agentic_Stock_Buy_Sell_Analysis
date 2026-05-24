
from core.generate_output_with_retries import generate_output_with_retries
from core.output_validation import output_validation
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


def primary_tool_execution(ticker, need):
    tool = capabilities.get(need)
    if tool:
        url = url_dict.get(need)
        output = generate_output_with_retries(ticker, url, tool, need, "primary", 2)
        if output is not None and output_validation(output, need):
            return output
    return None



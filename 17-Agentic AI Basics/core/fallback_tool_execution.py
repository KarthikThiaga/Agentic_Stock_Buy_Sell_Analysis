from tools.fallback_financials import fall_back_finance
from tools.fallback_news import fall_back_news
from tools.fallback_price import fall_back_price
from core.generate_output_with_retries import generate_output_with_retries
from core.output_validation import output_validation

FALLBACK_API_URL = 'https://www.alphavantage.co/query'

fall_back_capabilities = {
    "price": fall_back_price,
    "news": fall_back_news,
    "financials": fall_back_finance
}

def fallback_tool_execution(ticker, need):
    fallback_tool = fall_back_capabilities.get(need)
    if fallback_tool:
        url = FALLBACK_API_URL
        fallback_output = generate_output_with_retries(ticker, url, fallback_tool, need, "fallback", 2)
        if fallback_output is not None and output_validation(fallback_output, need):
            return fallback_output
    return None
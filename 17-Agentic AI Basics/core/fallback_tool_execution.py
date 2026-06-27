from tools.fallback_financials import fall_back_finance
from tools.fallback_news import fall_back_news
from tools.fallback_price import fall_back_price
from core.generate_output_with_retries import generate_output_with_retries
from core.output_validation import output_validation
from config.settings import Settings
from config.logger import logger

settings = Settings()

API_CONFIG = {
    "price": {
        "url": settings.PRICE_API_URL,
        "key": settings.PRICE_API_KEY
    },
    "news": {
        "url": settings.NEWS_API_URL,
        "key": settings.NEWS_API_KEY
    },
    "financials": {
        "url": settings.FINANCIAL_REPORT_URL,
        "key": settings.FINANCE_API_KEY
    },
    "fallback": {
        "url": settings.FALLBACK_API_URL,
        "key": settings.FALLBACK_API_KEY
    }
}

fall_back_capabilities = {
    "price": fall_back_price,
    "news": fall_back_news,
    "financials": fall_back_finance
}

def fallback_tool_execution(ticker, need):
    """Executes the fallback tool for a given financial data requirement.

    Retrieves the alternative (fallback) tool component mapped to the specified 
    data requirement ('need'). If available, it attempts to safely generate and 
    validate the fallback output with up to 2 execution retries using the 
    pre-configured fallback API settings.

    Args:
        ticker (str): The target financial stock ticker symbol (e.g., 'AAPL').
        need (str): The specific data metric required, such as 'price', 
            'news', or 'financials'.

    Returns:
        Any | None: The validated fallback data output payload if the 
        execution succeeds and passes validation; otherwise, None.
    """
    fallback_tool = fall_back_capabilities.get(need)
    if fallback_tool:
        config = API_CONFIG.get('fallback')
        fallback_output = generate_output_with_retries(ticker, config, fallback_tool, need, "fallback", 2)
        if fallback_output is not None and output_validation(fallback_output, need):
            return fallback_output
    return None
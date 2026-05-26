from tools.fallback_financials import fall_back_finance
from tools.fallback_news import fall_back_news
from tools.fallback_price import fall_back_price
from core.generate_output_with_retries import generate_output_with_retries
from core.output_validation import output_validation
from config.settings import Settings

API_CONFIG = {
    "price": {
        "url": Settings.PRICE_API_URL,
        "key": Settings.PRICE_API_KEY
    },
    "news": {
        "url": Settings.NEWS_API_URL,
        "key": Settings.NEWS_API_KEY
    },
    "financials": {
        "url": Settings.FINANCIAL_REPORT_URL,
        "key": Settings.FINANCE_API_KEY
    },
    "fallback": {
        "url": Settings.FALLBACK_API_URL,
        "key": Settings.FALLBACK_API_KEY
    }
}

fall_back_capabilities = {
    "price": fall_back_price,
    "news": fall_back_news,
    "financials": fall_back_finance
}

def fallback_tool_execution(ticker, need):
    fallback_tool = fall_back_capabilities.get(need)
    if fallback_tool:
        config = API_CONFIG.get('fallback')
        fallback_output = generate_output_with_retries(ticker, config, fallback_tool, need, "fallback", 2)
        if fallback_output is not None and output_validation(fallback_output, need):
            return fallback_output
    return None
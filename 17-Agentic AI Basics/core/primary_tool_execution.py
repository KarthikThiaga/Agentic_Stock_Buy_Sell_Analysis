
from core.generate_output_with_retries import generate_output_with_retries
from core.output_validation import output_validation
from tools.price_tool import get_price
from tools.news_tool import get_news
from tools.financial_report import get_financial_reports
from config.settings import Settings    
capabilities = {
    "price": get_price,
    "news": get_news,
    "financials": get_financial_reports
}

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


def primary_tool_execution(ticker, need):
    tool = capabilities.get(need)
    if tool:
        config = API_CONFIG.get(need)
        print(config)
        output = generate_output_with_retries(ticker, config, tool, need, "primary", 2)
        if output is not None and output_validation(output, need):
            return output
    return None



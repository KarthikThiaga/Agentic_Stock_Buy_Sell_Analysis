
from core.generate_output_with_retries import generate_output_with_retries
from core.output_validation import output_validation
from tools.price_tool import get_price
from tools.news_tool import get_news
from tools.financial_report import get_financial_reports
from config.settings import Settings    
from config.logger import logger
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
    """Executes the primary tool for a financial metric and validates its result.

    Looks up the primary tool capability mapped to the specified requirement ('need'). 
    If the tool is found, it attempts to execute it with up to 2 retries under 
    the "primary" path settings. It logs a success message if the output is 
    successfully generated and passes schema validation; otherwise, it logs a 
    failure and returns None.

    Args:
        ticker (str): The financial stock ticker symbol (e.g., 'AAPL').
        need (str): The specific metric or data requirement (e.g., 'price', 
            'news', 'financials').

    Returns:
        Any | None: The validated tool execution output payload if successful; 
        otherwise, None.
    """
    tool = capabilities.get(need)
    if tool:
        config = API_CONFIG.get(need)
        output = generate_output_with_retries(ticker, config, tool, need, "primary", 2)
        if output is not None and output_validation(output, need):
            logger.info(
            f"event=tool_start"
            f"ticker={ticker}"
            f"tool={need}"
            f"type=primary"
            f"status=success"
            )
            return output
        
        logger.info(
        f"event=tool_start"
        f"ticker={ticker}"
        f"tool={need}"
        f"type=primary"
        f"status=failure"
        )
    return None




from core.validate_financials import validate_financials
from config.settings import Settings

REQUIRED_STATE = {
    'price': lambda x: isinstance(x,(int,float)) and x>0,
    'news': lambda x: isinstance(x,list) and len(x) > 0,
    'financials': lambda x:validate_financials(x)
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

def retry_tool(ticker, tool, need):
    """Executes a target data-fetching tool with an integrated retry loop.

    This function attempts to fetch and validate metric data for a stock ticker 
    using the provided tool component. It dynamically extracts the matching API 
    configuration and rule-based validation schema, repeatedly executing the tool 
    up to a maximum of 2 additional retries if the initial response fails to pass 
    the data validation logic.

    Args:
        ticker (str): The stock ticker symbol to process (e.g., 'AAPL').
        tool (Callable): The metric-specific function component to execute.
        need (str): The target requirement identifier (e.g., 'price', 'news', 
            'financials') used for checking configs and lookup validation states.

    Returns:
        Any: The tool execution output payload once it passes validation rules, 
        or the last invalid output state generated if all retry thresholds 
        are exhausted.
    """
    retry_count = 0

    config = API_CONFIG.get(need)

    output = tool(ticker,config)
    rule = REQUIRED_STATE.get(need)
    while not rule(output) and retry_count < 2:
        output = tool(ticker,config)
        retry_count += 1

    return output 

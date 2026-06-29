from core.retry_tool import retry_tool
from storage.update_tool_stats import update_tool_stats
from tools.price_tool import get_price
from tools.news_tool import get_news
from tools.financial_report import get_financial_reports
from tools.fallback_financials import fall_back_finance
from tools.fallback_news import fall_back_news
from tools.fallback_price import fall_back_price
from config.logger import logger

capabilities = {
    "price": get_price,
    "news": get_news,
    "financials": get_financial_reports,
}

fall_back_capabilities = {
    "price": fall_back_price,
    "news": fall_back_news,
    "financials": fall_back_finance
}

def execute_with_retries(ticker, need, path):
    """Executes a tool with a retry mechanism and updates its performance statistics.

    This function selects the appropriate tool capability (either primary or 
    fallback) based on the execution path and target requirement ('need'). It 
    then attempts to execute the tool via a retry wrapper, logging the success 
    or failure outcome and updating historical tracking stats accordingly.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        need (str): The tool requirement key (e.g., 'price', 'news', 'financials').
        path (str): The chosen execution track, either "primary" or "fallback".

    Returns:
        Any | None: The validated execution output from the tool if successful; 
        None if the execution fails across all retries.
    """

    if path == "primary":
        tool = capabilities.get(need)
    else:
        tool = fall_back_capabilities.get(need) 

    output = retry_tool(ticker, tool, need)
    if output is not None:
        logger.info(
            f'event=execute_with_retries'
            f'ticker={ticker} tool={tool.__name__}'  
            f'path={path}' 
            f'status=success')
        update_tool_stats(need, path, True)
        return output
    else:
        update_tool_stats(need, path, False)
        logger.info(
            f'event=execute_with_retries'
            f'ticker={ticker} tool={tool.__name__}'  
            f'path={path}' 
            f'status=error')
        return None
from core.output_validation import output_validation
from storage.update_tool_stats import update_tool_stats
from config.logger import logger

def generate_output_with_retries(ticker, config, tool, need, path, max_retries):
    """Executes a given tool with an API configuration and validation retry loop.

    This function attempts to run the provided tool up to a specified maximum 
    number of retries. It passes the target stock ticker and configuration 
    settings to the tool, validates the resulting payload, and tracks the overall 
    success or failure history in the tool execution statistics.

    Args:
        ticker (str): The stock ticker symbol to pass to the tool (e.g., 'AAPL').
        config (Dict[str, Any]): Configuration settings (like API configurations) 
            required by the tool.
        tool (Callable): The tool function component to execute.
        need (str): The metric requirement name (e.g., 'price', 'news', 'financials').
        path (str): The active execution pathway, either "primary" or "fallback".
        max_retries (int): The maximum allowed attempts to successfully run 
            and validate the tool.

    Returns:
        Any | None: The validated tool output if execution succeeds within 
        the retry limit; otherwise, None.
    """
    retry_count = 0
    while retry_count < max_retries:
        try:    
            output = tool(ticker, config)
            if output_validation(output, need):
                update_tool_stats(need, path, True)
                return output
            retry_count += 1
        except Exception as e:
            logger.exception(f"event=generate_output_with_retries  tool={tool.__name__} exception={e}")
            retry_count += 1
    update_tool_stats(need, path, False)
    return None
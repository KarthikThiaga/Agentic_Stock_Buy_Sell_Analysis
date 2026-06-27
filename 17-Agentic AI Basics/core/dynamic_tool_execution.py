
from core.primary_tool_execution import primary_tool_execution 
from core.output_validation import output_validation
from core.fallback_tool_execution import fallback_tool_execution 
from core.choose_execution_path import choose_execution_path
from core.execute_with_retries  import execute_with_retries
from config.logger import logger



def dynamic_tool_execution(ticker, needs):
    """Executes a series of tools dynamically based on historical performance and validation.

    Iterates through a list of requirements ('needs') for a specific stock ticker. 
    For each requirement, it determines whether to route through a primary or 
    fallback execution path. If the chosen path fails validation, the function 
    attempts to recover by switching to the fallback path or invoking a retry 
    mechanism.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        needs (List[str]): A list of tool requirements to execute 
            (e.g., ['price', 'news', 'financials']).

    Returns:
        Dict[str, Any]: A dictionary mapping each successful 'need' to its 
        validated tool execution output.
    """
    result = {}
    for need in needs:
        execution_path = choose_execution_path(need)
        logger.info(
            f'event=tool_start',
            f'ticker={ticker}',
            f'tool={need}'
            f'selected_path={execution_path}'
        )

        if execution_path == "primary":
            output = primary_tool_execution(ticker, need)
            if output is not None and output_validation(output, need):
                result[need] = output
                continue
            else:
                logger.info(
                    f'event=tool_start',
                    f'ticker={ticker}',
                    f'tool={need}'
                    f'Changing from {execution_path} to Fallback'
        )
                output = fallback_tool_execution(ticker, need)
                if output is not None and output_validation(output, need):
                    result[need] = output
                    continue
                else:
                    execute_with_retries(ticker, need, "fallback")

        elif execution_path == "fallback":
            output = fallback_tool_execution(ticker, need)
            if output is not None and output_validation(output, need):
                result[need] = output
                continue
            else:
                output = fallback_tool_execution(ticker, need)
                if output is not None and output_validation(output, need):
                    result[need] = output
                    continue
                else:
                    execute_with_retries(ticker, need, "fallback")

    return result
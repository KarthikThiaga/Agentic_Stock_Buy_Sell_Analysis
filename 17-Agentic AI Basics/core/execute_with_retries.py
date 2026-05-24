from core.retry_tool import retry_tool
from storage.update_tool_stats import update_tool_stats

def execute_with_retries(ticker, tool, need):
    output = retry_tool(ticker, tool, need)
    if output is not None:
        update_tool_stats(need, "primary", True)
        return output
    else:
        update_tool_stats(need, "primary", False)
        return None
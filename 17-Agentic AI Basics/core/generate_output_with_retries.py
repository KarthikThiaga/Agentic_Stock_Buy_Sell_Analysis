from core.output_validation import output_validation
from storage.update_tool_stats import update_tool_stats

def generate_output_with_retries(ticker, url, tool, need, path, max_retries):
    retry_count = 0
    while retry_count < max_retries:
        output = tool(ticker,url)
        if output_validation(output, need):
            update_tool_stats(need, path, True)
            return output
        retry_count += 1

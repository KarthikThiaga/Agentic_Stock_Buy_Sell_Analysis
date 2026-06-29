import json 
from config.logger import logger
def write_tool_stats(data):
    """Serializes and persists performance tracking metrics to the tool statistics registry.

    Attempts to write the provided dictionary data structure into 'tool_stats.json' using 
    UTF-8 encoding and pretty-print indentation formatting. If the JSON serialization fails, 
    the error details are captured and logged. Generic file system errors or file access path 
    blockages are caught safely at the top level to avoid disrupting the system execution flow.

    Args:
        data (Dict[str, Any]): A dictionary containing tool execution configurations, 
            historical invocation counts, and tracking performance stats to persist.
    """
    try:
        with open('tool_stats.json','w',  encoding='utf-8') as file:
            try:
                json.dump(data, file, indent=4)
            except Exception as e1:
                logger.exception(f'event=write_tool_stats file=tool_stats.json operation=write status=failure exception={e1}')
    except Exception as ex_write_tool_stats:
        logger.exception(f'event=write_tool_stats file=tool_stats.json operation=open status=failure exception={ex_write_tool_stats}')

from config.logger import logger
import json


def read_tool_stats():
    """Reads and parses operational performance metrics from the local tool statistics registry.

    Attempts to open and load the JSON payload from 'tool_stats.json'. If the file contains 
    corrupted or malformed JSON data, the parser intercepts the error, records the failure details 
    via the configured system logger, and returns an empty fallback dictionary. If the target file 
    is missing, the function catches the `FileNotFoundError`, initializes a fresh tracking structure 
    by writing an empty dictionary template back out to disk, and logs the corrective creation action.

    Returns:
        Dict[str, Any]: A dictionary containing tool execution statistics and historical success metrics, 
        or an empty dictionary if any file operations, parsing errors, or missing file conditions are encountered.
    """
    try:
        with open('tool_stats.json','r') as file:
            try:
                content = file.read()
                data = json.loads(content)
                return data
            except Exception as ex1:
                logger.exception(f'event=read_tool_stats file=tool_stats.json operation=read/load status=failure exception={ex1}')
                return {}
    except FileNotFoundError:
        with open('tool_stats.json','w') as file:
            json.dump({}, file)
            logger.info(f'event=read_tool_stats file=tool_stats.json operation=create status=success msg=FIleNotFound')
            return {}
    except Exception as ex_tool_stats_file:
        logger.exception(f'event=read_tool_stats file=tool_stats.json operation=open status=failure msg=ex_tool_stats_file')
        # print(f'LOG: Opening tool_stats.json file - {ex_tool_stats_file}')
        return {}

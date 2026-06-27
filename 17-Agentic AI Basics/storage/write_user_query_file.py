import json
from config.logger import logger

def write_user_query_file(data):
    """Serializes and persists the updated user query log to a local JSON file.

    Attempts to write the provided dictionary data structure into 'user_query.json' 
    using UTF-8 encoding and pretty-print indentation formatting. If the JSON 
    serialization fails, the error details are recorded via the configured system 
    logger. Generic file system errors or file access path blockages are caught 
    safely at the top level to avoid disrupting the system execution flow.

    Args:
        data (Dict[str, Any]): A dictionary containing normalized user query terms 
            mapped to their resolution metadata, confidence scores, sources, and 
            invocation counters to persist.
    """
    try:
        with open('user_query.json','w',  encoding='utf-8') as file:
            try:
                json.dump(data, file, indent=4)
            except Exception as ex1:
                logger.exception(f'event=write_user_query_file file=user_query.json operation=write status=failure exception={ex1}')
    except Exception as ex_write_user_json:
        logger.exception(f'event=write_user_query_file file=user_query.json operation=open status=failure exception={ex_write_user_json}')
        # print(f'ERROR: while writing user_query.json file - {ex_write_user_json}')

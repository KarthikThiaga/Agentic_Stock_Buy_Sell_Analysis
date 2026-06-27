import json
from config.logger import logger

def read_user_query_file():
    """Reads and parses contextual information from the user queries history tracking storage.

    Attempts to open and read a JSON configuration file named 'user_query.json' using 
    UTF-8 encoding. If the file contains malformed JSON or fails to parse, it captures 
    the error, records the exception via the system logger, and returns an empty dictionary. 
    If the file does not exist, a new template file is initialized with an empty dictionary 
    JSON schema, logged as a successful fallback operation, and an empty dictionary is returned.

    Returns:
        Dict[str, Any]: The parsed data structure representing historical user queries and 
        matching tracking metadata, or an empty dictionary if any file operations, parsing 
        tasks, or missing file conditions are encountered.
    """
    try: 
        with open('user_query.json','r', encoding='utf-8') as file:
            try: 
                content = file.read()
                data = json.loads(content)
                return data
            except Exception as ex_json_read_error:
                logger.exception(f'event=read_user_query_file file=user_query.json operation=read/load status=failure exception={ex_json_read_error}')
                # print(f'ERROR: JSON read failed for user map - {ex_json_read_error}')
    except FileNotFoundError:
        with open('user_query.json', 'w') as file:
            file.write({})
            logger.info(f'event=read_user_query_file file=user_query.json operation=create msg=FileNotFound')
            return {}
    except Exception as ex_user_file:
        logger.exception(f'event=read_user_query_file file=user_query.json operation=open status=failure exception={ex_user_file}')
        # print(f'ERROR: user_query.json file open failed - {ex_user_file}')
        return {}

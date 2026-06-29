import json
from config.logger import logger

def read_memory():
    """Reads and parses contextual information from the local tracking memory storage.

    Attempts to open and read a JSON configuration file named 'memory.json'. If the 
    file contains malformed JSON or fails to parse, it captures the error, records 
    the exception via the system logger, and returns an empty dictionary. If the file 
    does not exist, a new placeholder 'memory.json' file is initialized with an empty 
    JSON schema, logged as a success event, and an empty dictionary is returned.

    Returns:
        Dict[str, Any]: The parsed data structure loaded from the memory registry, 
        or an empty dictionary if any file operations, parsing tasks, or file-not-found 
        conditions occur.
    """
    try:
        with open('memory.json','r') as r:
            try: 
                content = r.read()
                data = json.loads(content)
                return data
            except Exception as ex_json_read_error:
                logger.exception(f'event=read_memory file=memory.json opertion=read/load status=failure exception= {ex_json_read_error}')
                # print(f'ERROR: JSON read failed for user map - {ex_json_read_error}')
                return {}
    except FileNotFoundError:
        with open('memory.json', 'w') as file:
            file.write({})
            logger.info(f'event=read_memory file=memory.json opertion=create status=success msg=FileNotFound')
            return {}
    except Exception as ex_mem_file:
        logger.exception(f'event=read_memory file=memory.json opertion=open status=failure exception= {ex_mem_file}')
        # print(f'ERROR: memory.json file open failed - {ex_mem_file}')
        return {}

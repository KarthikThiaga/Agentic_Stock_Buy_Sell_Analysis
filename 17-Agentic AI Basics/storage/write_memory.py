import json
from config.logger import logger

def write_memory(memory):
    """Serializes and persists context state data back into local tracking memory storage.

    Attempts to write the provided memory data structure into 'memory.json' using 
    UTF-8 encoding and pretty-print indentation formatting. If the serialization 
    fails, the error is recorded via the configured system logger. If the target 
    file layout cannot be accessed due to missing structural references, it safely 
    re-initializes a fallback empty database schema block. All generic disk input/output 
    exceptions are caught and logged securely.

    Args:
        memory (Dict[str, Any]): The active session or state tracking map to be written 
            to persistent storage.

    Returns:
        Dict[str, Any] | None: Returns an empty dictionary container context if a top-level 
        file path access exception occurs; otherwise, returns None upon completion.
    """
    try:
        with open('memory.json','w', encoding='utf-8') as r:
            try: 
                json.dump(memory, r, indent=4)
            except Exception as ex_write_error:
                logger.exception(f'event=write_memory operation=write status=failure exception={ex_write_error}')
                # print(f'ERROR: JSON write failed for memory map - {ex_write_error}')
    except FileNotFoundError:
        with open('memory.json', 'w', encoding='utf-8') as file:
            file.write({})
        logger.info(f'event=write_memory operation=create status=success exception=FileNotFound')
        
    except Exception as ex_mem_file:
        logger.exception(f'event=write_memory operation=open status=failure exception={ex_mem_file}')
        # print(f'ERROR: memory.json file open while write failed - {ex_mem_file}')
        return {}

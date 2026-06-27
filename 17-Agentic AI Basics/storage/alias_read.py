
import json
from config.logger import logger

def load_alias_map():
    """Loads and deserializes the corporate alias mapping from a local JSON file.

    Attempts to read 'alias_map.json' using UTF-8 encoding and parse its contents 
    into a key-value dictionary. If the JSON payload is malformed, an exception is 
    logged and an empty mapping is returned. If the mapping file does not exist, 
    the function catches the `FileNotFoundError`, creates a fresh file containing 
    the empty dictionary template, and returns it.

    Returns:
        Dict[str, str]: A dictionary mapping resolved corporate names or variations 
        to their official ticker abbreviations. Returns an empty dictionary if the 
        file is empty, corrupted, or newly initialized.
    """
    alias_map = {}
    try:
        with open('alias_map.json','r', encoding='utf-8') as file:
            content = file.read()
            try:
                alias_map = json.loads(content)
            except Exception as ex_json:
                logger.exception(f'event=load_alias_map content={content} status=failure exception= {ex_json}')
                # print(f'ERROR: Error while loading ALIAS_MAP check {content} for exception {ex_json}')
    except FileNotFoundError:
        # print(f'ERROR: alias_map.json file not found - creation a new one')
        with open('alias_map.json','w') as file:
            json.dump(alias_map, file)
        logger.INFO(f'event=load_alias_map operation=open status=success msg=FileNotFound')
    except Exception as Ex2:
        print(f'ERROR: alias_map.json file not found - creation a new one - {Ex2}')
        logger.exception(f'event=load_alias_map operation=open status=failure exception= {Ex2}')

    return alias_map
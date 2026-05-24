
import json

def load_alias_map():
    alias_map = {}
    try:
        with open('alias_map.json','r', encoding='utf-8') as file:
            content = file.read()
            try:
                alias_map = json.loads(content)
            except Exception as ex_json:
                print(f'ERROR: Error while loading ALIAS_MAP check {content} for exception {ex_json}')
    except FileNotFoundError:
        print(f'ERROR: alias_map.json file not found - creation a new one')
        with open('alias_map.json','w') as file:
            json.dump(alias_map, file)
    except Exception as Ex2:
        print(f'ERROR: alias_map.json file not found - creation a new one - {Ex2}')

    return alias_map
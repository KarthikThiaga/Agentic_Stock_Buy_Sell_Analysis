import json

def read_memory():
    try:
        with open('memory.json','r') as r:
            try: 
                content = r.read()
                data = json.loads(content)
                return data
            except Exception as ex_json_read_error:
                print(f'ERROR: JSON read failed for user map - {ex_json_read_error}')
                return {}
    except FileNotFoundError:
        with open('memory.json', 'w') as file:
            file.write({})
            return {}
    except Exception as ex_mem_file:
        print(f'ERROR: memory.json file open failed - {ex_mem_file}')
        return {}

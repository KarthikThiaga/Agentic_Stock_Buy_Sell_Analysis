import json
def write_memory(memory):
    try:
        with open('memory.json','w', encoding='utf-8') as r:
            try: 
                json.dump(memory, r, indent=4)
            except Exception as ex_write_error:
                print(f'ERROR: JSON write failed for memory map - {ex_write_error}')
    except FileNotFoundError:
        with open('memory.json', 'w', encoding='utf-8') as file:
            file.write({})
    except Exception as ex_mem_file:
        print(f'ERROR: memory.json file open while write failed - {ex_mem_file}')
        return {}

import json

def read_user_query_file():
    try: 
        with open('user_query.json','r', encoding='utf-8') as file:
            try: 
                content = file.read()
                data = json.loads(content)
                return data
            except Exception as ex_json_read_error:
                print(f'ERROR: JSON read failed for user map - {ex_json_read_error}')
    except FileNotFoundError:
        with open('user_query.json', 'w') as file:
            file.write({})
            return {}
    except Exception as ex_user_file:
        print(f'ERROR: user_query.json file open failed - {ex_user_file}')
        return {}

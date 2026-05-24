import json
def write_user_query_file(data):
    try:
        with open('user_query.json','w',  encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    except Exception as ex_write_user_json:
        print(f'ERROR: while writing user_query.json file - {ex_write_user_json}')

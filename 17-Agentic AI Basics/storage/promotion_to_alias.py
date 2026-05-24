import json 

def promotion_to_alias():
    try:
        with open('user_query.json','r',encoding='utf-8') as file:
            content = file.read()
            user_data = json.loads(content) 
    except Exception as ex_read_user_query_file:
        print(f'LOG: Opening user_query.json in promotion_to_alias function - {ex_read_user_query_file}')
        return
    try:
        with open('alias_map.json','r',encoding='utf-8') as file:
            content = file.read()
            alias_data = json.loads(content)
    except Exception as ex_read_alias_map_file:
        print(f'LOG: Opening alias_map.json in promotion_to_alias function - {ex_read_alias_map_file}')
        return


    updated = False

    for query,info in user_data.items():
        if info['count'] >= 3 and info['confidence'] >= 80:
            resolved = info['resolved']

            if query not in alias_data:
                alias_data[query] = resolved
                print(f"PROMOTION: {query} → {resolved}")
                updated = True
        
    if updated:
        try:
            with open('alias_map.json','w') as f:
                json.dump(alias_data,f,indent=4)
        except Exception as ex_write_alias:
            print(f'LOG: promotion to alias failed and reason is {ex_write_alias}')



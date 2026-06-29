import json 
from config.logger import logger

def promotion_to_alias():
    """Promotes frequently matched user query terms to the official alias registry.

    Reads historical user query trends and the current alias mapping configurations. 
    If a tracked query term meets or exceeds a specific usage threshold (frequency >= 3) 
    and passes a strict identity classification check (confidence score >= 80), it is 
    "promoted" and appended to the persistent alias registry to streamline future string 
    resolutions.

    The function reads from 'user_query.json' and 'alias_map.json', evaluates eligibility, 
    and flushes any new additions back out to 'alias_map.json'. Failures during file 
    operations or deserialization tasks are intercepted and safely logged.
    """
    try:
        with open('user_query.json','r',encoding='utf-8') as file:
            content = file.read()
            user_data = json.loads(content) 
    except Exception as ex_read_user_query_file:
        logger.exception(f'event=promotion_to_alias operation=open file=user_query.json status=failure exception: {ex_read_user_query_file}')
        # print(f'LOG: Opening user_query.json in promotion_to_alias function - {ex_read_user_query_file}')
        return
    try:
        with open('alias_map.json','r',encoding='utf-8') as file:
            content = file.read()
            alias_data = json.loads(content)
    except Exception as ex_read_alias_map_file:
        logger.exception(f'event=promotion_to_alias operation=open file=alias_map.json status=failure exception={ex_read_alias_map_file}')
        # print(f'LOG: Opening alias_map.json in promotion_to_alias function - {ex_read_alias_map_file}')
        return


    updated = False

    for query,info in user_data.items():
        if info['count'] >= 3 and info['confidence'] >= 80:
            resolved = info['resolved']

            if query not in alias_data:
                alias_data[query] = resolved
                logger.info(f'event=promotion_to_alias content={resolved} updated status=success')
                # print(f"PROMOTION: {query} → {resolved}")
                updated = True
        
    if updated:
        try:
            with open('alias_map.json','w') as f:
                json.dump(alias_data,f,indent=4)
        except Exception as ex_write_alias:
            logger.exception(f'event=promotion_to_alias operation=write file=alias_map.json status=failure exception={ex_write_alias}')
            # print(f'LOG: promotion to alias failed and reason is {ex_write_alias}')



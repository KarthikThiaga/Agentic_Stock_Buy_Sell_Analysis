import json
import re
from tools.llmcall import llmcall   
from storage.prompt_map import get_prompt
from storage.user_token_log import user_token_log

def llm_entity_extraction(query,intent):
    
    print("LOG: Fuzzy extraction insufficient --> Triggering LLM")
    prompt = get_prompt('entity_extraction').format(query=query, intent=intent)
    
    try:
        resp = re.sub(r"```json|```", "", llmcall(prompt))
        print(resp)
        data = json.loads(resp)["entities"]

        list_of_entities = []
        try:
            for items in data:
                user_token_log(entity = items["input"],
                            match = items["resolved"],
                            score = int(items["confidence"] * 100),
                            logic = 'llm')
                list_of_entities.append(items["resolved"])
        except KeyError:
            print(f'ERROR: Clean prompt the response is {resp}')
        except Exception as ex_entity_error:
            print(f'ERROR: in llm_call to log user query = {ex_entity_error}')

        response = {
            "tickers": list_of_entities
        }
        
        return response

    except Exception as ex1:
        print(f'LLM response JSON load failed  - Exception is {ex1}')
        return None
import json
import re
from tools.llmcall import llmcall   
from storage.prompt_map import get_prompt
from storage.user_token_log import user_token_log
from config.logger import logger

def llm_entity_extraction(query,intent):
    """Extracts financial entities from a user query via an LLM fallback mechanism.

    This function triggers a Large Language Model (LLM) call when preliminary fuzzy 
    matching strategies prove insufficient. It formats a targeted prompt containing 
    the query and parsed intent, sanitizes the LLM's raw markdown/JSON string response, 
    parses it into structured entity records, and logs token resolution performance.

    Args:
        query (str): The original natural language input query string from the user.
        intent (Dict[str, Any]): The classified user intent metrics and configuration 
            flags used to contextualize the extraction.

    Returns:
        Dict[str, List[str]] | None: A dictionary containing a list of resolved ticker 
        symbols under the "tickers" key if successfully parsed; otherwise, None if 
        JSON loading or response processing fails.
    """
    
    logger.info("Fuzzy extraction insufficient --> Triggering LLM")
    prompt = get_prompt('entity_extraction').format(query=query, intent=intent)
    
    try:
        resp = re.sub(r"```json|```", "", llmcall(prompt))
        data = json.loads(resp)["entities"]

        list_of_entities = []
        
        try:
            for items in data:
                
                user_token_log(entity = items["input"],
                            match = items["resolved"],
                            score = int(items["confidence"] * 100),
                            logic = 'llm')
                list_of_entities.append(items["resolved"])

        except KeyError as ke:
            logger.exception(f'event=llm_entity_extraction llm_response={data} status=failure exception= ke')
            print(f'ERROR: Clean prompt the response is {resp}')
        except Exception as ex_entity_error:
            logger.exception(f'event=llm_entity_extraction llm_response={data} status=failure exception= ex_entity_error')
            print(f'ERROR: in llm_call to log user query = {ex_entity_error}')

        response = {
            "tickers": list_of_entities
        }
        
        return response

    except Exception as ex1:
        logger.exception(f'event=llm_entity_extraction status=failure exception= ex1')
        print(f'LLM response JSON load failed  - Exception is {ex1}')
        return None
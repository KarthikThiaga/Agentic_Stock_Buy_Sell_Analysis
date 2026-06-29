from models.entity_extraction import entity_extraction
from models.required_llm_call import required_llm_call
from models.intent_extraction import get_intent
from models.llm_entity_extract import llm_entity_extraction
from app import emit_event
from config.logger import logger

def extract_intent_entity(query):
    """Extracts parsed intent and target stock entities from a user query.

    Determines the basic operational intent and extracts financial entities using 
    standard matching. If necessary, a secondary Large Language Model (LLM) extraction 
    is triggered to unearth complex or hidden company references. It backfills newly 
    discovered assets into the entity tracking registry and validates comparative constraints 
    to ensure multi-entity workflows have sufficient context.

    Args:
        query (str): The natural language query string submitted by the user.

    Returns:
        Tuple[List[Dict[str, Any]] | str, Dict[str, Any] | str, Dict[str, bool]]: 
        A structured tuple containing:
            - entity (List[Dict] or "none"): A list of placeholder entity objects, 
              or "none" if extraction fails.
            - intent (Dict or "none"): The classification criteria mapping user 
              objectives, or "none" if extraction fails.
            - error (Dict): Dictionary tracking state violations (e.g., `{'invalid': True}` 
              or `{'duplicate': True}`).
    """
    error = {}
    intent = get_intent(query)
    entity = entity_extraction(query)

    call_llm = required_llm_call(entity,intent)

    if call_llm:
        logger.info(f'event=extract_intent_entity call_llm={call_llm}')
        company_names = llm_entity_extraction(query,intent)



        if not company_names:
            logger.error(f'event=extract_intent_entity company_names: not_found tool:llm_entity_extraction status=failed')
            emit_event({'type': 'info', 'text': "No entities found in query."})
            error.update({'invalid': True})
            return "none","none",error

        new_entries = []

        company_list = company_names.get('tickers',[])
            
        for ticker in company_list:
            exists = False 
            for items in entity:
                if ticker == items['ticker']:
                    exists = True
            
            if not exists:
                new_entity = {
                    'ticker': ticker,
                    'price': None,
                    'news': None,
                    'financials': None
                }
                new_entries.append(new_entity)


            entity.extend(new_entries)
    
    if intent['compare']:
        if len(entity) <=1:
            logger.error(f'event=extract_intent_entity company_names: duplicate_entity tool:llm_entity_extraction status=failed')
            error.update({'duplicate': True})
            return "none","none",error

    return entity,intent,error

from models.entity_extraction import entity_extraction
from models.required_llm_call import required_llm_call
from models.intent_extraction import get_intent
from models.llm_entity_extract import llm_entity_extraction
from app import emit_event

def extract_intent_entity(query):
    intent = get_intent(query)
    entity = entity_extraction(query)

    call_llm = required_llm_call(entity,intent)

    if call_llm:

        company_names = llm_entity_extraction(query,intent)

        if not company_names:
            emit_event({'type': 'info', 'text': "No entities found in query."})
            return "none","none"

        new_entries = []

        for ticker in company_names:
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
    
    return entity,intent

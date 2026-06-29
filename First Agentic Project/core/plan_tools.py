
from app.emit_event import emit_event
from config.logger import logger

def plan_tools(intent, entity):

    """Plans the specific data tools to execute based on user intent and target entities.

    This function determines a strategy list of tool names ('price', 'news', 
    'financials') required to fulfill a request. The logic evaluates the 
    'compare' flag and the evaluation topics ('basis') listed in the intent. 
    If an analysis is requested for a single entity, additional tools are 
    automatically added to provide a comprehensive dataset.

    Args:
        intent (Dict[str, Any]): A dictionary containing configuration flags 
            and data constraints, including a boolean 'compare' key and a list 
            or set under the 'basis' key.
        entity (List[str] | Any): The target entity or list of entities (such 
            as stock tickers) being analyzed.

    Returns:
        List[str]: A list of tool names mapping out the execution plan 
        (e.g., ['price', 'news', 'financials']). Returns an empty list if no 
        conditions match, which triggers an error log.

    Events Emitted:
        Emits an initial "info" level event via `emit_event` indicating that 
        the tool planning workflow has started.
    """

    emit_event({'type': 'info', 'text': 'Planning tools to execute based on intent and entities'})
    
    plan = []

    if intent['compare']:
        plan = ['price','news','financials']
    
    elif "analysis" in intent['basis']:
        plan = ['financials']

        if len(entity) == 1:
            plan.append('news')
            plan.append('price')        

    elif 'price' in intent['basis']:
        plan.append('price')
        if 'news' in intent['basis']:
            plan.append('news')
    
    elif 'news' in intent['basis']:
        plan.append('news') 
        if 'price' in intent['basis']:
            plan.append('price')
    
    else:
        logger.error(f'event=plan_tools intent={intent} entity={entity} status=failure')

    
    return plan

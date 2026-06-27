from core.plan_tools import plan_tools
from config.logger import logger

def get_requirements(intent, entity):

    """Compiles the required tool execution needs for each target stock entity.

    Validates that at least one stock entity is provided, maps out the necessary 
    tools by delegating to `plan_tools`, aligns the intent parameters, and maps 
    the planned tool requirements to each entity.

    Args:
        intent (Dict[str, Any]): A dictionary mapping user configuration details, 
            containing at least a boolean 'compare' key and evaluation fields.
        entity (List[Dict[str, Any]]): A list of extracted entity dictionaries, 
            where each item contains a 'ticker' identifier key.

    Returns:
        Tuple[List[Dict[str, Any]] | str, Dict[str, Any] | str]: A tuple containing:
            - required (List[Dict] or "none"): A collection of required entity-to-needs 
              mappings (e.g., `[{'entity': 'AAPL', 'needs': [...]}]`), or "none" if 
              no entities were found.
            - intent (Dict or "none"): The updated or updated evaluation intent dictionary, 
              or "none" if validation failed.
    """
        
    if len(entity) == 0:
        logger.error('event=get_requirements msg=no_entity_found status=failure')
        return "none","none"

    required = []
    req = plan_tools(intent, entity)
    
    if intent['compare']:
        intent['basis'] = req
        
    for enty in entity:
        new_req = {
            'entity': enty['ticker'],
            'needs': req
            }
        required.append(new_req)

    return required,intent

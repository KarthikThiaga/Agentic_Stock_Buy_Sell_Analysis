from core.plan_tools import plan_tools

def get_requirements(intent, entity):
        
    if len(entity) == 0:
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

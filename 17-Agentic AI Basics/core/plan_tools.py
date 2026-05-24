
from app.emit_event import emit_event

def plan_tools(intent, entity):

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
    
    elif 'news' in intent['basis']:
        plan.append('news') 

    
    return plan

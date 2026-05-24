def required_llm_call(entity, intent):
    if len(entity) == 0:
        return True
    elif intent['compare'] and len(entity) < 2:
        return True
    elif 'analysis' in intent['basis'] and len(entity) < 1:
        return True
    else:
        return False

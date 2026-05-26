
def get_reccomendation(intent):
    if intent['compare'] and set(intent['basis']) == {'price','news','financials'}:
        return 'compare'
    elif 'analysis' in intent['basis']:
        return 'analysis'
    else:
        return 'simple'

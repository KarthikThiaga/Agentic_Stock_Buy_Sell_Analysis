from core.validate_financials import validate_financials

REQUIRED_STATE = {
    'price': lambda x: isinstance(x,(int,float)) and x>0,
    'news': lambda x: isinstance(x,list) and len(x) > 0,
    'financials': lambda x:validate_financials(x)
}

def output_validation(output, need):
    rule = REQUIRED_STATE.get(need)
    if rule and rule(output):
        return True
    return False
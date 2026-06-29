from core.validate_financials import validate_financials

REQUIRED_STATE = {
    'price': lambda x: isinstance(x,(int,float)) and x>0,
    'news': lambda x: isinstance(x,list) and len(x) > 0,
    'financials': lambda x:validate_financials(x)
}

def output_validation(output, need):
    """Validates the tool execution output against specified metric rules.

    Checks if the provided output payload conforms to the data type and structural 
    constraints defined in `REQUIRED_STATE` for the given data requirement ('need').

    Args:
        output (Any): The data payload received from a tool execution to be validated.
        need (str): The specific metric requirement name (e.g., 'price', 
            'news', or 'financials') used to look up the validation rule.

    Returns:
        bool: True if a validation rule exists for the requirement and the 
        output passes its validation criteria; otherwise, False.
    """
    rule = REQUIRED_STATE.get(need)
    if rule and rule(output):
        return True
    return False

def get_reccomendation(intent):
    """Determines the data formatting recommendation based on user intent.

    Analyzes the 'compare' configuration flag and the 'basis' items inside 
    the provided intent dictionary to prescribe a matching output treatment 
    strategy ('compare', 'analysis', or 'simple').

    Args:
        intent (Dict[str, Any]): A dictionary mapping user configuration details, 
            containing a boolean 'compare' key and a list or set of metrics 
            under the 'basis' key.

    Returns:
        str: The formatting strategy directive, returning 'compare' for full comparative 
        evaluations, 'analysis' for analytical studies, and 'simple' for standard scenarios.
    """
    if intent['compare'] and set(intent['basis']) == {'price','news','financials'}:
        return 'compare'
    elif 'analysis' in intent['basis']:
        return 'analysis'
    else:
        return 'simple'

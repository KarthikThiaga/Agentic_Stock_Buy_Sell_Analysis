
from core.validate_financials import validate_financials

REQUIRED_STATE = {
    'price': lambda x: isinstance(x,(int,float)) and x>0,
    'news': lambda x: isinstance(x,list) and len(x) > 0,
    'financials': lambda x:validate_financials(x)
}

def validate_state(required, result):
    errors = []

    for req in required:
        ticker = req['entity']
        needs = req['needs']

        entity_data = result.get(ticker, {})

        for need in needs:
            rule = REQUIRED_STATE.get(need)
            if rule:
                value = entity_data.get(need)

                try:
                    if not rule(value):
                        errors.append(
                            {
                                'ticker': ticker,
                                'field': need,
                                'error': 'invalid'
                            }
                        )
                except:
                    errors.append(
                        {
                            'ticker': ticker,
                            'field': need,
                            'error': 'exception'
                        }
                    )
        
    return errors 


from core.validate_financials import validate_financials
from config.logger import logger

REQUIRED_STATE = {
    'price': lambda x: isinstance(x,(int,float)) and x>0,
    'news': lambda x: isinstance(x,list) and len(x) > 0,
    'financials': lambda x:validate_financials(x)
}

def validate_state(required, result):
    """Validates aggregated tool results against requirements and logs structured validation errors.

    This function cross-checks the structured execution results dictionary against a list 
    of requirements grouped by entity (ticker). It looks up lambda validation rules from 
    `REQUIRED_STATE` for each metric data type and captures detailed information if a metric 
    fails validation or if an exception is raised during validation evaluation.

    Args:
        required (List[Dict[str, Any]]): A list of dictionaries defining requested entities 
            and metrics. Example:
                [{'entity': 'AAPL', 'needs': ['price', 'news']}]
        result (Dict[str, Dict[str, Any]]): A nested dictionary containing fetched 
            tool metrics grouped by ticker symbol. Example:
                {'AAPL': {'price': 150.0, 'news': ['Headline']}}

    Returns:
        List[Dict[str, str]]: A list of error dictionaries containing context details for 
        each invalid or failing configuration. Structure of an error item:
            {
                'ticker': str (the stock ticker),
                'field': str (the metric type evaluated),
                'error': str (either 'invalid' or 'exception')
            }
    """
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
                        logger.error(f'event=validate_state ticker={ticker} field={need} error=invalid')
                        errors.append(
                            {
                                'ticker': ticker,
                                'field': need,
                                'error': 'invalid'
                            }
                        )
                except:
                    logger.exception(f'event=validate_state ticker={ticker} field={need} error=invalid')
                    errors.append(
                        {
                            'ticker': ticker,
                            'field': need,
                            'error': 'exception'
                        }
                    )
        
    return errors 

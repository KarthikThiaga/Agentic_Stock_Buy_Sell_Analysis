
from tools.price_tool import get_price
from tools.news_tool import get_news
from tools.financial_report import get_financial_reports
from tools.fallback_price import fall_back_price
from tools.fallback_news import fall_back_news
from tools.fallback_financials import fall_back_finance
from app.emit_event import emit_event  
from core.dynamic_tool_execution import dynamic_tool_execution


capabilities = {
    "price": get_price,
    "news": get_news,
    "financials": get_financial_reports
}

fall_back_capabilities = {
    "price": fall_back_price,
    "news": fall_back_news,
    "financials":  fall_back_finance
}

def execute_tool(required):
    """Executes multiple data-fetching tools for a list of target entities.

    This function processes a batch of requirements grouped by entity (such as a 
    stock ticker). It iterates through each entry, extracts the entity name and 
    its requested data needs (e.g., price, news, financials), and invokes the 
    dynamic tool execution workflow to retrieve and aggregate the results.

    Args:
        required (List[Dict[str, Any]]): A list of dictionaries where each item 
            specifies an entity and its associated requirements. 
            Example:
                [
                    {'entity': 'AAPL', 'needs': ['price', 'news']},
                    {'entity': 'MSFT', 'needs': ['financials']}
                ]

    Returns:
        Dict[str, Dict[str, Any]]: A nested dictionary mapping each entity to 
        its gathered data results. Returns an empty dictionary `{}` if a 
        `KeyError` or unexpected exception occurs during parsing.

    Events Emitted:
        Emits an initial "info" level event via `emit_event` indicating that 
        tool execution has commenced.
    """
    emit_event(
        {
            'type': 'info',
            'text': 'Executing tools to fetch required data'
        }
    )  
    result_dict = {}
    for entries in required:
        try:
            key_val = entries['entity']
        except KeyError:
            print ('Function: execute_tool -KeyError')
            return {}
        except Exception:
            print(f'Function: execute_tool - {Exception}')
            return {}

        if key_val not in result_dict:
            result_dict[key_val] = {}
        
        needs = entries['needs']
        result_dict[key_val].update(dynamic_tool_execution(key_val, needs))
        
    return result_dict
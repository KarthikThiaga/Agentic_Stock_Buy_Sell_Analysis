
from core.validate_financials import validate_financials

REQUIRED_STATE = {
    'price': lambda x: isinstance(x,(int,float)) and x>0,
    'news': lambda x: isinstance(x,list) and len(x) > 0,
    'financials': lambda x:validate_financials(x)
}

def retry_tool(ticker, tool, need):
    retry_count = 0

    output = tool(ticker)
    rule = REQUIRED_STATE.get(need)
    while not rule(output) and retry_count < 2:
        output = tool(ticker)
        retry_count += 1

    return output if rule(output) else None

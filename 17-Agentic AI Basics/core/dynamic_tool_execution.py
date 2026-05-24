
from core.primary_tool_execution import primary_tool_execution 
from core.output_validation import output_validation
from core.fallback_tool_execution import fallback_tool_execution 
from core.choose_execution_path import choose_execution_path

def dynamic_tool_execution(ticker, needs):
    result = {}
    for need in needs:
        execution_path = choose_execution_path(need)

        if execution_path == "primary":
            output = primary_tool_execution(ticker, need)
            if output is not None and output_validation(output, need):
                result[need] = output
                continue
            else:
                output = fallback_tool_execution(ticker, need)
                if output is not None and output_validation(output, need):
                    result[need] = output
                    continue
                else:
                    result[need] = None 

        elif execution_path == "fallback":
            output = fallback_tool_execution(ticker, need)
            if output is not None and output_validation(output, need):
                result[need] = output
                continue
            else:
                output = fallback_tool_execution(ticker, need)
                if output is not None and output_validation(output, need):
                    result[need] = output
                    continue
                else:
                    result[need] = None

    return result
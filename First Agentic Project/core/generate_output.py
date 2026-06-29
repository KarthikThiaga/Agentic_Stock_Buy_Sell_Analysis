from app.emit_event import emit_event
from core.format_output import format_output
from core.get_raw_summary import get_raw_summary
from core.get_reccomendation import get_reccomendation

def generate_output(result,intent):
    """Generates the final formatted output based on tool execution results and user intent.

    This function coordinates the output generation pipeline by emitting an 
    informational tracking event, compiling a raw text summary from the results 
    matching the given intent, determining a recommendation strategy, and formatting 
    the final output text accordingly.

    Args:
        result (Dict[str, Any]): The aggregated results returned from tool 
            executions.
        intent (str): The verified purpose or objective derived from the 
            user's interaction.

    Returns:
        str: The final formatted text block or LLM response generated for the user.
    """
    emit_event({
        'type': 'info',
        'text': 'Generating output based on fetched data and intent'
    })

    raw_summary = get_raw_summary(result,intent)

    recommendation = get_reccomendation(intent)

    final_output = format_output(raw_summary, recommendation)

    return final_output
    




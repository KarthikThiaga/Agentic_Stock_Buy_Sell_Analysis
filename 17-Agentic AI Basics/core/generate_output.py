from app.emit_event import emit_event
from core.format_output import format_output
from core.get_raw_summary import get_raw_summary
from core.get_reccomendation import get_reccomendation

def generate_output(result,intent):
    emit_event({
        'type': 'info',
        'text': 'Generating output based on fetched data and intent'
    })

    raw_summary = get_raw_summary(result,intent)

    recommendation = get_reccomendation(intent)

    final_output = format_output(raw_summary, recommendation)

    return final_output
    




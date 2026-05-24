from core.execute_tools import execute_tool
from core.validate_state import validate_state
from core.generate_output import generate_output
from models.get_requirements import get_requirements
from models.extract_intent_entity import extract_intent_entity
from storage.promotion_to_alias import promotion_to_alias
from app.emit_event import emit_event
import time 
from app import ui

StreamlitUI = ui.StreamlitUIDisplay()
memory = {}


def orchestator(query):
    #1. Extract intent and entity
    entity, intent = extract_intent_entity(query)

    #2. Get requirements based on intent and entity
    required, intent = get_requirements(intent, entity)

    if required == "none":
        emit_event({
            "type": "error",
            "text": "Sorry, I couldn't understand your query. Please try again with a different phrasing."
            })
        
        return
    
    #3. Execute tools based on requirements and get results
    result = execute_tool(required)

    #4. Validate state and if errors → recover state
    errors = validate_state(required, result)

    if errors:
        emit_event({
            "type": "error",
            "text": "Tool are having some issues fetching data, please try again later"
        })
        print(f"LOG: validation errors = {errors}")

    #5. Generate output based on result and intent
    output = generate_output(result, intent)

    emit_event({
        "type": "success",
        "text": "Here is the result for your query: "
    })
    emit_event({
        "type": "output",
        "text": output
    })


query = ui.display_ui()

submit_button = StreamlitUI.ui_button("Submit Query")
spinner = StreamlitUI.ui_spinner("Processing your query...")

if submit_button:
    if query.strip() == "":
        emit_event({
            "type": "error",
            "text": "Please enter a valid stock related query."
        })
    else:
        with spinner:
            time.sleep(2)  # Simulate processing time

            orchestator(query)
            

promotion_to_alias()


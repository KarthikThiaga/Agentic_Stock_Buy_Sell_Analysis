from core.execute_tools import execute_tool
from core.validate_state import validate_state
from core.generate_output import generate_output
from models.get_requirements import get_requirements
from models.extract_intent_entity import extract_intent_entity
from storage.promotion_to_alias import promotion_to_alias
from app.emit_event import emit_event
import time 
from app import ui
from config.settings import Settings
from config.logger import logger
from config.validate_config import validate_config

StreamlitUI = ui.StreamlitUIDisplay()
memory = {}


def orchestator(query):
    """Orchestrates the main request-response pipeline for processing stock market queries.

    Acts as the primary lifecycle manager for incoming natural language financial queries. 
    The orchestration sequence proceeds as follows:
    1. Extracts explicit intent identifiers and concrete named-entities (tickers) from the input string.
    2. Maps parsed parameters into discrete system execution requirements, issuing validation errors 
       via the Streamlit user interface if the scope is non-financial or missing references.
    3. Triggers dynamic execution tools to gather live pricing, metrics, or news feed payloads.
    4. Evaluates downstream state constraints to isolate or gracefully handle interface data gaps.
    5. Dispatches collected outputs to a localized response generation model and publishes state change 
       events back to application UI consumers.

    Args:
        query (str): The raw text financial or stock-related question submitted by the user.

    Returns:
        Dict[str, Any] | str: A unified pipeline evaluation summary mapping entities, intents, 
        tool results, structural errors, and generated markdown responses. Returns a fallback matching 
        status string ("none") if early request validation triggers a constraint violation.
    """
    logger.info('STARTING ORCHESTRATION')
    intent_errors = None

    #1. Extract intent and entity
    entity, intent,intent_errors = extract_intent_entity(query)

    if intent_errors:
        duplicate = intent_errors.get('duplicate', {})
        invalid = intent_errors.get('invalid')

        if duplicate:
            StreamlitUI.ui_error("Comparitive analysis should have more than one company")
            # return
            return {
                'entity': entity,
                'intent': intent,
                'intent_errors': intent_errors} 
        
        if invalid:
            StreamlitUI.ui_error("there is an issue with tool - Please try after sometime")
            # return
            return {
                'entity': entity,
                'intent': intent,
                'intent_errors': intent_errors}

    #2. Get requirements based on intent and entity
    required, intent = get_requirements(intent, entity)

    if required == "none":
        StreamlitUI.ui_error("Sorry, Please provide a query related to stocks")
        # return 
        return required 
    
    #3. Execute tools based on requirements and get results
    result = execute_tool(required)

    #4. Validate state and if errors → recover state
    errors = validate_state(required, result)

    if errors:
        emit_event({
            "type": "error",
            "text": "Tool are having some issues fetching data, please try again later"
        })
        logger.error('event=validate_state errors={errors}')


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
    logger.info('event=model result=success')

    return {
        'entity': entity,
        'intent': intent,
        'intent_errors': intent_errors,
        'required': required,
        'result': result,
        'errors': errors,
        'output': output
    }



settings = Settings()

errors = validate_config(settings)

if len(errors) > 0:
    logger.error(
        f'config=invalid'
        f'items={errors}'
        f'status=failed'
    )
    raise ValueError("Invalid Configuration")

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


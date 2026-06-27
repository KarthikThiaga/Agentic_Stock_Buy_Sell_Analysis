from storage.write_tool_stats import write_tool_stats
from storage.read_tool_stats import read_tool_stats
from config.logger import logger

def update_tool_stats(need, state, success):
    """Updates and commits run-time invocation performance tracking metrics for a given tool.

    Loads the current metrics snapshot, registers initial placeholder data schemas if the 
    requested tool ('need') is unmonitored, and increments total usage counters. Based 
    upon structural flags determining execution mode flow ('primary' or 'fallback') and 
    outcome validations ('success' boolean state), specific performance counters are 
    safely adjusted within independent error handling checkpoints. Once operations 
    conclude, the aggregated records are committed back to disk.

    Args:
        need (str): The functional capability or metric collection identifier being evaluated.
        state (str): The operational route matching the tool context ('primary' or 'fallback').
        success (bool): A evaluation flag representing whether the action concluded 
            successfully (True) or encountered errors/failures (False).
    """
    tool_stats = read_tool_stats()

    if need not in tool_stats:
        tool_stats[need] = {"calls": 0, "successes": 0, "failures": 0,"fallback successes": 0, "fallback failures": 0}

    try:
        tool_stats[need]["calls"] += 1
    except Exception as e:
        logger.exception(f'event=update_tool_stats need={need} operation=primary_call status=failure exception={e}')
        # print(f"Error updating calls for {need}: {e}")

    if success:
        if state == "fallback":
            try:
             tool_stats[need]["fallback successes"] += 1
            except Exception as e:
                logger.exception(f'event=update_tool_stats need={need} operation=fallback_success status=failure exception={e}')
                # print(f"Error updating fallback successes for {need}: {e}")
        elif state == "primary":
            try:
                tool_stats[need]["successes"] += 1
            except Exception as e:
                logger.exception(f'event=update_tool_stats need={need} operation=primary_success status=failure exception={e}')
                # print(f"Error updating successes for {need}: {e}")
        else:
            pass
    else:
        if state == "fallback":
            try:
                tool_stats[need]["fallback failures"] += 1
            except Exception as e:
                logger.exception(f'event=update_tool_stats need={need} operation=fallback_failure status=failure exception={e}')
                # print(f"Error updating fallback failures for {need}: {e}")
        elif state == "primary":
            try:
                tool_stats[need]["failures"] += 1
            except Exception as e:
                logger.exception(f'event=update_tool_stats need={need} operation=primary_failure status=failure exception={e}')
                # print(f"Error updating failures for {need}: {e}")
        else:
            pass

    write_tool_stats(tool_stats)


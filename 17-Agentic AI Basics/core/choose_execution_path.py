
from storage.read_tool_stats import read_tool_stats
from app.emit_event import emit_event



def choose_execution_path(need):
        """Determines the optimal tool execution path based on historical performance.

        This function analyzes the historical success and failure statistics for a given 
        tool requirement ('need'). If the tool has been called at least 50 times, has a 
        primary failure rate exceeding 50%, and its fallback mechanism has a rescue 
        success rate over 80%, it routes execution to the "fallback" path. Otherwise, 
        it defaults to the "primary" path.

        Args:
            need (str): The specific tool identifier or requirement to evaluate.

        Returns:
            str: The chosen execution path, either "primary" or "fallback".

        Events Emitted:
            Emits an "info" level event via `emit_event` containing a breakdown of the 
            tool's total calls, successes, failures, fallback successes, and fallback 
            failures if historical metrics exist for the provided key.
        """
        tool_stats = read_tool_stats()
    
        if need in tool_stats:
            stats = tool_stats[need]
            emit_event({
                "type": "info",
                "text": f"Tool stats for {need} - Calls: {stats['calls']}, Success: {stats['successes']}, Failure: {stats['failures']}, Fallback Successes: {stats['fallback successes']}, Fallback Failures: {stats['fallback failures']}"
            })

            if stats['calls'] >=50:
                  
                primary_failure_rate = (
                        stats['failures']/ stats['calls']
                )
                
                if stats['failures'] > 0:
                    failure_rescue_rate = (
                            stats['fallback successes']/stats['failure']
                    )
                else:
                    failure_rescue_rate = 0

                if (
                    primary_failure_rate > 0.5 
                    and failure_rescue_rate > 0.8 
                ):
                    return "fallback"
                    
            # if stats['failures'] > 0 and stats['fallback successes'] > 0: 
            #     print(f"Fallback success rate for {need}: {stats['fallback successes'] / stats['failures']}")
            #     if  stats['fallback successes'] / stats['failures'] > 0.5:
            #         logger.info(f'event=choose_execution_path  need={need} - path=fallback')
            #         return "fallback"
                
        return "primary"


from storage.read_tool_stats import read_tool_stats
from app.emit_event import emit_event


def choose_execution_path(need):
        tool_stats = read_tool_stats()
    
        if need in tool_stats:
            stats = tool_stats[need]
            emit_event({
                "type": "info",
                "text": f"Tool stats for {need} - Calls: {stats['calls']}, Success: {stats['successes']}, Failure: {stats['failures']}, Fallback Successes: {stats['fallback successes']}, Fallback Failures: {stats['fallback failures']}"
            })
            if stats['failures'] > 0 and stats['fallback successes'] > 0: 
                if  stats['fallback successes'] / stats['failures'] > 0.5:
                    return "fallback"
        
        return "primary"

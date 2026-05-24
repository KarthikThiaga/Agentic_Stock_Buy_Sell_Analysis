from storage.write_tool_stats import write_tool_stats
from storage.read_tool_stats import read_tool_stats

def update_tool_stats(need, state, success):
    tool_stats = read_tool_stats()
    if need not in tool_stats:
        tool_stats[need] = {"calls": 0, "successes": 0, "failures": 0,"fallback successes": 0, "fallback failures": 0}

    tool_stats[need]["calls"] += 1

    if success:
        if state == "fallback":
            tool_stats[need]["fallback successes"] += 1
        else:
            tool_stats[need]["successes"] += 1
    else:
        if state == "fallback":
            tool_stats[need]["fallback failures"] += 1
        else:
            tool_stats[need]["failures"] += 1

    write_tool_stats(tool_stats)


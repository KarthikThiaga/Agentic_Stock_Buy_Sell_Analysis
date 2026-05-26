from tools.llmcall import llmcall
from storage.prompt_map import get_prompt
def format_output(raw_summary, recommendation):
    if recommendation == 'compare':
        prompt = get_prompt('compare_prompt').format(raw_summary=raw_summary)
        return llmcall(prompt)
    elif recommendation == 'analysis':
        prompt = get_prompt('analyze_prompt').format(raw_summary=raw_summary)
        return llmcall(prompt)
    else:
        final_output = '\n'.join(raw_summary)
        return final_output
    
from tools.llmcall import llmcall
from storage.prompt_map import get_prompt
def format_output(raw_summary, recommendation):
    """Formats raw summary data into a final output string based on a recommendation strategy.

    Depending on the specified recommendation, this function formats the raw 
    summary data into a targeted Large Language Model (LLM) prompt to perform 
    either a comparative evaluation or a detailed analysis. If no specific 
    recommendation matches, it merges the raw summary text lines directly.

    Args:
        raw_summary (str | List[str]): The raw summary information or a list 
            of text lines to be formatted or processed by the LLM.
        recommendation (str): The processing strategy to apply. Expected 
            values include 'compare', 'analysis', or any other value for a 
            default plaintext merge.

    Returns:
        str: The generated response string from the LLM call if specialized 
        formatting is requested, or a single newline-joined string compiled 
        from the raw summary.
    """
    if recommendation == 'compare':
        prompt = get_prompt('compare_prompt').format(raw_summary=raw_summary)
        return llmcall(prompt)
    elif recommendation == 'analysis':
        prompt = get_prompt('analyze_prompt').format(raw_summary=raw_summary)
        return llmcall(prompt)
    else:
        final_output = '\n'.join(raw_summary)
        return final_output
    
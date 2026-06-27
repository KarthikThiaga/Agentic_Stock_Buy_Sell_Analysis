def get_prompt(prompt_name):
    """Retrieves the raw text content of a specified prompt from storage.

    Opens and reads a text file matching the provided prompt name from the 
    local `storage/` directory pathway.

    Args:
        prompt_name (str): The filename identifier of the target prompt 
            (excluding the `.txt` extension).

    Returns:
        str: The complete raw text content contained within the prompt file.
    """
    with open(f'storage/{prompt_name}.txt', 'r') as file:
        prompt = file.read()
    return prompt
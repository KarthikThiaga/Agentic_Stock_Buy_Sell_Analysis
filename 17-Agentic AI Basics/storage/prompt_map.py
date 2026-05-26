def get_prompt(prompt_name):
    with open(f'storage/{prompt_name}.txt', 'r') as file:
        prompt = file.read()
    return prompt
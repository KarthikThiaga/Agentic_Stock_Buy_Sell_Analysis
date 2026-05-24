from google import genai

def llmcall(prompt):
    client = genai.Client(api_key='AIzaSyBXxSjUUjhw9n8F1NFQXIfFf51sv6RA_EU')
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents={"text": prompt}
    )

    return (response.text)

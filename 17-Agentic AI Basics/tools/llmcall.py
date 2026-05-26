from google import genai
from config.settings import Settings

def llmcall(prompt):
    api_key = Settings.GEMINI_API_KEY
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents={"text": prompt}
    )

    return (response.text)

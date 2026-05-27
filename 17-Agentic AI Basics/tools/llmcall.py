from google import genai
from config.settings import Settings

def llmcall(prompt):
    settings = Settings()
    api_key = settings.GEMINI_API_KEY
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents={"text": prompt}
    )

    return (response.text)

import sys 
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)


try:
    from google import genai
except ModuleNotFoundError:
    logging.error('google module not found - Check requirements')
    sys.exit()

api_key = os.getenv('API_SECRET_KEY')

if api_key is None:
    logging.error('key not found')
    sys.exit()

logging.info('Started Application')
client = genai.Client(api_key=api_key)

try: 
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents={"text": "Why is the sky blue?"}
    )

    if not response or  not getattr(response,"text", None):
        logging.error('incorrect response received')
        sys.exit()

    with open('response.txt','a+') as file:
        file.write(response.text)

except Exception as ex:
    logging.error(f"API call failed: {type(ex).__name__} - {ex}")
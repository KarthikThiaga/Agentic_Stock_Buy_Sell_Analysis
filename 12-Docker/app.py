import logging
import sys
import os

logging.basicConfig(
     level=logging.INFO,
     format="%(asctime)s - %(levelname)s - %(message)s",
     handlers=[
          logging.StreamHandler(sys.stdout),
          logging.FileHandler('app.log')
     ]
)

try:
    from google import genai
    from flask import Flask 
#     from dotenv import load_dotenv
except ModuleNotFoundError:
     logging.error('modules not installed.check requirements')
     sys.exit()

print('app started')
# load_dotenv('config.env')

app = Flask(__name__)

@app.route('/')

def home():
     return 'containerized service running'


if __name__ == "__main__":
     app.run(host="0.0.0.0",port=5000)

api_key = os.getenv('API_SECRET_KEY')

if api_key is None:
     logging.error('Api key not found')
     sys.exit()
    
client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
          model="gemini-2.5-flash-lite",
        contents={"text": "Why is the sky blue?"}
     )
    
    try:
        with open('result.txt','a+') as file:
               file.write(response.text)
    except FileNotFoundError:
        logging.error('File not found while write')
        sys.exit()
    except Exception as ex1:
         logging.error(ex1)
         sys.exit()
     
    
    if not response or not getattr(response,"text", None):
        logging.error("Empty or malformed response received.")
        logging.debug(response)
        sys.exit()

     
          
          
except Exception as ex:
    logging.error(f"API call failed: {type(ex).__name__} - {ex}")
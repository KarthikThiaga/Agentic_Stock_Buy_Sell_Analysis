import sys 
import logging
import os
import json
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

try:
    import requests
except ModuleNotFoundError:
    logging.error('request not found while import check requirements')
    sys.exit()

try:
    from flask import Flask
except ModuleNotFoundError:
    logging.error('request not found while import check requirements')
    sys.exit()

API_URL = 'https://api.nasa.gov/planetary/apod'

API_KEY = os.getenv('API_KEY')

if API_KEY is None:
    logging.error('pass the api key')
    sys.exit()

PARAMS = {
    "api_key": API_KEY
}

print('Into App1')

app = Flask(__name__)
@app.route('/')
def main():
    try:
        start = time.time()
        response = requests.get(url=API_URL,params=PARAMS)
        print('Into App')
        if response.status_code != 200:
            logging.error(f"NASA API returned {response.status_code}")
            return {"error": "NASA API failure"}, 500
        latency = (time.time() - start) * 1000

        logging.info(f'NASA API Latency: {latency:2f}ms')

        with open('response.txt', 'a+') as file:
            file.write(response.text)

        return response.text

    except Exception as ex:
        logging.error(ex)
        return {"error": "internal server error"}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
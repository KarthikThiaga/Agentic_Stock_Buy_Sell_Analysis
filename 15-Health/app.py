import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s -%(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
        ,logging.FileHandler('app.log')
    ]

)

try:
    from flask import Flask
except ModuleNotFoundError:
    logging.error('flask module was not installed check requirements')
    sys.exit()


app = Flask(__name__)

@app.route("/")

def home():
    return "welcome to Flask App"

@app.route("/health")

def health():
    return {"status": "healthy"}, 200

@app.route("/fail")

def fail():
    logging.error("Simulation Error")
    raise Exception("Simulation Error")
    

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
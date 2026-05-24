import sys
try:
    from flask import Flask
except ModuleNotFoundError:
    print('flask module not present check requirements')
    sys.exit()

app = Flask(__name__)
@app.route('/')


def home():
    print('Welcome to my first container')
    return 'Welcome to my first container'

print(__name__)

app.run(host="0.0.0.0",port=5000)



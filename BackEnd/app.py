import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv()
name = os.getenv("DB_NAME")
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    print(f"Database name: {name}")
    # app.run()

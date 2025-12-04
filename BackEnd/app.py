
from flask import Flask
from database.engine.db_engine import DBEngine as Engine

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    engine = Engine.get_engine()
    #app.run()

#!/usr/bin/python3
"""
0. Hello Flask!
Script that starts a Flask web application.
$ export FLASK_APP=0-hello_route.py
python3 -m web_flask.0-hello_route
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """response text"""
    return 'Hello HBNB!'

if __name__ == "__main__":
    app.run(host='0.0.0.0')

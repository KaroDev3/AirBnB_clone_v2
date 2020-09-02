#!/usr/bin/python3
"""
4. Is it a number?
script that starts a Flask web application
python3 -m web_flask.4-number_route
curl -Ls 0.0.0.0:5000/number/123 ; echo "" | cat -e
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """response text"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """response text"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """response text"""
    text = text.replace("_", " ")
    return 'C %s' % text


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """response text"""
    text = text.replace("_", " ")
    return 'Python %s' % text


@app.route('/number/<int:n>', strict_slashes=False)
def is_n(n):
    """response text"""
    if type(n) == int:
        return '%s is a number' % n


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

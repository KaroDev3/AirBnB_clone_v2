#!/usr/bin/python3
"""Initialize the flask class"""
from flask import Flask
import sys

app = Flask(__name__)

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

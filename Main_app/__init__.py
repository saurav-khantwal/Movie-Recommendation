from flask import Flask
import pandas as pd
import pickle

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True

else:
    app.debug = False

app.config['SECRET_KEY'] = '5252ff2ac905b9acd329d6e2'

from Main_app import routes



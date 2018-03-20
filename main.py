import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
        return 'Hello, World!'

@app.route('/health')
def healthcheck():
        return 'OK'

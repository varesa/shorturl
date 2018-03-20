import os
import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    if request.method == 'POST':
        return 'I create a new link'
    else:
        return 'Simple UI'

@app.route('/<short>')
def expand(short):
    return 'I expand ' + short + ' to the full URL'

@app.route('/health')
def healthcheck():
        return 'OK'

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    short = db.Column(db.String(8), unique=True, nullable=False)
    full  = db.Column(db.Text, nullable=False)

    created       = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    requested     = db.Column(db.DateTime, default=None)
    request_count = db.Column(db.Integer,  default=0)

    @staticmethod
    def request(short):
        link = Link.query.filter_by(short=short)
        if link:
            link.requested = datetime.datetime.utcnow()
            link.request_count += 1
            return link.full
        else:
            return None

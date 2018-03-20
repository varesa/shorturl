import datetime
import os
import random
import string

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Initialize app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Database model

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    short = db.Column(db.String(8), unique=True, nullable=False)
    full  = db.Column(db.Text, nullable=False)

    created       = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    requested     = db.Column(db.DateTime, default=None)
    request_count = db.Column(db.Integer,  default=0)

    @staticmethod
    def request(short):
        link = Link.query.filter_by(short=short).first()
        if link:
            link.requested = datetime.datetime.utcnow()
            link.request_count += 1
            return link.full
        else:
            return None


# Generate a new link

def newkey():
    while True:
        key = ''.join([random.choice(string.ascii_lowercase) for _ in range(3)])
        if not Link.query.filter_by(short=key).first():
            return key


@app.route('/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        key = newkey()
        link = Link(short=key, full=request.form.get('url'))
        db.session.add(link)
        db.session.commit()
        return "https://s.esav.fi/" + key
    else:
        return 'Simple UI'


# Expand a short URL into a redirect

@app.route('/<short>')
def expand(short):
    url = Link.request(short)
    if url:
        return redirect(url)
    else:
        return 'No URL with key ' + short + ' found', 404


# Basic healthcheck for orchestration and monitoring

@app.route('/health')
def healthcheck():
    link = Link.request('health')
    if link:
        return 'OK'

    link = Link(short='health', full='https://shorturl.esav.fi/')
    db.session.add(link)
    db.session.commit()

    if Link.request('health'):
        return 'OK'
    else:
        return 'Err', 500


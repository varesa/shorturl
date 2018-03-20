import os
import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        return 'I create a new link'
    else:
        return 'Simple UI'

@app.route('/<short>')
def expand(short):
    url = Link.request(short)
    if url:
        return url
    else:
        return 'No URL with key ' + short + ' found', 404

@app.route('/health')
def healthcheck():
    link = Link.request('health')
    if link:
        return 'OK'

    link = Link(full='https://shorturl.esav.fi/')
    db.session.add(link)
    db.session.commit()

    if Link.request('health'):
        return 'OK'
    else:
        return 'Err', 500


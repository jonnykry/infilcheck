import os
from flask import Flask
import boto3
from models import db

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ['FLASK_SECRET_KEY']

head_bucket = os.environ['S3_HEAD_BUCKET']

s3 = boto3.resource('s3')

# Load default config and override config from an environment variable
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
    DEBUG=os.environ['FLASK_DEBUG'],
    USERNAME=os.environ['FLASK_USERNAME'],
    PASSWORD=os.environ['FLASK_PASSWORD'],
))

db.init_app(app)

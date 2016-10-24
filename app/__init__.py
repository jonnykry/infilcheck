import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import boto3

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super duper secret key xD'

head_bucket = 'se329-project2'

s3 = boto3.resource('s3')

# Load default config and override config from an environment variable
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
    DEBUG=True,
    USERNAME='admin',
    PASSWORD='admin',
))

db = SQLAlchemy(app)

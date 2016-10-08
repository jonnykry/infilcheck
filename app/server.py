import os
from flask import Flask, render_template, redirect
import boto3
import botocore

app = Flask(__name__, template_folder='templates')

s3 = boto3.resource('s3')

# Load default config and override config from an environment variable
app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, 'attendanceapp.db'),
    DEBUG=True,
    USERNAME='admin',
    PASSWORD='admin',
))
app.config.from_envvar('ATTENDANCEAPP_SETTINGS', silent=True)


@app.route('/')
def home():
    return dashboard()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/logout')
def logout():
    return redirect('/')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/upload', methods=['POST'])
def upload_video():
    # TODO:  Get userId
    user_id = '12345'
    head_bucket = 'se329-project2'

    bucket = s3.Bucket(head_bucket)
    exists = True

    try:
        s3.meta.client.head_bucket(Bucket=user_id)
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False

    if not exists:
        s3.create_bucket('se329-project2')

    # TODO: Store the POST data as a temporary `.mov` or `.mp4` file

    filepath = 'app/static/uploads'
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    filepath += '/temp.mp4'

    # TODO:  Uniquely identify each video upload
    s3.Object(head_bucket, user_id + '/temp.mp4').put(Body=open(filepath, 'rb'))

    return redirect('dashboard')

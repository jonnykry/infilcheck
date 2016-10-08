import os
from flask import Flask, render_template, redirect
import boto3

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
    user_id = 12345

    s3.create_bucket(Bucket=user_id)
    

    return redirect('dashboard')

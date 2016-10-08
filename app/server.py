import os
import flask
from flask import Flask, render_template, redirect , Response
import flask_login

import boto3


app = Flask(__name__, template_folder='templates')
app.secret_key = 'super secret string'

s3 = boto3.resource('s3')

# Load default config and override config from an environment variable
app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, 'attendanceapp.db'),
    DEBUG=True,
    USERNAME='admin',
    PASSWORD='admin',
))
app.config.from_envvar('ATTENDANCEAPP_SETTINGS', silent=True)




login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@app.route('/')
def home():
    return dashboard()

users = {'test@test.com': {'pw': '123'},'test2': {'pw': 'secret'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect('dashboard')



@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/upload', methods=['POST'])
def upload_video():

    # TODO:  Get userId
    user_id = 12345

    s3.create_bucket(Bucket=user_id)
    

    return redirect('dashboard')

@login_manager.unauthorized_handler
def unauthorized():
    return login()

#render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    email = flask.request.form['email']
    if flask.request.form['pass'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect('dashboard')

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id
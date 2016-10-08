import os

from flask import Flask, render_template, redirect , Response
from flask.ext.login import LoginManager, UserMixin, login_required

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




login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def home():
    return dashboard()



class User(UserMixin):
    # proxy for a database of users
    user_database = {"JohnDoe": ("JohnDoe", "John"),
                     "JaneDoe": ("JaneDoe", "Jane")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None



@app.route("/protected/",methods=["GET"])
@login_required
def protected():
    return Response(response="Hello Protected World!", status=200)



@app.route('/logout')
def logout():
    return redirect('/')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/upload', methods=['POST'])
def upload_video():
    return redirect('dashboard')

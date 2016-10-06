import os
from flask import Flask, render_template, redirect

app = Flask(__name__, template_folder='../templates')


# Load default config and override config from an environment variable
app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, 'attendanceapp.db'),
    DEBUG=True,
    USERNAME='admin',
    PASSWORD='admin',
))
app.config.from_envvar('ATTENDANCEAPP_SETTINGS', silent=True)



@app.route('/')
def hello():
    return login()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route("/logout")
def logout():
    return redirect('/')

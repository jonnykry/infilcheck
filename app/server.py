from __future__ import print_function
import os
import sys
import flask
import uuid
import ffmpy
from flask import Flask, request, render_template, redirect , Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, \
     check_password_hash
import flask_login
import boto3
import botocore

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

login_manager = flask_login.LoginManager()
login_manager.init_app(app)



@app.route('/')
def home():
    return dashboard()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(12), unique=True)
    passhash = db.Column(db.String(120), unique=True)
    pi_id = db.Column(db.String(120), unique=True)

    def __init__(self, email, password, phone):
        self.email = email
        self.set_password(password)
        self.phone = phone
        self.pi_id = str(uuid.uuid4())

    def set_password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passhash, password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("access_forbidden.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


@app.errorhandler(405)
def method_not_allowed_page(error):
    return render_template("method_not_allowed.html"), 405


@app.errorhandler(500)
def server_error_page(error):
    return render_template("server_error.html"), 500


@login_manager.user_loader
def user_loader(email):
    users = db.session.query(User).filter(User.email == email)

    if users is None:
        return;

    temp_user = None

    for user in users:
        print('User loader: ' + user.email, file=sys.stderr)
        temp_user = user

    if temp_user is None:
        return

    return temp_user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')

    if email is None:
        return

    password = request.form['pw']

    for user in db.session.query(User).filter(User.email == email):
        print('User loader: ' + user.email, file=sys.stderr)

        if user is None:
            return

        user.is_authenticated = user.check_password(password)

    return user


@login_manager.unauthorized_handler
def unauthorized():
    return login()


@app.route('/login', methods=['GET', 'POST'])
def login():

    if flask.request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['pass']

    for user in db.session.query(User).filter(User.email == email):
        print('Login Result: ' + user.email, file=sys.stderr)

        if user.check_password(password):
            flask_login.login_user(user)
            return redirect('dashboard')

    # TODO:  Send a bad request result

    return redirect('login_failed')

@app.route('/login_failed')
def login_failed():
    return render_template('login_failed.html')


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect('dashboard')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        phone = flask.request.form['phone']

        if email is not None and password is not None and phone is not None:
            print('Creating user: ' + email + ' ' + password, file=sys.stderr)
            user = User(email, password, phone)
            db.session.add(user)
            db.session.commit()

            flask_login.login_user(user)

            return redirect('dashboard')
        else:
            print('Error creating user: ' + email, file=sys.stderr)

    return render_template('register.html')


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/settings', methods=['GET', 'POST'])
@flask_login.login_required
def settings():
    return render_template('settings.html', user_data = flask_login.current_user)


@app.route('/live', methods=['GET', 'POST'])
@flask_login.login_required
def live():
    return render_template('live.html')


@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    user = username = flask_login.current_user
    user_id = user.id

    bucket = s3.Bucket(head_bucket)
    exists = True

    try:
        s3.meta.client.head_bucket(Bucket=head_bucket)
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False

    url_list = []

    if exists:
        for key in bucket.objects.all():
            url = get_bucket_url(bucket.name, key.key.rsplit('.', 1)[0])
            temp_user_id = key.key.rsplit('/', 1)[0]
            file_ext = key.key.rsplit('/', 1)[1]

            if int(temp_user_id) == user_id and url not in url_list:
                url_list.append(url)

    username = user.email.rsplit('@', 1)[0]

    return render_template('dashboard.html', username=username, urls=url_list)


@app.route('/upload', methods=['POST'])
def upload_video():
    if request.method == 'POST':
        pi_id = request.form['piid']
        user_to_update = None

        for user in db.session.query(User).filter(User.pi_id == pi_id):
            user_to_update = user
            break

        if user_to_update is None:
            return render_template('server_error.html')

        if not request.files:
            print('No file in POST request', file=sys.stderr)
            return redirect('dashboard')

        file = request.files.values()[0]
        filename = file.filename
        file.save('/tmp/' + filename)

        bucket = s3.Bucket(head_bucket)
        exists = True

        try:
            s3.meta.client.head_bucket(Bucket=head_bucket)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                exists = False

        if not exists:
            s3.create_bucket(head_bucket)

        filepath = '/tmp/'
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        filepath += '/' + filename

        # Set filename to end in `.gif` and place previous `/tmp/` video as new `/tmp/`
        new_filename = filename.rsplit('.', 1)[0] + '.gif'
        in_filepath = '/tmp/' + filename
        out_filepath = '/tmp/' + new_filename

        ff = ffmpy.FFmpeg(inputs={in_filepath: None}, outputs={out_filepath: None})
        ff.run()

        obj = s3.Object(head_bucket, str(user_to_update.id) + '/' + new_filename)
        obj.put(Body=open(out_filepath, 'rb'))
        obj.Acl().put(ACL='public-read')

        obj2 = s3.Object(head_bucket, str(user_to_update.id) + '/' + filename)
        obj2.put(Body=open(in_filepath, 'rb'))
        obj2.Acl().put(ACL='public-read')

    return redirect('dashboard')


def get_bucket_url(bucket, object_name):
    return 'https://s3.amazonaws.com/' + bucket + '/' + object_name

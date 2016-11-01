from __future__ import print_function
import os
import sys
import flask
import ffmpy
from flask import request, render_template, redirect
import flask_login
import botocore
from __init__ import db, app, s3, head_bucket
from models import User, Video, Flags, Pi
import uuid
from werkzeug.security import generate_password_hash
from datetime import datetime


login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route('/')
def home():
    return dashboard()


@app.errorhandler(403)
def forbidden_page(error):
    print('Error: ' + str(error), file=sys.stderr)
    return render_template("access_forbidden.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    print('Error: ' + str(error), file=sys.stderr)
    return render_template("page_not_found.html"), 404


@app.errorhandler(405)
def method_not_allowed_page(error):
    print('Error: ' + str(error), file=sys.stderr)
    return render_template("method_not_allowed.html"), 405


@app.errorhandler(500)
def server_error_page(error):
    print('Error: ' + str(error), file=sys.stderr)
    return render_template("server_error.html"), 500


@login_manager.user_loader
def user_loader(email):
    users = db.session.query(User).filter(User.email == email)

    if users is None:
        return

    temp_user = None

    for user in users:
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

    loaded_user = None

    # TODO:  Why the loop here if we only want one???
    for user in db.session.query(User).filter(User.email == email):
        if user is None:
            return

        user.is_authenticated = user.check_password(password)
        loaded_user = user

    return loaded_user


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
            user = User(email, password, phone)
            db.session.add(user)
            db.session.commit()

            flags = Flags(user.id, False, False, False)
            pi = Pi(user.id, datetime.utcnow())

            db.session.add(flags)
            db.session.add(pi)
            db.session.commit()

            flask_login.login_user(user)

            return redirect('dashboard')
        else:
            print('Error creating user: ' + str(email), file=sys.stderr)

    return render_template('register.html')


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/settings', methods=['GET', 'POST'])
@flask_login.login_required
def settings():
    if request.method == 'POST':
        email = request.form['email']
        curpassword = request.form['curpassword']
        password = request.form['password']
        phone = flask.request.form['phone']
        pi_id = flask.request.form['piid']

        current_user = User.query.filter_by(id=flask_login.current_user.id).first()

        if pi_id == 'true':
           current_user.pi_id = str(uuid.uuid4())

        if current_user.check_password(curpassword):
            current_user.passhash = generate_password_hash(password)

        current_user.email = email

        current_user.phone = phone

        db.session.commit()

        return redirect('settings')

    return render_template('settings.html', user_data = flask_login.current_user)


@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    user = flask_login.current_user
    user_id = user.id

    video_list = []
    for video in db.session.query(Video).filter(Video.user_id == user_id):
        video_list.append(video)

    username = user.email.rsplit('@', 1)[0]

    return render_template('dashboard.html', username=username, videos=video_list)


@app.route('/upload', methods=['POST'])
def upload_video():
    if request.method == 'POST':
        pi_id = request.form['piid']

        user_to_update = db.session.query(User).filter(User.pi_id == pi_id).first()

        if user_to_update is None:
            return render_template('server_error.html')

        if not request.files:
            print('No file in POST request', file=sys.stderr)
            return redirect('dashboard')

        file = request.files.values()[0]
        filename = file.filename
        file.save('/tmp/' + filename)

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

        user_bucket = str(user_to_update.id) + '/'

        ff = ffmpy.FFmpeg(inputs={in_filepath: None}, outputs={out_filepath: None})
        ff.run()

        obj = s3.Object(head_bucket, user_bucket + new_filename)
        obj.put(Body=open(out_filepath, 'rb'))
        obj.Acl().put(ACL='public-read')

        gif_url = get_bucket_url(head_bucket, user_bucket + new_filename)

        obj2 = s3.Object(head_bucket, user_bucket + filename)
        obj2.put(Body=open(in_filepath, 'rb'))
        obj2.Acl().put(ACL='public-read')

        vid_url = get_bucket_url(head_bucket, user_bucket + filename)

        # Update the Database for the video
        video = Video(user_to_update.id, vid_url, gif_url, datetime.utcnow())
        db.session.add(video)
        db.session.commit()

    return redirect('dashboard')


@app.route('/poll', methods=['POST'])
def poll():
    if request.method == 'POST':
        pi_id = request.form['piid']

        user = db.session.query(User).filter(User.pi_id == pi_id).first()

        if user is None:
            return flask.abort(404)

        flags = db.session.query(Flags).filter(Flags.user_id == user.id).first()
        pi_obj = db.session.query(Pi).filter(Pi.user_id == user.id).first()

        if flags is None or pi_obj is None:
            return flask.abort(404)

        update_settings = flags.request_update_settings

        settings_data = {}
        if update_settings is not False:
            settings_data = {
                'room_name': pi_obj.room_name,
                'capture_framerate': pi_obj.capture_framerate,
                'threshold_frame_count': pi_obj.threshold_frame_count,
                'output_framerate': pi_obj.output_framerate,
                'is_enabled': pi_obj.is_enabled
            }

        response = {
            'requests_picture': flags.request_picture,
            'requests_log': flags.request_log,
            'update_settings': flags.request_update_settings,
            'settings_data': settings_data
        }

        return flask.jsonify(response)


def get_bucket_url(bucket, object_name):
    return 'https://s3.amazonaws.com/' + bucket + '/' + object_name


if __name__ == '__main__':
    app.run()

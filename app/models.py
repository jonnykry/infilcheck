from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, \
     check_password_hash
import uuid

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(12), unique=True)
    passhash = db.Column(db.String(120), unique=True)
    pi_id = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime)

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


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    s3_video_url = db.Column(db.String(120))
    s3_gif_url = db.Column(db.String(120))
    created_at = db.Column(db.DateTime)

    def __init__(self, user_id, s3_video_url, s3_gif_url, created_at):
        self.user_id = user_id
        self.s3_video_url = s3_video_url
        self.s3_gif_url = s3_gif_url
        self.created_at = created_at

    def get_user_id(self):
        return self.user_id

    def get_s3_video_url(self):
        return self.s3_video_url

    def get_s3_gif_url(self):
        return self.s3_gif_url

    def get_created_at(self):
        return self.created_at

class Flags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    request_picture = db.Column(db.Boolean)
    request_log = db.Column(db.Boolean)
    request_update_settings = db.Column(db.Boolean)

    def __init__(self, user_id, request_picture, request_log, request_update_settings):
        self.user_id = user_id
        self.request_picture = request_picture
        self.request_log = request_log
        self.request_update_settings = request_update_settings

    def get_request_picture(self):
        return self.request_picture

    def get_request_log(self):
        return self.request_log

    def get_request_update_settings(self):
        return self.request_update_settings


class Pi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_name = db.Column(db.String(120))
    capture_framerate = db.Column(db.Integer)
    output_framerate = db.Column(db.Integer)
    threshold_frame_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

    def __init__(self, user_id, created_at):
        self.user_id = user_id
        self.room_name = "Room"
        self.capture_framerate = 32
        self.threshold_frame_count = 5
        self.output_framerate = 10
        self.created_at = created_at

    def get_user_id(self):
        return self.user_id

    def get_room_name(self):
        return self.room_name

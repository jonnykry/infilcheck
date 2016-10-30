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
    s3_url = db.Column(db.String(120))
    created_at = db.Column(db.DateTime)

    def __init__(self, user_id, s3_url, created_at):
        self.user_id = user_id
        self.s3_url = s3_url
        self.created_at = created_at

    def get_user_id(self):
        return self.user_id

    def get_s3_url(self):
        return self.s3_url

    def get_created_at(self):
        return self.created_at

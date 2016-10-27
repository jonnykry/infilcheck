from app.app import db


class Video(db.Model):
    __tablename__ = 'video'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, foreign_key=True)
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

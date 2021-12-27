from myapi.extensions import db
from sqlalchemy.dialects.postgresql import UUID


class News(db.Model):

    __tablename__="News"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("Users.id"), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    picture = db.Column(db.VARCHAR(2086), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=True)


    def __repr__(self):
        return "<Title %s by user_id %d>" % self.title, self.user_id

    def __init__(self, user_id=None, title=None, description=None, content=None, picture=None):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.content = content
        self.picture = picture

    def __str__(self):
        return 
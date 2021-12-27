from myapi.extensions import db


class Tag(db.Model):

    __tablename__="Tags"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("Users.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=True)


    def __repr__(self):
        return "<Name %s by user_id %d>" % self.name, self.user_id

    def __init__(self, user_id=None, name=None):
        self.user_id = user_id
        self.name = name


    def __str__(self):
        return 

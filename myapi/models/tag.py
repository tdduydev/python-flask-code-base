import datetime
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from flask_jwt_extended import current_user
from sqlalchemy import event
from myapi.extensions import db
from myapi.models import *


class Tag(db.Model):

    __tablename__ = "Tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    def __repr__(self):
        return "<Name %s by user_id %d>" % self.name, self.user_id

    def __init__(self, user_id=None, name=None):
        self.user_id = user_id
        self.name = name

    def __str__(self):
        return

# TRIGGERS


@event.listens_for(Tag, "before_insert")
def on_insert_trigger(mapper, connection, target):
    table = Role.__table__
    verify_jwt_in_request()
    user: User = current_user
    target.created_by = user.id


@event.listens_for(Tag, "before_update")
def on_update_trigger(mapper, connection, target):
    table = Role.__table__
    target.updated_at = datetime.datetime.now()

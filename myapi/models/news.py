import datetime
import json
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from sqlalchemy import event
from myapi import permissions
from myapi.extensions import db
from flask_jwt_extended import current_user
from sqlalchemy.dialects.postgresql import UUID

from myapi.models import *


class News(db.Model):

    __tablename__ = "News"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("Users.id"), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    picture = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

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

# TRIGGERS


@event.listens_for(News, "before_insert")
def on_insert_trigger(mapper, connection, target):
    table = Role.__table__
    verify_jwt_in_request()
    user: User = current_user
    target.created_by = user.id


@event.listens_for(News, "before_update")
def on_update_trigger(mapper, connection, target):
    table = Role.__table__
    target.updated_at = datetime.datetime.now()

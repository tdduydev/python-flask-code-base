
from datetime import datetime
import json
from sqlalchemy import event
from flask_jwt_extended import current_user
from myapi import permissions
from myapi.extensions import db
from myapi.models import *


class Category(db.Model):

    __tablename__ = "Categories"

    # PROPERTIES
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    parent_id = db.Column(db.Integer, nullable=True)
    created_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    def __repr__(self):
        return f"<Category {self.name}>"

    def __init__(self, name=None, description=None, parent_id=None):
        self.name = name
        self.description = description
        self.parent_id = parent_id

    def __str__(self):
        return f"id={self.id}, name={self.name}, description={self.description}, parent_id={self.parent_id}"


# TRIGGERS

@event.listens_for(Role, "before_insert")
def on_insert_trigger(mapper, connection, target):
    table = Role.__table__
    user: User = current_user
    target.created_by = user.id


@event.listens_for(Role, "before_update")
def on_update_trigger(mapper, connection, target):
    table = Role.__table__
    target.updated_at = datetime.datetime.now()

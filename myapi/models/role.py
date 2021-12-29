import datetime
from flask_jwt_extended.view_decorators import jwt_required, verify_jwt_in_request
from sqlalchemy import event
from flask import json
from flask_seeder.generator import String
from sqlalchemy.sql.functions import user
from myapi.extensions import db
from myapi import permissions
from flask_jwt_extended import current_user

from myapi.models.user import User


class Role(db.Model):
    __tablename__ = "Roles"

    # PROPERTIES
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permissions = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    # RELATIONSHIPS
    assigned_roles = db.relationship("UserWithRole", backref="role", lazy="joined")

    def __repr__(self) -> str:
        return f"<Role {self.name}>"

    def __init__(self,  name: str = None,
                 description: str = None,
                 permissions: str = None) -> None:
        self.name = name
        self.description = description
        self.permissions = permissions

    def __str__(self) -> String:
        return f"id={self.id}, name={self.name}, permission={self.permissions}, description={self.description}"

# TRIGGERS


@event.listens_for(Role, "before_insert")
def on_insert_trigger(mapper, connection, target):
    table = Role.__table__
    verify_jwt_in_request()
    user: User = current_user
    target.created_by = user.id
    target.permissions = json.dumps(permissions.PERMISSION)


@event.listens_for(Role, "before_update")
def on_update_trigger(mapper, connection, target):
    table = Role.__table__
    target.updated_at = datetime.datetime.now()

from sys import meta_path
from flask import json
from marshmallow.utils import EXCLUDE
from marshmallow_sqlalchemy.schema import auto_field
from myapi.models import User
from myapi.extensions import ma, db
from marshmallow import validate, fields
from myapi.models import Role


class RoleSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    permissions = auto_field(dump_only=True)

    class Meta:
        model = Role
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")

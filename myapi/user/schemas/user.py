from enum import unique
from flask import json
from marshmallow_sqlalchemy.schema import auto_field
from myapi.models import User
from myapi.extensions import ma, db

from marshmallow import validate, fields


class UserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)
    email = fields.Email()
    last_name = fields.String(validate=validate.Length(max=80))
    first_name = fields.String(validate=validate.Length(max=80))
    address = fields.String(validate=validate.Length(max=300))
    phone = fields.String(validate=validate.Length(max=11))
    created_at = auto_field(dump_only = True)
    updated_at = auto_field(dump_only = True)
    deleted_at = auto_field(dump_only = True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password",)

    

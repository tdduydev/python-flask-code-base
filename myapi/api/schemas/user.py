from flask_marshmallow import Marshmallow
from myapi.models import User
from myapi.extensions import ma, db

from marshmallow import fields ,validate

class UserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)
    email = fields.Email()
    lastName = fields.String(validate=validate.Length(max=20))
    firstName = fields.String(validate=validate.Length(max=20))
    address = fields.String(validate=validate.Length(max=80))
    phoneNumber = fields.String(validate=validate.Length(max=12))

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password",)

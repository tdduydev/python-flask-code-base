from marshmallow_sqlalchemy.schema import auto_field
from myapi.models import Tag
from myapi.extensions import ma, db

from marshmallow import validate, fields


class TagSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    name = fields.String(validate=validate.Length(max=80))
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)


    class Meta:
        model = Tag
        sqla_session = db.session
        load_instance = True
        
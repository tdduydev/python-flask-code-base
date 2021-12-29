from marshmallow_sqlalchemy.schema import auto_field
from myapi.models import Tag
from myapi.extensions import ma, db

from marshmallow import validate, fields


class TagSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    name = fields.String(validate=validate.Length(max=80))

    class Meta:
        model = Tag
        sqla_session = db.session
        load_instance = True
        exclude = ("created_by", "created_at", "updated_at", "deleted_at")

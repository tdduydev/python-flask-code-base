from marshmallow_sqlalchemy.schema import auto_field
from myapi.models import News
from myapi.extensions import ma, db

from marshmallow import validate, fields


class NewsSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    title = fields.String(validate=validate.Length(max=80))
    description = fields.String(validate=validate.Length(max=300))
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)


    class Meta:
        model = News
        sqla_session = db.session
        load_instance = True
        


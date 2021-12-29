from marshmallow_sqlalchemy.schema import auto_field
from myapi.models import News
from myapi.extensions import ma, db

from marshmallow import validate, fields


class NewsSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = News
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")

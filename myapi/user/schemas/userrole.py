from marshmallow_sqlalchemy.schema import auto_field
from myapi.models import UserWithRole
from myapi.extensions import ma, db

class UserWithRoleSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)

    class Meta:
        model = UserWithRole
        sqla_session = db.session
        load_instance = True


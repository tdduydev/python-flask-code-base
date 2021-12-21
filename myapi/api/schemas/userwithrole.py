from myapi.models import UserWithRole
from myapi.extensions import ma, db

class UserWithRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserWithRole
        sqla_session = db.session
        load_instance = True


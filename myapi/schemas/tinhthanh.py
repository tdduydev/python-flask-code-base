from myapi.extensions import ma, db
from myapi.models import Tinhthanh




class TinhthanhSchema(ma.SQLAlchemyAutoSchema):

    id = ma.UUID(dump_only=True)


    class Meta:
        model = Tinhthanh
        sqla_session = db.session
        load_instance = True
        exclude = ("created_by", "created_at", "updated_at","updated_by","deleted_by","deleted_at","deleted")
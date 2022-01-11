from myapi.extensions import ma, db
from myapi.models import Tagnews


class TagNewsSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    tag_id = ma.Int()
    news_id = ma.Int()


    class Meta:
        model = Tagnews
        sqla_session = db.session
        load_instance = True
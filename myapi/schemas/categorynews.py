from myapi.extensions import ma, db
from myapi.models import Categorynews


class CategorynewsSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    category_id = ma.Int()
    news_id = ma.Int()


    class Meta:
        model = Categorynews
        sqla_session = db.session
        load_instance = True
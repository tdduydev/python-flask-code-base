from flask_restful import Resource
from myapi.extensions import db, apispec
from myapi.models import category
from myapi.models.category import Category
from myapi.models.news import News
from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import jwt_required, current_user
from myapi.schemas import CategorynewsSchema


blueprint = Blueprint("categorynews", __name__, url_prefix="/categorynews")

@blueprint.route("", methods=["POST"])
@jwt_required()
def add_categorynews():
    """Create category news
    ---
    post:
        tags:
          - category news
        summary: Create category news
        description: Create a category news
        requestBody:
          content:
            application/json:
              schema:
                CategorynewsSchema
        responses:
          200:
            description: Category news has been created 
          400:
            description: news or category not found
    """
    schema = CategorynewsSchema()
    
    categorynews = schema.load(request.json)
    news_id = request.args.get('news_id')
    category_id = request.args.get('category_id')
    
    categorynews.news = News.query.get_or_404(news_id)

    if categorynews.news == None :
        return {"msg": "no news found"}, 404

    categorynews.category = Category.query.get_or_404(category_id)

    if categorynews.category == None:
        return {"msg": "no category found"} , 404

    db.session.add(categorynews)
    db.session.commit()

    return {"msg": "categorynews create", "categorynews": schema.dump(categorynews)} 

@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("CategorynewsSchema", schema=CategorynewsSchema)
    apispec.spec.path(view=add_categorynews, app=app)

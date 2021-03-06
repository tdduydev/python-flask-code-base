from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from myapi.extensions import apispec
from myapi.news.resources import NewsResource, NewsList, NewsPicture
from myapi.schemas import NewsSchema


blueprint = Blueprint("news", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_resource(NewsResource, "/news/<int:news_id>", endpoint="news_by_id")
api.add_resource(NewsList, "/news", endpoint="news")
api.add_resource(NewsPicture, "/picture/<int:news_id>", endpoint="picture")


@blueprint.before_app_first_request
def register_view():
    apispec.spec.components.schema("NewsSchema", schema=NewsSchema)

    apispec.spec.path(view=NewsList, app=current_app)
    apispec.spec.path(view=NewsResource, app=current_app)
    apispec.spec.path(view=NewsPicture, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400

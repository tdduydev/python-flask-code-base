from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from myapi.extensions import apispec
from myapi.tag.resources import TagResource , TagList
from myapi.tag.schemas.tag import TagSchema


blueprint = Blueprint("tag",__name__,url_prefix="/api/v2")
api = Api(blueprint)

api.add_resource(TagResource, "/tag/<int:tag_id>", endpoint="tag_by_id")
api.add_resource(TagList, "/tag", endpoint="tag")



@blueprint.before_app_first_request
def register_view():
    apispec.spec.components.schema("TagSchema", schema=TagSchema)

    apispec.spec.path(view=TagList, app=current_app)
    apispec.spec.path(view=TagResource, app=current_app)

@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
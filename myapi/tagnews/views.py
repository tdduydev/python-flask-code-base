from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from myapi.extensions import apispec
from marshmallow import ValidationError
from myapi.schemas.tagnews import TagNewsSchema
from myapi.tagnews.resources.tagnews import TagnewsList


blueprint = Blueprint("tagnews",__name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_resource(TagnewsList,"/tagnews", endpoint="tagnews")

@blueprint.before_app_first_request
def register_view():
    apispec.spec.components.schema("TagNewsSchema", schema=TagNewsSchema)
    apispec.spec.path(view=TagnewsList, app=current_app)

@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400

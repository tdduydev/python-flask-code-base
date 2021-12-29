
from flask.json import jsonify
from flask_jwt_extended.view_decorators import jwt_required
from myapi.models import Category
from myapi.schemas import CategorySchema
from myapi.utils.rolehelper import permissions_required
from myapi.extensions import db, apispec
from flask import request, jsonify, Blueprint, current_app as app

blueprint = Blueprint("category", __name__, url_prefix="/category")


@blueprint.route("", methods=["POST"])
@jwt_required()
@permissions_required("category", ["create"])
def add_category():
    # region Swagger UI
    """Get category
    ---
    post:
        tags:
          - category
        summary: Create category
        description: Create a category
        requestBody:
          content:
            application/json:
              schema:
                CategorySchema
        responses:
          200:
            description: Category has been created successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    # CHECK IF REQUEST INPUT IS IN JSON FORMAT
    if not request.is_json:
        return {"msg": "bad request"}, 403

    # CHECK IF REQUEST IS APPROPRIATE
    if not request.json.get("name", None) or str(request.json.get("name", None)).isspace():
        return {"msg": "Name is missing"}

    # CHECK IF THE Category IS ALREADY EXIST
    if Category.query.filter(Category.name == request.json.get("name", None)).first():
        return {"msg": "The category had already been created"}

    category = CategorySchema().load(request.json)
    db.session.add(category)
    db.session.commit()
    return {"msg": "Category has been created successfully"}, 200


@blueprint.route("/list", methods=["GET"])
@jwt_required()
@permissions_required("category", ["get"])
def get_category_list():
    # region Swagger UI
    """Get category
    ---
    get:
        tags:
          - category
        summary: Get category
        description: Get a list category
        responses:
          200:
            content:
              application/json:
                schema:
                  allOf:
                    - type: array
                      items:
                        $ref: '#/components/schemas/CategorySchema'
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion
    categories = Category.query.all()
    print(categories)
    return jsonify(CategorySchema().dump(categories, many=True)), 200


@blueprint.route("", methods=["PUT"])
@jwt_required()
@permissions_required("category", ["update"])
def update_category():
    # region Swagger UI
    """Update category
    ---
    get:
        tags:
          - category
        summary: Update category
        description: Update a category
        responses:
          200:
            description: Category has been updated successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("CategorySchema", schema=CategorySchema)

    apispec.spec.path(view=get_category_list, app=app)
    apispec.spec.path(view=add_category, app=app)

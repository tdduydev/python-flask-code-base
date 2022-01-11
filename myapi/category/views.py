
from flask_jwt_extended.view_decorators import jwt_required
from myapi.commons.pagination import paginate
from myapi.helper.http_code import HttpCode
from myapi.models import Category
from myapi.schemas import CategorySchema
from myapi.utils.role_helper import permissions_required
from myapi.helper.multi_language import return_message
from myapi.extensions import db, apispec, lang
from flask import request, Blueprint, current_app as app
from myapi.helper.multi_language import DictionaryReturnType
blueprint = Blueprint("category", __name__, url_prefix="/category")


@blueprint.route("", methods=["POST"])
@jwt_required()
# @permissions_required("category", ["create"])
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
    if 'language' in request.headers:
        language = request.headers.get()
    if not request.is_json:
        return {"msg": "bad request"}, HttpCode.BadRequest

    # CHECK IF REQUEST IS APPROPRIATE
    if not request.json.get("name", None) or str(request.json.get("name", None)).isspace():
        return {"msg": "Name is missing"}, HttpCode.BadRequest

    # CHECK IF THE Category IS ALREADY EXIST
    if Category.query.filter(Category.name == request.json.get("name", None)).first():
        return {"msg": "The category had already been created"}

    category = CategorySchema().load(request.json)
    db.session.add(category)
    db.session.commit()
    return {"msg": "Category has been created successfully"}, 200


@blueprint.route("/list", methods=["GET"])
@jwt_required()
# @permissions_required("category", ["get"])
def get_category_list():
    # region Swagger UI
    """Get list of categories
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
    schema = CategorySchema(many=True)
    query = Category.query
    return paginate(query, schema), HttpCode.OK


@blueprint.route("/<id>", methods=["PUT"])
@jwt_required()
@permissions_required("category", ["update"])
def update_category(id):
    # region Swagger UI
    """Update category
    ---
    put:
        tags:
          - category
        summary: Update category
        description: Update a category
        parameters:
          - in: path
            name: id
            schema:
              type: integer
        requestBody:
                content:
                  application/json:
                    schema:
                      CategorySchema
        responses:
          200:
            description: Category has been updated successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    # CHECK IF USER INPUT IS FORMATTED AS JSON
    if not request.is_json:
        return {"msg": "bad request"}, HttpCode.BadRequest

    # CHECK IF name IS EMPTY OR WHITE SPACE
    if not request.json.get("name", None) or str(request.json.get("name", None)).isspace():
        return {"msg": "Name is missing"}, HttpCode.BadRequest

    # CHECK IF parent_id EXIST
    if 'parent_id' in request.json:
        if not Category.query.get(request.json.get('parent_id')):
            return {"msg": "Provided parent_id doesn't exist"}, HttpCode.BadRequest

    schema = CategorySchema(partial=True)
    category: Category = Category.query.get_or_404(id)

    # CHECK IF name EXIST
    print(request.json.get("name", None))
    if Category.query.filter(Category.name == request.json.get("name", None)).first():
        return {"msg": "Name is already exist"}, HttpCode.BadRequest

    category = schema.load(request.json, instance=category)
    db.session.commit()
    if 'language' in request.headers:
        lang.set_current_language(request.headers.get('language'))

    return {"msg": lang.get_current_text(DictionaryReturnType.success)}, HttpCode.OK


@ blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("CategorySchema", schema=CategorySchema)

    apispec.spec.path(view=get_category_list, app=app)
    apispec.spec.path(view=add_category, app=app)
    apispec.spec.path(view=update_category, app=app)

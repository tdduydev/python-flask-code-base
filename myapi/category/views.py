
from flask.json import jsonify
from flask_jwt_extended.view_decorators import jwt_required
from myapi.commons.pagination import paginate
from myapi.helper.http_code import HttpCode
from myapi.models import Category, category
from myapi.schemas import CategorySchema
from myapi.utils.role_helper import permissions_required
from myapi.helper.multi_language import return_message
from myapi.extensions import db, apispec, lang
from flask import request, Blueprint, current_app as app
from myapi.helper.multi_language import ReturnMessageEnum
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
        return {"msg": lang.get_current_text(ReturnMessageEnum.not_json)}, HttpCode.BadRequest

    # CHECK IF REQUEST IS APPROPRIATE
    if not request.json.get("name", None) or str(request.json.get("name", None)).isspace():
        return {"msg": f"{lang.get_current_text(ReturnMessageEnum.missing)}: name"}, HttpCode.BadRequest

    # CHECK IF THE Category IS ALREADY EXIST
    if Category.query.filter(Category.name == request.json.get("name", None)).first():
        return {"msg": lang.get_current_text(ReturnMessageEnum.not_json)}

    # CHECK IF USER INPUT parent_id
    if "parent_id" in request.json:
        # CHECK IF parent_id IS AN INTEGER
        try:
            parent_id = int(request.json.get("parent_id"))
        except:
            return {"msg": f"{lang.get_current_text(ReturnMessageEnum.fail)}: id"}, HttpCode.BadRequest

        # CHECK IF PARENT Category exist
        if not Category.query.filter(Category.id == parent_id):
            return {"msg": lang.get_current_text(ReturnMessageEnum.not_exist)}

    category = CategorySchema().load(request.json)
    db.session.add(category)
    db.session.commit()
    return {"msg": lang.get_current_text(ReturnMessageEnum.success)}, HttpCode.OK


@blueprint.route("/list", methods=["GET"])
@jwt_required()
@permissions_required("category", ["get"])
def get_category_list():
    # region Swagger UI
    """Get list of categories
    ---
    get:
        tags:
          - category
        summary: Get list of categories 
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


@blueprint.route("/<id>", methods=["GET"])
@jwt_required()
@permissions_required("category", ["get"])
def get_category(id):
    # region Swagger UI
    """Get a category
    ---
    get:
        tags:
          - category
        summary: Get a category
        description: Get a list category
        parameters:
          - in: path
            name: id
            schema:
              type: integer
        responses:
          200:
            content:
              application/json:
                schema:
                  CategorySchema
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion
    # CHECK IF id IS AN INTEGER
    try:
        id = int(id)
    except:
        return {"msg": f"{lang.get_current_text(ReturnMessageEnum.fail)}: id"}, HttpCode.BadRequest
    schema = CategorySchema()
    category = Category.query.filter(Category.id == id).first_or_404()
    return schema.dump(category), HttpCode.OK


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
        return {"msg": lang.get_current_text(ReturnMessageEnum.not_json)}, HttpCode.BadRequest
    # CHECK IF id IS AN INTEGER
    try:
        id = int(id)
    except:
        return {"msg": f"{lang.get_current_text(ReturnMessageEnum.fail)}: id"}, HttpCode.BadRequest
    # CHECK IF name IS EMPTY OR WHITE SPACE
    if not request.json.get("name", None) or str(request.json.get("name", None)).isspace():
        return {"msg": f"{lang.get_current_text(ReturnMessageEnum.missing)}: name"}, HttpCode.BadRequest

    # CHECK IF parent_id EXIST
    if 'parent_id' in request.json:
        # CHECK IF parent_id IS IN CORRECT FORMAT
        try:
            parent_id = int(request.json.get("parent_id"))
        except:
            return {"msg": f"{lang.get_current_text(ReturnMessageEnum.fail)}: parent_id"}, HttpCode.BadRequest
        # CHECK IF PARENT Category EXIST
        if not Category.query.filter(Category.id == parent_id).first():
            return {"msg": f"{lang.get_current_text(ReturnMessageEnum.not_exist)}: parent_id"}, HttpCode.BadRequest

    # CHECK IF name EXIST
    if Category.query.filter(Category.name == request.json.get("name", None), Category.id != id).first():
        return {"msg": lang.get_current_text(ReturnMessageEnum.exist)}, HttpCode.BadRequest

    schema = CategorySchema(partial=True)
    category: Category = Category.query.get_or_404(id)
    category = schema.load(request.json, instance=category)
    db.session.commit()
    return {"msg": lang.get_current_text(ReturnMessageEnum.success)}, HttpCode.OK


@blueprint.route("/<id>", methods=["DELETE"])
@jwt_required()
@permissions_required("category", ["delete"])
def delete_category(id):
    # region Swagger UI
    """Delete category
    ---
    delete:
        tags:
          - category
        summary: Delete category
        description: Delete a category via id
        parameters:
          - in: path
            name: id
            schema:
              type : integer
        responses:
          200:
            description: Category has been deleted successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    # CHECK IF THE Category id IS AN INTEGER
    try:
        id = int(id)
    except:
        return {"msg": f"{lang.get_current_text(ReturnMessageEnum.fail)}: id"}, HttpCode.BadRequest

    # CHECK IF REQUEST INPUT IS IN JSON FORMAT
    category = Category.query.filter(Category.id == id).first_or_404()
    print(category)
    db.session.delete(category)
    db.session.commit()
    return {"msg": lang.get_current_text(ReturnMessageEnum.success)}, HttpCode.OK


@ blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("CategorySchema", schema=CategorySchema)

    apispec.spec.path(view=get_category_list, app=app)
    apispec.spec.path(view=add_category, app=app)
    apispec.spec.path(view=update_category, app=app)
    apispec.spec.path(view=delete_category, app=app)

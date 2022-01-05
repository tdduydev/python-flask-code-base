from re import I
from flask import json
from flask.json import jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    current_user as user_jwt
)
from flask import request, jsonify, Blueprint, current_app as app
from marshmallow.utils import INCLUDE
from sqlalchemy.sql.expression import update
from myapi import permissions
from myapi.commons.pagination import paginate
from myapi.extensions import db, apispec, lang
from myapi.helper.http_code import HttpCode
from myapi.helper.multi_language import ReturnMessageEnum
from myapi.models import User, UserWithRole, Role, role
from myapi.schemas.role import RoleSchema
from marshmallow import EXCLUDE
import datetime
from myapi.schemas.userrole import UserWithRoleSchema
from myapi.utils.role_helper import update_permissions, permissions_required
##########################################################################


blueprint = Blueprint("role", __name__, url_prefix="/role")


@blueprint.route("/assign/<userid>/<roleid>", methods=["POST"])
@jwt_required()
@permissions_required("role", ["assign_role"])
def assign_role(userid, roleid):

    # region Swagger UI
    """Assign user with role
    ---
    post:
        tags:
          - role
        summary: Assign role
        description: Assign a user with a role
        parameters:
          - in: path
            name: userid
            schema:
              type: integer
          - in: path
            name: roleid
            schema:
              type: integer
        responses:
          201:
            description: user has been assigned successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    # CHECK IF username OR role_id EXIST
    if not userid or not roleid:
        return jsonify(
            {"msg": f"{lang.get_current_text(ReturnMessageEnum.missing)}: userid or roleid"}), HttpCode.BadRequest
    # CHECK IF userid and roleid IS IN CORRECT FORMAT
    try:
        userid = int(userid)
        roleid = int(roleid)
    except:
        return jsonify(
            {"msg": f"{lang.get_current_text(ReturnMessageEnum.fail)}: userid or roleid"}), HttpCode.BadRequest

    # CHECK IF USER EXISTS
    if not User.query.filter_by(id=userid).first():
        return jsonify({"msg": f"{lang.get_current_text(ReturnMessageEnum.not_exist)}: User"}), HttpCode.BadRequest

    # CHECK IF OBJECT EXISTS
    if not Role.query.filter_by(id=roleid).first():
        return jsonify({"msg": f"{lang.get_current_text(ReturnMessageEnum.not_exist)}: Role"}), HttpCode.BadRequest

    user_with_role = UserWithRole(userid, roleid)

    # CHECK IF OBJECT IS INSTANTIATED THEN ADD TO THE DATABASE
    db.session.add(user_with_role)
    db.session.commit()
    return jsonify({"msg": f"{lang.get_current_text(ReturnMessageEnum.success)}"}), HttpCode.Created


@blueprint.route("/unassign/<userid>/<roleid>", methods=["DELETE"])
@jwt_required()
@permissions_required("role", ["unassign_role"])
def unassign_role(userid, roleid):
    # region Swagger UI
    """Unassign user with role
    ---
    delete:
        tags:
          - role
        summary: Unassign role
        description: Unassign a user with a role
        parameters:
          - in: path
            name: userid
            schema:
              type: integer
          - in: path
            name: roleid
            schema:
              type: integer
        responses:
          200:
            description: user has been unassigned successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion
    # CHECK IF userid OR role_id EXIST
    # IF NOT, SEND RESPONSE STATUS 400
    if not userid or not roleid:
        return jsonify(
            {"msg": f"{lang.get_current_text(ReturnMessageEnum.missing)}: userid or roleid"}), HttpCode.BadRequest

    # CHECK IF userid and roleid IS IN CORRECT FORMAT
    try:
        userid = int(userid)
        roleid = int(roleid)
    except:
        return jsonify(
            {"msg": f"{lang.get_current_text(ReturnMessageEnum.fail)}: userid or roleid"}), HttpCode.BadRequest

    # INSTANTIATE AN UserWithRole OBJECT
    # IF OBJECT IS NULL RETURN RESPONSE STATUS 404
    user_with_role = UserWithRole.query\
        .filter(UserWithRole.user_idn == userid)\
        .filter(UserWithRole.role_id == roleid)\
        .first_or_404()

    db.session.delete(user_with_role)
    db.session.commit()
    return jsonify({"msg": f"{lang.get_current_text(ReturnMessageEnum.success)}"}), HttpCode.OK


@blueprint.route("", methods=["POST"])
@jwt_required()
@permissions_required("role", ["create"])
def add_role():
    # region Swagger UI
    """Add role
    ---
    post:
        tags:
          - role
        summary: Add role
        description: Add a new role
        requestBody:
          content:
            application/json:
              schema:
                RoleSchema
        responses:
          201:
            description: Role has been created successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    # CHECK IF REQUEST IS SENT AS JSON
    # IF NOT, SEND RESPONSE STATUS 400
    if not request.is_json:
        return jsonify({"msg": f"{lang.get_current_text(ReturnMessageEnum.not_jsont)}"}), HttpCode.BadRequest

    # CHECK IF REQUEST IS APPROPRIATE
    if not request.json.get("name", None) or str(request.json.get("name", None)).isspace():
        return {"msg": f"{lang.get_current_text(ReturnMessageEnum.missing)}: name"}

    # CHECK IF THE Role IS ALREADY EXIST
    if Role.query.filter(Role.name == request.json.get("name", None)).first():
        return {"msg": f"{lang.get_current_text(ReturnMessageEnum.exist)}"}

    # SETUP SCHEMA AND TURN JSON INTO THE CORRECT OBJECT
    schema = RoleSchema()
    role = schema.load(request.json)

    # ADD DATA TO THE DATABASE AND COMMIT
    db.session.add(role)
    db.session.commit()
    return jsonify({"msg": f"{lang.get_current_text(ReturnMessageEnum.success)}"}), HttpCode.Created


@blueprint.route("/<id>", methods=["PUT"])
@jwt_required()
@permissions_required("role", ["update"])
def update_role(id):
    # region Swagger UI
    """Update role
    ---
    put:
        tags:
          - role
        summary: Update role
        description: Update a role with new data
        parameters:
          - in: path
            name: id
            schema:
              type: integer
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  permissions:
                    type: string
                    example: {"auth": {"change_password": false, "login": false, "refresh": false, "revoke_access": false, "revoke_refresh": false}, "role": {"assign_role": false, "create": false,"get": true, "delete": false,"unassign_role": false, "update": false}, "user": {"create": false, "delete": false, "edit": false, "update": false}}
                    required: true
                  description:
                    type: string
                    example: description
                    required: true
                  name:
                    type: string
                    example: name
                    required: true
        responses:
          200:
            description: Role has been updated successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    # CHECK IF REQUEST IS SENT AS JSON
    # IF NOT, SEND RESPONSE STATUS 400
    if not request.is_json:
        return jsonify({"msg": f"{lang.get_current_text(ReturnMessageEnum.not_json)}"}), HttpCode.BadRequest

    # CHECK IF REQUEST IS APPROPRIATE
    if not request.json.get("name", None) or str(request.json.get("name", None)).isspace():
        return {"msg": f"{lang.get_current_text(ReturnMessageEnum.not_json)}"}, HttpCode.BadRequest

    # SETUP SCHEMA AND TURN JSON INTO THE CORRECT OBJECT
    role: Role = Role.query.get_or_404(id)
    role.permissions = json.dumps(request.json.get("permissions", None))
    role.name = request.json.get("name", None)
    role.description = request.json.get("description", None)
    db.session.commit()
    return jsonify({"msg": f"{lang.get_current_text(ReturnMessageEnum.success)}"}), HttpCode.OK


@blueprint.route("/<id>", methods=["GET"])
@jwt_required()
@permissions_required("role", ["get"])
def get_role(id):
    # region Swagger UI
    """Get role
    ---
    get:
        tags:
          - role
        summary: Get a role
        description: Get a role via id
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
                  RoleSchema
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    # CHECK IF id IS NOT EMPTY ELSE RETURN RESPONSE STATUS 400
    try:
        id = int(id)
    except:
        return jsonify({"msg": f"{lang.get_current_text(ReturnMessageEnum.missing)}"}), HttpCode.BadRequest

    role: Role = Role.query.get_or_404(id)
    role.permissions = update_permissions(role.permissions)
    return jsonify({"msg": lang.get_current_text(ReturnMessageEnum.success), "content": RoleSchema().dump(role)}), HttpCode.OK


@blueprint.route("/list", methods=["GET"])
@jwt_required()
@permissions_required("role", ["get"])
def get_role_list():
    # region Swagger UI
    """Get list of roles
    ---
    get:
        tags:
          - role
        summary: Get list of roles
        description: Get a list of roles
        responses:
          200:
            description: success
            content:
              application/json:
                schema:
                  allOf:
                    - type: array
                      items:
                        $ref: '#/components/schemas/RoleSchema'
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion   print(roles)

    schema = RoleSchema(many=True)
    # GET LIST OF Role
    roles = Role.query
    # UPDATE ALL PERMISSION FOR EACH ROLE
    for role in roles:
        role: Role = role
        role.permissions = str(update_permissions(role.permissions))
    return paginate(roles, schema), HttpCode.OK


@blueprint.route("/list/<userid>", methods=["GET"])
@jwt_required()
@permissions_required("role", ["get"])
def get_user_role(userid):
    # region Swagger UI
    """Get user roles
    ---
    get:
        tags:
          - role
        summary: Get user's roles
        description: Get roles of user
        parameters:
          - in: path
            name: userid
            schema:
              type: integer
        responses:
          200:
            description: bad request
            content:
              application/json:
                schema:
                  allOf:
                    - type: array
                      items:
                        RoleSchema
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    try:
        userid = int(userid)
    except:
        return jsonify({"msg": f"{lang.get_current_text(ReturnMessageEnum.missing)}"}), HttpCode.BadRequest
    # GET THE ROLES USING THE userid
    schema = RoleSchema(many=True)
    roles = Role.query.join(UserWithRole).join(User).filter(User.id == userid)
    return paginate(roles, schema), HttpCode.OK


@ blueprint.route("/<id>", methods=["DELETE"])
@ jwt_required()
@ permissions_required("role", ["delete"])
def delete_role(id):
    # region Swagger UI
    """Delete role
    ---
    delete:
        tags:
          - role
        summary: Delete a role
        description: Delete a role via id
        parameters:
          - in: path
            name: id
            schema:
              type: integer
        responses:
          200:
            description: Role has been deleted successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    # GET THE ROLE USING PROVIDED id
    role = Role.query.get_or_404(id)
    # CHECK IF role HAD ALREADY BEEN DELETED
    if role.deleted_at:
        return jsonify({"msg": "Role had already been deleted"}), HttpCode.BadRequest
    # IF role HADN'T BEEN DELETED THEN SET TIMESTAMP
    role.deleted_at = datetime.datetime.now()
    db.session.commit()
    return jsonify({"msg": "Role has been deleted successfully"}), HttpCode.OK


@ blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("RoleSchema", schema=RoleSchema)
    apispec.spec.components.schema("UserWithRoleSchema", schema=UserWithRoleSchema)
    apispec.spec.path(view=assign_role, app=app)
    apispec.spec.path(view=add_role, app=app)
    apispec.spec.path(view=update_role, app=app)
    apispec.spec.path(view=get_role, app=app)
    apispec.spec.path(view=delete_role, app=app)
    apispec.spec.path(view=unassign_role, app=app)
    apispec.spec.path(view=get_role_list, app=app)
    apispec.spec.path(view=get_user_role, app=app)

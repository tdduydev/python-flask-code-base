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
from myapi.extensions import db, apispec
from myapi.models import User, UserWithRole, Role, role
from myapi.user.schemas.role import RoleSchema
from marshmallow import EXCLUDE
import datetime
from myapi.user.schemas.userrole import UserWithRoleSchema
from myapi.utils import permissions_required

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
    # IF NOT, SEND RESPONSE STATUS 400
    if not userid or not roleid:
        return jsonify({"msg": "Missing userid or roleid"}), 400

    # CHECK IF USER EXISTS
    # IF NOT, SEND RESPONSE STATUS 400
    if not User.query.filter_by(id=userid).first():
        return jsonify({"msg": "User doesn't exist"}), 400

    # CHECK IF OBJECT EXISTS
    # IF NOT, SEND RESPONSE STATUS 400
    if not Role.query.filter_by(id=roleid).first():
        return jsonify({"msg": "Role doesn't exist"}), 400

    user_with_role = UserWithRole(userid, roleid)

    # CHECK IF OBJECT IS INSTANTIATED THEN ADD TO THE DATABASE
    if user_with_role:
        db.session.add(user_with_role)
        db.session.commit()
        return jsonify({"msg": "User has been assigned successfully"}), 201


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
        return jsonify({"msg": "Missing username or roleid"}), 400

    # CHECK IF USER EXISTS
    # IF NOT, SEND RESPONSE STATUS 400
    if not User.query.filter_by(id=userid).first():
        return jsonify({"msg": "User doesn't exist"}), 400

    # CHECK IF OBJECT EXISTS
    # IF NOT, SEND RESPONSE STATUS 400
    if not Role.query.filter_by(id=userid).first():
        return jsonify({"msg": "Role doesn't exist"}), 400

    # INSTANTIATE AN UserWithRole OBJECT
    # IF OBJECT IS NULL RETURN RESPONSE STATUS 404
    user_with_role = UserWithRole.query.filter_by(user_id=userid).filter_by(role_id=roleid).first_or_404()

    db.session.delete(user_with_role)
    db.session.commit()
    return jsonify({"msg": "User has been unassigned successfully"}), 200


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
        return jsonify({"msg": "Missing JSON in request"}), 400

    # SETUP SCHEMA AND TURN JSON INTO THE CORRECT OBJECT
    schema = RoleSchema()
    print(request.json)
    role = schema.load(request.json)

    # CHECK IF DATA IS INSTANTIATED
    if not role:
        return jsonify({"msg": "Role cannot be created"}), 400

    # ADD DATA TO THE DATABASE AND COMMIT
    db.session.add(role)
    db.session.commit()
    return jsonify({"msg": "Role has been created successfully"}), 201


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
                RoleSchema
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
        return jsonify({"msg": "Missing JSON in request"}), 400

    # SETUP SCHEMA AND TURN JSON INTO THE CORRECT OBJECT
    schema = RoleSchema()
    role = Role.query.get_or_404(id)
    role = schema.load(request.json, instance=role)

    db.session.commit()

    return jsonify({"msg": "Role has been updated successfully"}), 200


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
        summary: Get role
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
    if not id:
        return jsonify({"msg": "Missing id"}), 400

    role = Role.query.get_or_404(id)
    return jsonify(RoleSchema().dump(role)), 200


@blueprint.route("/list", methods=["GET"])
@jwt_required()
@permissions_required("role", ["get"])
def get_role_list():
    # region Swagger UI
    """Get role
    ---
    get:
        tags:
          - role
        summary: Get role
        description: Get a role via id
        responses:
          200:
            description: bad request
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
    # endregion

    roles = Role.query
    return jsonify(RoleSchema().dump(roles, many=True)), 200


@blueprint.route("/list/<userid>", methods=["GET"])
@jwt_required()
@permissions_required("role", ["get"])
def get_user_role(userid):
    # region Swagger UI
    """Get user role
    ---
    get:
        tags:
          - role
        summary: Get user role
        description: Get a role via id
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

    # GET THE ROLES USING THE userid
    roles = Role.query.join(UserWithRole).join(User).filter(User.id == userid).all()
    print(roles)
    return jsonify(RoleSchema().dump(roles, many=True)), 200


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
        summary: Delete role
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
        return jsonify({"msg": "Role had already been deleted"}), 400
    # IF role HADN'T BEEN DELETED THEN SET TIMESTAMP
    role.deleted_at = datetime.datetime.now()
    db.session.commit()
    return jsonify({"msg": "Role has been deleted successfully"}), 200


@ blueprint.route("/update_permission/<id>", methods=["POST"])
@ jwt_required()
@ permissions_required("role", ["update"])
def update_permission(id):
    # region Swagger UI
    """Update permission
    ---
    post:
        tags:
          - role
        summary: Update role permission
        description: Update role permission via id
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
        responses:
          200:
            description: Role's permission has been updated successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    # GET THE ROLE USING PROVIDED id
    role: Role = Role.query.get_or_404(id)
    # CHECK IF role HAD ALREADY BEEN DELETED
    # IF role HADN'T BEEN DELETED THEN SET TIMESTAMP
    role.permissions = json.dumps(request.json.get("permissions", None))
    role.deleted_at = datetime.datetime.now()
    db.session.commit()
    return jsonify({"msg": "Role's permissions has been updated successfully"}), 200


@ blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=assign_role, app=app)
    apispec.spec.path(view=add_role, app=app)
    apispec.spec.path(view=update_role, app=app)
    apispec.spec.path(view=get_role, app=app)
    apispec.spec.path(view=delete_role, app=app)
    apispec.spec.path(view=unassign_role, app=app)
    apispec.spec.path(view=get_role_list, app=app)
    apispec.spec.path(view=get_user_role, app=app)
    apispec.spec.path(view=update_permission, app=app)

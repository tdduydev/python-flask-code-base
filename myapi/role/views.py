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
from sqlalchemy.sql.expression import update
from myapi.extensions import db, apispec
from myapi.models import User, UserWithRole, Role
from myapi.user.schemas.role import RoleSchema


blueprint = Blueprint("role", __name__, url_prefix="/role")


@blueprint.route("/assign_role",methods=["POST"])
@jwt_required()
def assign_role():
    """Assign user with role
    ---
    post:
        tags:
          - role
        summary: Assign role
        description: Assign a user with a role
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  username: 
                    type: string
                    example: testing1
                    required: true
                  roleid:
                    type: int
                    example: 1
                    required: true
          responses:
            201:
              description: user has been assigned successfully
            400:
              description: bad request
            401:
              description: unauthorized
    """

    #CHECK IF REQUEST IS SENT AS JSON
    #IF NOT, SEND RESPONSE STATUS 400
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    #GET username & roleid FROM REQUEST
    username = request.json.get("username", None)
    role_id = request.json.get("roleid", None)

    #CHECK IF username OR role_id EXIST
    #IF NOT, SEND RESPONSE STATUS 400
    if not username or not role_id:
      return jsonify({"msg":"Missing username or roleid"}),400
    
    #GET User OBJECT FROM DATABASE
    #THEN CHECK IF OBJECT EXISTS
    #IF NOT, SEND RESPONSE STATUS 400
    intended_user = User.query.filter_by(username = username).first()
    if not intended_user:
      return jsonify({"msg":"User doesn't exist"}),400


    #GET Role OBJECT FROM DATABASE
    #THEN CHECK IF OBJECT EXISTS
    #IF NOT, SEND RESPONSE STATUS 400
    intended_role = Role.query.filter_by(id = role_id).first()
    if not intended_role:
      return jsonify({"msg":"Role doesn't exist"}),400
    
    #INSTANTIATE AN UserWithRole OBJECT 
    user_with_role = UserWithRole(user=intended_user,role=intended_role)

    #CHECK IF OBJECT IS INSTANTIATED THEN ADD TO THE DATABASE
    if user_with_role:
      db.session.add(user_with_role)
      db.session.commit()
      return jsonify({"msg":"User has been assigned successfully"}), 201

@blueprint.route("/add_role",methods=["POST"])
@jwt_required()
def add_role():
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
    #CHECK IF REQUEST IS SENT AS JSON
    #IF NOT, SEND RESPONSE STATUS 400
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    #SETUP SCHEMA AND TURN JSON INTO THE CORRECT OBJECT
    schema = RoleSchema()
    role = schema.load(request.json)

    #CHECK IF DATA IS INSTANTIATED
    if not role:
        return jsonify({"msg":"Role cannot be created"}), 400
    
    #ADD DATA TO THE DATABASE AND COMMIT
    db.session.add(role)
    db.session.commit()
    return jsonify({"msg":"Role has been created successfully"}), 201

@blueprint.route("/update_role/<role_id>",methods=["POST"])
@jwt_required()
def update_role(role_id):
    """Update role
    ---
    post:
        tags:
          - role
        summary: Update role
        description: Update a role with new data
        parameters:
          - in: path
            name: role_id
            schema:
              type: integer
        requestBody:
          content:
            application/json:
              schema:
                RoleSchema
        responses:
          201:
            description: Role has been updated successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    #CHECK IF REQUEST IS SENT AS JSON
    #IF NOT, SEND RESPONSE STATUS 400
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    #SETUP SCHEMA AND TURN JSON INTO THE CORRECT OBJECT
    schema = RoleSchema()
    role = Role.query.get_or_404(role_id)
    role = schema.load(request.json, instance = role)

    db.session.commit()

    return jsonify({"msg":"Role has been updated successfully"}), 201
    

@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=assign_role, app=app)
    apispec.spec.path(view=add_role, app=app)
    apispec.spec.path(view=update_role, app=app)


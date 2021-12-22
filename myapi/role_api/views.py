
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
from myapi.extensions import db, apispec
from myapi.models import User, UserWithRole, Role


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
    

    user_with_role = UserWithRole(user=intended_user,role=intended_role)
    if not user_with_role:
      db.session.add(user_with_role)
      db.session.commit()
      return jsonify({"msg":"User has been assigned successfully"}), 201

# @blueprint.route("/assign_role",methods=["POST"])
# @jwt_required()
# def add_role():
#     """Add new role
#     ---
#     post:
#       tags:
#         - Add new role
#       summary: Add role
#       description: Add a new role to assign to user
#       requestBody:
#         content:
#           application/json:
#             schema:
#               UserSchema
#         responses:
#         201:
#           description: user has been assigned successfully
#         400:
#           description: bad request
#         401:
#           description: unauthorized
#     """

@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=assign_role, app=app)
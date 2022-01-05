from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    current_user as user_jwt
)
from sqlalchemy.sql.functions import current_user
from myapi.helper.http_code import HttpCode
from myapi.helper.multi_language import ReturnMessageEnum
from myapi.schemas.user import UserSchema

from myapi.models import User
from myapi.extensions import pwd_context, jwt, apispec, db, lang
from myapi.auth.helpers import revoke_token, is_token_revoked, add_token_to_database
import json

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/login", methods=["POST"])
def login():
    """Authenticate user and return tokens

    ---
    post:
      tags:
        - auth
      summary: Authenticate a user
      description: Authenticates a user's credentials and returns tokens
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: admin
                  required: true
                password:
                  type: string
                  example: admin
                  required: true
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myaccesstoken
                  refresh_token:
                    type: string
                    example: myrefreshtoken
        400:
          description: bad request
      security: []
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), HttpCode.BadRequest

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), HttpCode.BadRequest

    user = User.query.filter_by(username=username).first()
    if user is None or not pwd_context.verify(password, user.password):
        return jsonify({"msg": "Bad credentials"}), HttpCode.BadRequest

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])
    print("User: ")
    print(user)
    ret = {"msg": lang.get_current_text(ReturnMessageEnum.success),
           "access_token": access_token,
           "refresh_token": refresh_token,
           "userInfo": UserSchema().dump(user)}
    return ret, HttpCode.OK


@blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Get an access token from a refresh token

    ---
    post:
      tags:
        - auth
      summary: Get an access token
      description: Get an access token by using a refresh token in the `Authorization` header
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myaccesstoken
        400:
          description: bad request
        401:
          description: unauthorized
    """
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {"access_token": access_token}
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    return jsonify(ret), HttpCode.OK


@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    """Revoke an access token

    ---
    delete:
      tags:
        - auth
      summary: Revoke an access token
      description: Revoke an access token
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), HttpCode.OK


@blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    """Revoke a refresh token, used mainly for logout

    ---
    delete:
      tags:
        - auth
      summary: Revoke a refresh token
      description: Revoke a refresh token, used mainly for logout
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), HttpCode.OK


@blueprint.route("/change_password", methods=["PUT"])
@jwt_required()
def change_password():
    """Change Password 

    ---
     put:
        tags:
          - auth
        summary: Change Password
        description: Change password for user
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  old_password:
                    type: string
                    example: P4$$w0rd!
                    required: true
                  new_password:
                    type: string
                    example: PaSsW0rD@
                    required: true
                  retype_password:
                    type: string
                    example: PaSsW0rD@
                    required: true
        responses:
          200:
            description: change password successfully
          400:
            description: bad request
    """
    method_decorators = [jwt_required()]
    password = user_jwt.password
    old_password = request.json.get("old_password", None)
    new_password = request.json.get("new_password", None)
    retype_password = request.json.get("retype_password", None)

    if pwd_context.verify(old_password, password) is False:
        return jsonify({"msg": "Enter a valid password and try again."}), HttpCode.BadRequest

    if new_password != retype_password:
        return jsonify({"msg": "Password do not match"}), HttpCode.BadRequest

    user = User.query.filter_by(username=user_jwt.username).first()
    user.password = new_password
    db.session.commit()

    return jsonify({"msg": "Change Password Successfully"}), HttpCode.OK


@jwt.user_lookup_loader
def user_loader_callback(jwt_headers, jwt_payload):
    identity = jwt_payload["sub"]
    return User.query.get(identity)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    return is_token_revoked(jwt_payload)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=login, app=app)
    apispec.spec.path(view=refresh, app=app)
    apispec.spec.path(view=revoke_access_token, app=app)
    apispec.spec.path(view=revoke_refresh_token, app=app)
    apispec.spec.path(view=change_password, app=app)

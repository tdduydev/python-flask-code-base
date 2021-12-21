from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user , get_current_user
from marshmallow.fields import Email
from myapi.api.schemas import UserSchema, user
from myapi.models import User
from myapi.extensions import db , pwd_context
from myapi.commons.pagination import paginate


class UserResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      summary: Get a user
      description: Get a single user by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        404:
          description: user does not exists
    put:
      tags:
        - api
      summary: Update a user
      description: Update a single user by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user updated
                  user: UserSchema
        404:
          description: user does not exists
    delete:
      tags:
        - api
      summary: Delete a user
      description: Delete a single user by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user deleted
        404:
          description: user does not exists
    """

    method_decorators = [jwt_required()]

    def get(self, user_id):
        schema = UserSchema()
        user = User.query.get_or_404(user_id)
        return {"user": schema.dump(user)}

    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=user)

        db.session.commit()

        return {"msg": "user updated", "user": schema.dump(user)}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"msg": "user deleted"}


class UserList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      summary: Get a list of users
      description: Get a list of paginated users
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/UserSchema'
    post:
      tags:
        - api
      summary: Create a user
      description: Create a new user
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user created
                  user: UserSchema
    """

    method_decorators = [jwt_required()]

    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)

    def post(self):
        schema = UserSchema()
        user = schema.load(request.json)

        db.session.add(user)
        db.session.commit()

        return {"msg": "user created", "user": schema.dump(user)}, 201


class UserInform(Resource):

    """Single object resource

   ---
   get:
     tags:
       - api
     summary: Automatic User loading
     description: Get a user by jwt login
     responses:
       200:
         content:
           application/json:
             schema:
               type: object
               properties:
                 user: UserSchema
       404:
         description: user does not exists
   """
    @jwt_required()
    def get(self):

        method_decorators = [jwt_required()]
      
        return jsonify(
            id=current_user.id,
            email=current_user.email,
            last_name=current_user.last_name,
            first_name=current_user.first_name,
            address=current_user.address,
            phone=current_user.phone,
        )

class UserSearch(Resource):

  """Single object resource

    ---
    get:
      tags:
        - api
      summary: Search User by First Name
      description: Search user get list 
      parameters:
        - in: query
          name: search_key
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        404:
          description: user does not exists
    """

  method_decorators = [jwt_required()]

    # def get(self, search_key):
    #     schema = UserSchema(many=True)
    #     query = User.query.filter(User.__ts_vector__.match(expressions, postgresql_regconfig='english')).all()
    #     return paginate(query, schema)

  def get(self):
        search_key = request.args.get('search_key')
        print(search_key)
        schema = UserSchema(many=True)
        query = User.query.filter(User.first_name.match(search_key) | User.phone.match(search_key) )
        return paginate(query, schema)

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from myapi.models.tag import Tag
from myapi.schemas.tag import TagSchema
from myapi.extensions import db


class TagList(Resource):

    method_decorators = [jwt_required()]

    @jwt_required()
    def post(self):
        schema = TagSchema()
        tag = schema.load(request.json)

        tag.user_id = current_user.id

        db.session.add(tag)
        db.session.commit()

        return {"msg": "tag upload", "tag": schema.dump(tag)}, 201


class TagResource(Resource):

    method_decorators = [jwt_required()]

    def get(self, tag_id):
        schema = TagSchema()
        tag = Tag.query.get_or_404(tag_id)
        return {"tag": schema.dump(tag)}

    def put(self, tag_id):
        schema = TagSchema(partial=True)
        tag = Tag.query.get_or_404(tag_id)
        tag.updated_at = db.func.current_timestamp()
        tag = schema.load(request.json, instance=tag)

        db.session.commit()

        return {"msg": "tag updated", "tag": schema.dump(tag)}

    def delete(self, tag_id):
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()

        return {"msg": "tag deleted"}

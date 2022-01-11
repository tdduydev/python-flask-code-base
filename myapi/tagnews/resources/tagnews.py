from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from myapi.schemas.tagnews import TagNewsSchema
from myapi.models.tag import Tag
from myapi.models.news import News
from myapi.extensions import db


class TagnewsList(Resource):

    method_decorators = [jwt_required()]

    @jwt_required()
    def post(self):
        schema = TagNewsSchema()
        tagnews = schema.load(request.json)
        tag_id = request.args.get('tag_id')
        news_id = request.args.get('news_id')


        tag = Tag.query.filter_by(tag_id)
        
        # print (tag)
        if tag == None :
            return {"tag is not existed"} , 404

        news = News.query.filter_by(news_id)
        
        if news == None :
            return {"news is not existed"} , 404

        db.session.add(tagnews)
        db.session.commit()

        return {"msg": "tagnews upload", "tagnews": schema.dump(tagnews)}, 200
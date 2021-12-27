from functools import partial
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from myapi.models.news import News
from myapi.news.schemas import NewsSchema
from myapi.extensions import db




class NewsList(Resource):

    """Creation 

    ---
    post:
      tags:
        - news
      summary: Create a news
      description: Create a news post
      requestBody:
        content:
          application/json:
            schema:
              NewsSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: news upload
                  news: NewsSchema
    """

    method_decorators = [jwt_required()]

    @jwt_required()
    def post(self):
        schema = NewsSchema()
        news = schema.load(request.json)

        news.user_id = current_user.id

        db.session.add(news)
        db.session.commit()

        return {"msg":"news upload","news": schema.dump(news)}, 201


class NewsResource(Resource):

    """Single object resource

    ---
    get:
      tags:
        - news
      summary: Get a news
      description: Get a single news by ID
      parameters:
        - in: path
          name: news_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  news: NewsSchema
        404:
          description: news does not exists
    put:
      tags:
        - news
      summary: Update a news
      description: Update a single news by ID
      parameters:
        - in: path
          name: news_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              NewsSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: news updated
                  news: NewsSchema
        404:
          description: news does not exists
    delete:
      tags:
        - news
      summary: Delete a news
      description: Delete a single news by ID
      parameters:
        - in: path
          name: news_id
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
                    example: news deleted
        404:
          description: news does not exists
    """

    method_decorators = [jwt_required()]

    def get(self, news_id):
        schema = NewsSchema()
        news = News.query.get_or_404(news_id)
        return {"news": schema.dump(news)}

    
    def put(self, news_id):
        schema = NewsSchema(partial=True)
        news = News.query.get_or_404(news_id)
        news.updated_at = db.func.current_timestamp()
        news = schema.load(request.json, instance=news)

        db.session.commit()

        return {"msg": "news updated", "news": schema.dump(news)}

    def delete(self, news_id):
        news = News.query.get_or_404(news_id)
        db.session.delete(news)
        db.session.commit()

        return {"msg": "news deleted"}
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from myapi.models.news import News
from myapi.schemas import NewsSchema
from myapi.extensions import db
from myapi.minio_handler import MinioHandler
from io import BytesIO
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class NewsPicture(Resource):

    """Upload Image for News 

    ---
    put:
      tags:
        - news
      summary: Upload image 
      description: Upload image for news
      parameters:
        - in: path
          name: news_id
          schema:
            type: integer
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  bucket_name:
                    type: string
                    example: bucket_name
                  file_name:
                    type: string
                    example: file_name
                  url:
                    type: text
                    example: url
        404:
          description: no news found
        400:
          description: allow file type are .png , .jpg , .jpeg
    get:
        tags:
          - news
        summary: Get a Picture
        description: Get a picture on news 
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
                    url:
                    type: text
                    example: url
          404:
            description: images does not exists
    """

    method_decorators = [jwt_required()]

    @jwt_required()
    def put(self, news_id):
        
        schema = NewsSchema(partial=True)
        news = News.query.get_or_404(news_id)
        
        if news == None :
          return {"msg": "no news found"}, 404

        if 'file' not in request.files:
          return {"msg": "no files in request"} , 400
        
        file = request.files['file']

        if file.filename == '':
          return {"msg": "no files are selected"}, 400

        if file and allowed_file(file.filename):
        # try

          data = file.read()

          file_name = " ".join(file.filename.strip().split())

          data_file = MinioHandler().get_instance().put_object(
          file_name=file_name,
          file_data=BytesIO(data),
          content_type=file.content_type
          )

          news.picture = data_file.get('file_name')
          db.session.commit()

          print(data_file)

          return data_file
        else :
          return {"msg": "allow file type are .png , .jpg , .jpeg"} , 400
    
        # except CustomException as e:
        #   raise e
        # except Exception as e:
        #   if e.__class__.__name__ == 'MaxRetryError':
        #     raise CustomException(http_code=400, code='400', message='Can not connect to Minio')
        #   raise CustomException(code='999', message='Server Error')

    @jwt_required()
    def get(self, news_id):

      news = News.query.get_or_404(news_id)
        
      if news == None :
        return {"msg": "no news found"}, 404

      picture_name = news.picture

      minio_client = MinioHandler().get_instance()
      if not minio_client.check_file_name_exists(minio_client.bucket_name, picture_name):
          return{"msg": "image not found"}, 400

      file = MinioHandler().presigned_get_object(bucket_name=minio_client.bucket_name, object_name=picture_name)

      return {'url':file} , 201

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
 
        return {"msg": "news upload", "news": schema.dump(news)}, 
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

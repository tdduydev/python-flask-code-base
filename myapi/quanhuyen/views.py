from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import jwt_required
from myapi.schemas.quanhuyen import QuanhuyenSchema
from myapi.commons.pagination import paginate
from myapi.extensions import db, apispec
from myapi.models import Quanhuyen, Tinhthanh
from myapi.schemas.tinhthanh import TinhthanhSchema

blueprint = Blueprint("quanhuyen",__name__, url_prefix="/quanhuyen")

@blueprint.route("",methods=["GET"])
@jwt_required()
def get_listquanhuyen():
    
    """Danh sach quan huyen

      ---
      get:
        tags:
          - VietNam
        summary: Danh sach quan huyen theo tinh, thanh pho
        description: Danh sach quan huyen theo tinh, thanh pho
        parameters:
          - in: query
            name: ten_tinhthanh
            schema:
              type: string
        responses:
          200:
            allOf:
              - $ref: '#/components/schemas/PaginatedResult'
              - type: object
                properties:
                  results:
                    type: array
                    items:
                      $ref: '#/components/schemas/TinhthanhSchema'
          404:
            description: khong ton tai
      """

    schema = QuanhuyenSchema(many=True)
    ten_tinhthanh = request.args.get('ten_tinhthanh')
    tinhthanh = Tinhthanh.query.filter_by(ten = ten_tinhthanh).first()
    quanhuyen = Quanhuyen.query.filter_by(tinhthanh_id = tinhthanh.id)

    return paginate(quanhuyen, schema)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("QuanhuyenSchema", schema=QuanhuyenSchema)
    apispec.spec.path(view=get_listquanhuyen, app=app)


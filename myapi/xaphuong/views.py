from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import jwt_required
from myapi.schemas.xaphuong import XaPhuongSchema
from myapi.commons.pagination import paginate
from myapi.extensions import db, apispec
from myapi.models import Quanhuyen, Xaphuong, xaphuong
from myapi.schemas.quanhuyen import QuanhuyenSchema

blueprint = Blueprint("xaphuong",__name__, url_prefix="/xaphuong")

@blueprint.route("",methods=["GET"])
@jwt_required()
def get_listxaphuong():

    """Danh sach xa phuong

      ---
      get:
        tags:
          - VietNam
        summary: Danh sach  xa phuong theo quan, huyen
        description: Danh sach xa phuong theo quan, huyen
        parameters:
          - in: query
            name: ten_quanhuyen
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
                      $ref: '#/components/schemas/XaPhuongSchema'
          404:
            description: khong ton tai
      """

    schema = XaPhuongSchema(many=True)
    ten_quanhuyen = request.args.get('ten_quanhuyen')
    quanhuyen = Quanhuyen.query.filter_by(ten = ten_quanhuyen).first()
    xaphuong = Xaphuong.query.filter_by(quanhuyen_id = quanhuyen.id)

    return paginate(xaphuong, schema)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("XaPhuongSchema", schema=XaPhuongSchema)
    apispec.spec.path(view=get_listxaphuong, app=app)


from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import jwt_required
from myapi.schemas.tinhthanh import TinhthanhSchema
from myapi.commons.pagination import paginate
from myapi.extensions import db, apispec
from myapi.models import Tinhthanh




blueprint = Blueprint("tinhthanh",__name__, url_prefix="/tinhthanh")


@blueprint.route("",methods=["GET"])
@jwt_required()
def get_listtinhthanh():
    """Get All

    ---
    get:
      tags:
        - VietNam
      summary: danh sach tinh thanh Viet Nam
      description: danh sach tinh thanh Viet Nam
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
                          $ref: '#/components/schemas/TinhthanhSchema'
    """

    schema = TinhthanhSchema(many=True)
    query = Tinhthanh.query
    return paginate(query, schema)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("TinhthanhSchema", schema=TinhthanhSchema)
    apispec.spec.path(view=get_listtinhthanh, app=app)